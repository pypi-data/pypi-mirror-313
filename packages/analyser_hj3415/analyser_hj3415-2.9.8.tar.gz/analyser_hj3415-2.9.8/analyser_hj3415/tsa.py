"""
Time Series Analysis
"""
from pprint import pprint

import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import StandardScaler
from utils_hj3415 import utils, helpers
from typing import Optional
import plotly.graph_objs as go
from plotly.offline import plot
import matplotlib.pyplot as plt  # Matplotlib 수동 임포트
from db_hj3415 import myredis
from collections import OrderedDict
from analyser_hj3415 import eval
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import Input
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from dataclasses import dataclass
import itertools

import logging

tsa_logger = helpers.setup_logger('tsa_logger', logging.WARNING)

expire_time = 3600 * 24

class MyProphet:
    expire_time_h = 24
    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self.scaler = StandardScaler()

        self.model = Prophet()
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.raw_data = self._get_raw_data()
        self.df_real = self._preprocessing_for_prophet()
        self.df_forecast = self._make_forecast()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        tsa_logger.info(f'change code : {self.code} -> {code}')
        self.model = Prophet()
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.raw_data = self._get_raw_data()
        self.df_real = self._preprocessing_for_prophet()
        self.df_forecast = self._make_forecast()

    @staticmethod
    def is_valid_date(date_string):
        try:
            # %Y-%m-%d 형식으로 문자열을 datetime 객체로 변환 시도
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            # 변환이 실패하면 ValueError가 발생, 형식이 맞지 않음
            return False

    def _get_raw_data(self) -> pd.DataFrame:
        """
        야후에서 해당 종목의 4년간 주가 raw data를 받아온다.
        :return:
        """
        # 오늘 날짜 가져오기
        today = datetime.today()

        # 4년 전 날짜 계산 (4년 = 365일 * 4)
        four_years_ago = today - timedelta(days=365 * 4)

        return yf.download(
            self.code + '.KS',
            start=four_years_ago.strftime('%Y-%m-%d'),
            end=today.strftime('%Y-%m-%d')
        )

    def _preprocessing_for_prophet(self) -> pd.DataFrame:
        """
        Prophet이 사용할 수 있도록 데이터 준비
        ds는 날짜, y는 주가
        :return:
        """
        df = self.raw_data[['Close', 'Volume']].reset_index()
        df.columns = ['ds', 'y', 'volume']  # Prophet의 형식에 맞게 열 이름 변경

        # ds 열에서 타임존 제거
        df['ds'] = df['ds'].dt.tz_localize(None)

        # 추가 변수를 정규화
        df['volume_scaled'] = self.scaler.fit_transform(df[['volume']])
        tsa_logger.debug('_preprocessing_for_prophet')
        tsa_logger.debug(df)
        return df

    def _make_forecast(self) -> pd.DataFrame:
        # 정규화된 'volume_scaled' 변수를 외부 변수로 추가
        self.model.add_regressor('volume_scaled')

        self.model.fit(self.df_real)

        # 향후 180일 동안의 주가 예측
        future = self.model.make_future_dataframe(periods=180)
        tsa_logger.debug('_make_forecast_future')
        tsa_logger.debug(future)

        # 미래 데이터에 거래량 추가 (평균 거래량을 사용해 정규화)
        future_volume = pd.DataFrame({'volume': [self.raw_data['Volume'].mean()] * len(future)})
        future['volume_scaled'] = self.scaler.transform(future_volume[['volume']])

        forecast = self.model.predict(future)
        tsa_logger.debug('_make_forecast')
        tsa_logger.debug(forecast)
        return forecast

    def get_yhat(self) -> dict:
        """
        최근 날짜의 예측데이터를 반환한다.
        :return: {'ds':..., 'yhat':.., 'yhat_lower':.., 'yhat_upper':..,}
        """
        df = self.df_forecast
        last_real_date = self.df_real.iloc[-1]['ds']
        tsa_logger.info(last_real_date)
        yhat_dict = df[df['ds']==last_real_date].iloc[0][['ds', 'yhat_lower', 'yhat_upper', 'yhat']].to_dict()
        tsa_logger.info(yhat_dict)
        return yhat_dict

    def visualization(self):
        # 예측 결과 출력
        print(self.df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # 예측 결과 시각화 (Matplotlib 사용)
        fig = self.model.plot(self.df_forecast)
        # 추세 및 계절성 시각화
        fig2 = self.model.plot_components(self.df_forecast)
        plt.show()  # 시각화 창 띄우기

    def export(self, to="str") -> Optional[str]:
        """
        prophet과 plotly로 그래프를 그려서 html을 문자열로 반환
        :param to: str, png, htmlfile
        :return:
        """
        # Plotly를 사용한 시각화
        fig = go.Figure()

        # 실제 데이터
        fig.add_trace(go.Scatter(x=self.df_real['ds'], y=self.df_real['y'], mode='markers', name='실제주가'))
        # 예측 데이터
        fig.add_trace(go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat'], mode='lines', name='예측치'))

        # 상한/하한 구간
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_upper'], fill=None, mode='lines', name='상한'))
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_lower'], fill='tonexty', mode='lines', name='하한'))

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis = dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis = dict(
                tickformat=".0f",  # 소수점 없이 원래 숫자 표시
            ),
            showlegend=False,
        )

        if to == 'str':
            # 그래프 HTML로 변환 (string 형식으로 저장)
            graph_html = plot(fig, output_type='div')
            return graph_html
        elif to == 'png':
            # 그래프를 PNG 파일로 저장
            fig.write_image(f"myprophet_{self.code}.png")
            return None
        elif to == 'htmlfile':
            # 그래프를 HTML로 저장
            plot(fig, filename=f'myprophet_{self.code}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

    @classmethod
    def ranking(cls, refresh = False) -> OrderedDict:
        """
        가장 최근 날짜의 랭킹 분석
        :param refresh:
        :return:
        """
        print("**** Start myprophet_ranking... ****")
        redis_name = 'myprophet_ranking'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {MyProphet.expire_time_h}h")

        def fetch_ranking() -> dict:
            data = {}
            p = MyProphet('005930')
            for i, code in enumerate(myredis.Corps.list_all_codes()):
                p.code = code
                last_real_data = p._preprocessing_for_prophet().iloc[-1]
                recent_price = last_real_data['y']
                recent_date = datetime.strftime(last_real_data['ds'], '%Y-%m-%d')
                yhat_dict = p.get_yhat()
                tsa_logger.info(f'recent_price: {recent_price}, yhat_dict: {yhat_dict}')
                yhat_lower = int(yhat_dict['yhat_lower'])
                if recent_price < yhat_lower:
                    deviation = int(eval.Tools.cal_deviation(recent_price, yhat_lower))
                    data[code] = deviation
                    print(f"{i}.{p.code}/{p.name} date: {recent_date} 가격:{recent_price} 기대하한값:{yhat_lower} 편차:{deviation}")
            return data

        data_dict = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_ranking, timer=MyProphet.expire_time_h * 3600)

        return OrderedDict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

@dataclass
class LSTMData:
    code: str

    data_2d: np.ndarray
    train_size: int
    train_data_2d: np.ndarray
    test_data_2d: np.ndarray

    X_train_3d: np.ndarray
    X_test_3d: np.ndarray
    y_train_1d: np.ndarray
    y_test_1d: np.ndarray

@dataclass
class LSTMGrade:
    """
    딥러닝 모델의 학습 결과를 평가하기 위해 사용하는 데이터 클래스
    """
    code: str

    mean_train_prediction_2d: np.ndarray
    mean_test_predictions_2d: np.ndarray

    train_mse: float
    train_mae: float
    train_r2: float
    test_mse: float
    test_mae: float
    test_r2: float

class MyLSTM:
    """
    LSTM(Long Short-Term Memory)
    """
    # 미래 몇일을 예측할 것인가?
    future_days = 30
    expire_time_h = 24

    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.raw_data = self._get_raw_data()
        self.lstm_data = self._preprocessing_for_lstm()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        tsa_logger.info(f'change code : {self.code} -> {code}')

        self._code = code
        self.name = myredis.Corps(code, 'c101').get_name()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.raw_data = self._get_raw_data()
        self.lstm_data = self._preprocessing_for_lstm()

    def _get_raw_data(self) -> pd.DataFrame:
        """
        야후에서 해당 종목의 4년간 주가 raw data를 받아온다.
        :return:
        """
        # 오늘 날짜 가져오기
        today = datetime.today()

        # 4년 전 날짜 계산 (4년 = 365일 * 4)
        four_years_ago = today - timedelta(days=365 * 4)
        tsa_logger.info(f"start: {four_years_ago.strftime('%Y-%m-%d')}, end: {today.strftime('%Y-%m-%d')}")

        df = yf.download(
            self.code + '.KS',
            start=four_years_ago.strftime('%Y-%m-%d'),
            end=today.strftime('%Y-%m-%d')
        )
        df.index = df.index.tz_localize(None)
        tsa_logger.debug(df)
        return df

    def _preprocessing_for_lstm(self) -> LSTMData:
        """
        lstm이 사용할 수 있도록 데이터 준비(정규화 및 8:2 훈련데이터 검증데이터 분리 및 차원변환)
        :return:
        """
        # 필요한 열만 선택 (종가만 사용) - 2차웜 배열로 변환
        data_2d = self.raw_data['Close'].values.reshape(-1, 1)
        tsa_logger.debug(data_2d)

        # 데이터 정규화 (0과 1 사이로 스케일링)
        scaled_data_2d = self.scaler.fit_transform(data_2d)

        # 학습 데이터 생성
        # 주가 데이터를 80%는 학습용, 20%는 테스트용으로 분리하는 코드
        train_size = int(len(scaled_data_2d) * 0.8)
        train_data_2d = scaled_data_2d[:train_size]
        test_data_2d = scaled_data_2d[train_size:]
        tsa_logger.info(f'총 {len(data_2d)}개 데이터, train size : {train_size}')

        # 학습 데이터에 대한 입력(X)과 정답(y)를 생성
        def create_dataset(data, time_step=60):
            X, y = [], []
            for i in range(len(data) - time_step):
                X.append(data[i:i + time_step, 0])
                y.append(data[i + time_step, 0])
            return np.array(X), np.array(y)

        X_train, y_train_1d = create_dataset(train_data_2d)
        X_test, y_test_1d = create_dataset(test_data_2d)

        # LSTM 모델 입력을 위해 데이터를 3차원으로 변환
        X_train_3d = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test_3d = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        tsa_logger.debug(f'n_dim - X_train_3d : {X_train_3d.ndim}, X_test_3d : {X_test_3d.ndim}, y_train : {y_train_1d.ndim}, y_test : {y_test_1d.ndim}')
        tsa_logger.debug(f'len - X_train_3d : {len(X_train_3d)}, X_test_3d : {len(X_test_3d)}, y_train : {len(y_train_1d)}, y_test : {len(y_test_1d)}')

        return LSTMData(
            code=self.code,
            data_2d=data_2d,
            train_size=train_size,
            train_data_2d=train_data_2d,
            test_data_2d=test_data_2d,
            X_train_3d=X_train_3d,
            X_test_3d=X_test_3d,
            y_train_1d=y_train_1d,
            y_test_1d=y_test_1d,
        )

    def _model_training(self) -> Sequential:
        # LSTM 모델 생성 - 유닛과 드롭아웃의 수는 테스트로 최적화 됨.
        model = Sequential()
        # Input(shape=(50, 1))는 50개의 타임스텝을 가지는 입력 데이터를 처리하며, 각 타임스텝에 1개의 특성이 있다는 것을 의미
        model.add(Input(shape=(self.lstm_data.X_train_3d.shape[1], 1)))  # 입력 레이어에 명시적으로 Input을 사용
        model.add(LSTM(units=150, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=75, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=25))
        model.add(Dropout(0.3))
        model.add(Dense(units=1))

        # 모델 요약 출력
        # model.summary()

        # 모델 컴파일 및 학습
        model.compile(optimizer='adam', loss='mean_squared_error')

        # 조기 종료 설정
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        # 모델 학습 - 과적합 방지위한 조기종료 세팅
        model.fit(self.lstm_data.X_train_3d, self.lstm_data.y_train_1d,
                  epochs=75, batch_size=32, validation_data=(self.lstm_data.X_test_3d, self.lstm_data.y_test_1d),
                  callbacks=[early_stopping])
        return model

    def ensemble_training(self, num) -> tuple:
        """
        딥러닝을 num 회 반복하고 평균을 사용하는 함수
        :param num: 앙상블 모델 수
        :return:
        """
        def prediction(model_in: Sequential, data: np.ndarray) -> np.ndarray:
            """
            훈련될 모델을 통해 예측을 시행하여 정규화를 복원하고 결과 반환한다.
            :param model_in:
            :param data:
            :return:
            """
            predictions_2d = model_in.predict(data)
            predictions_scaled_2d = self.scaler.inverse_transform(predictions_2d)  # 스케일링 복원
            tsa_logger.info(f'predictions_scaled_2d : ndim - {predictions_scaled_2d.ndim} len - {len(predictions_scaled_2d)}')  # numpy.ndarray 타입
            tsa_logger.debug(predictions_scaled_2d)
            return predictions_scaled_2d

        ensemble_train_predictions_2d = []
        ensemble_test_predictions_2d = []
        ensemble_future_predictions_2d = []

        for i in range(num):
            print(f"Training model {i + 1}/{num}...")
            model = self._model_training()

            # 훈련 데이터 예측
            train_predictions_scaled_2d = prediction(model, self.lstm_data.X_train_3d)
            ensemble_train_predictions_2d.append(train_predictions_scaled_2d)

            # 테스트 데이터 예측
            test_predictions_scaled_2d = prediction(model, self.lstm_data.X_test_3d)
            ensemble_test_predictions_2d.append(test_predictions_scaled_2d)

            # 8. 미래 30일 예측
            # 마지막 60일간의 데이터를 기반으로 미래 30일을 예측

            last_60_days_2d = self.lstm_data.test_data_2d[-60:]
            last_60_days_3d = last_60_days_2d.reshape(1, -1, 1)

            future_predictions = []
            for _ in range(self.future_days):
                predicted_price_2d = model.predict(last_60_days_3d)
                future_predictions.append(predicted_price_2d[0][0])

                # 예측값을 다시 입력으로 사용하여 새로운 예측을 만듦
                predicted_price_reshaped = np.reshape(predicted_price_2d, (1, 1, 1))  # 3D 배열로 변환
                last_60_days_3d = np.append(last_60_days_3d[:, 1:, :], predicted_price_reshaped, axis=1)

            # 예측된 주가를 다시 스케일링 복원
            future_predictions_2d = np.array(future_predictions).reshape(-1, 1)
            future_predictions_scaled_2d = self.scaler.inverse_transform(future_predictions_2d)
            ensemble_future_predictions_2d.append(future_predictions_scaled_2d)

        return ensemble_train_predictions_2d, ensemble_test_predictions_2d, ensemble_future_predictions_2d

    def grading(self, ensemble_train_predictions_2d: list, ensemble_test_predictions_2d: list) -> LSTMGrade:
        """
        딥러닝 결과를 분석하기 위한 함수
        :param ensemble_train_predictions_2d:
        :param ensemble_test_predictions_2d:
        :return:
        """
        # 예측값을 평균내서 최종 예측값 도출
        mean_train_prediction_2d = np.mean(ensemble_train_predictions_2d, axis=0)
        mean_test_predictions_2d = np.mean(ensemble_test_predictions_2d, axis=0)

        # y값(정답) 정규화 해제
        y_train_scaled_2d = self.scaler.inverse_transform(self.lstm_data.y_train_1d.reshape(-1, 1))
        y_test_scaled_2d = self.scaler.inverse_transform(self.lstm_data.y_test_1d.reshape(-1, 1))

        # 평가 지표 계산
        train_mse = mean_squared_error(y_train_scaled_2d, mean_train_prediction_2d)
        train_mae = mean_absolute_error(y_train_scaled_2d, mean_train_prediction_2d)
        train_r2 = r2_score(y_train_scaled_2d, mean_train_prediction_2d)

        test_mse = mean_squared_error(y_test_scaled_2d, mean_test_predictions_2d)
        test_mae = mean_absolute_error(y_test_scaled_2d, mean_test_predictions_2d)
        test_r2 = r2_score(y_test_scaled_2d, mean_test_predictions_2d)

        # 평가 결과 출력
        print("Training Data:")
        print(f"Train MSE: {train_mse}, Train MAE: {train_mae}, Train R²: {train_r2}")
        print("\nTesting Data:")
        print(f"Test MSE: {test_mse}, Test MAE: {test_mae}, Test R²: {test_r2}")
        # mse, mae는 작을수록 좋으며 R^2은 0-1 사이값 1에 가까울수록 정확함
        # 과적합에 대한 평가는 train 과 test를 비교하여 test가 너무 않좋으면 과적합 의심.

        return LSTMGrade(
            code=self.code,
            mean_train_prediction_2d=mean_train_prediction_2d,
            mean_test_predictions_2d=mean_test_predictions_2d,
            train_mse=train_mse,
            train_mae=train_mae,
            train_r2=train_r2,
            test_mse=test_mse,
            test_mae=test_mae,
            test_r2=test_r2,
        )

    def get_final_predictions(self, refresh, num=5) -> tuple:
        """
        미래 예측치를 레디스 캐시를 이용하여 반환함
        :param refresh:
        :param num: 앙상블 반복횟수
        :return:
        """
        print("**** Start get_final_predictions... ****")
        redis_name = f'{self.code}_mylstm_predictions'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {MyLSTM.expire_time_h}h")

        def fetch_final_predictions(num_in) -> tuple:
            """
            앙상블법으로 딥러닝을 모델을 반복해서 평균을 내서 미래를 예측한다. 평가는 래시스 캐시로 반환하기 어려워 일단 디버그 용도로만 사용하기로
            :param num_in:
            :return:
            """
            # 앙상블 테스트와 채점
            _, _, ensemble_future_predictions_2d = self.ensemble_training(
                num=num_in)

            """if grading:
                lstm_grade = self.grading(ensemble_train_predictions_2d, ensemble_test_predictions_2d)
            else:
                lstm_grade = None"""

            # 시각화를 위한 준비 - 날짜 생성 (미래 예측 날짜), 미래예측값 평균
            last_date = self.raw_data.index[-1]
            future_dates = pd.date_range(last_date, periods=self.future_days + 1).tolist()[1:]

            # Timestamp 객체를 문자열로 변환
            future_dates_str= [date.strftime('%Y-%m-%d') for date in future_dates]

            final_future_predictions = np.mean(ensemble_future_predictions_2d, axis=0)
            tsa_logger.info(f'num - future dates : {len(future_dates_str)} future data : {len(final_future_predictions)}')

            assert len(future_dates_str) == len(final_future_predictions), "future_dates 와 final_future_predictions 개수가 일치하지 않습니다."

            return future_dates_str, final_future_predictions.tolist()

        future_dates_str, final_future_predictions = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_final_predictions, num, timer=MyLSTM.expire_time_h * 3600)

        # 문자열을 날짜 형식으로 변환
        future_dates = [datetime.strptime(date, '%Y-%m-%d') for date in future_dates_str]

        # 리스트를 다시 NumPy 배열로 변환
        final_future_predictions = np.array(final_future_predictions)

        return future_dates, final_future_predictions

    def export(self, refresh=False, to="str") -> Optional[str]:
        """
        prophet과 plotly로 그래프를 그려서 html을 문자열로 반환
        :param refresh:
        :param to: str, htmlfile, png
        :return:
        """
        future_dates, final_future_predictions = self.get_final_predictions(refresh=refresh)
        final_future_predictions = final_future_predictions.reshape(-1) # 차원을 하나 줄인다.

        # 데이터 준비
        self.raw_data = self.raw_data.reset_index()
        data = self.raw_data[['Date', 'Close']][-120:].reset_index(drop=True)

        # 'Date'와 'Close' 열 추출
        actual_dates = pd.to_datetime(data['Date'])
        actual_close = data['Close']

        # 'actual_close'가 Series인지 확인
        if isinstance(actual_close, pd.DataFrame):
            actual_close = actual_close.squeeze()

        # 'Close' 열의 데이터 타입 확인
        actual_close = actual_close.astype(float)

        # 예측 데이터 준비
        predicted_dates = pd.to_datetime(future_dates)
        predicted_close = pd.Series(final_future_predictions, index=range(len(final_future_predictions))).astype(float)

        # 그래프 생성
        fig = go.Figure()

        # 실제 데이터 추가
        fig.add_trace(go.Scatter(
            x=actual_dates,
            y=actual_close,
            mode='markers',
            name='실제주가'
        ))

        # 예측 데이터 추가
        fig.add_trace(go.Scatter(
            x=predicted_dates,
            y=predicted_close,
            mode='lines+markers',
            name='예측치(30일)'
        ))

        # 레이아웃 업데이트
        fig.update_layout(
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis=dict(
                tickformat='%Y/%m',
            ),
            yaxis=dict(
                tickformat=".0f",
            ),
            showlegend=True,
        )

        tsa_logger.debug(f"actual_dates({len(actual_dates)}) - {actual_dates}")
        tsa_logger.debug(f"actual_close({len(actual_close)} - {actual_close}")
        tsa_logger.debug(f"predicted_dates({len(future_dates)}) - {future_dates}")
        tsa_logger.debug(f"predicted_close({len(predicted_close)}) - {predicted_close}")

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis = dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis = dict(
                tickformat=".0f",  # 소수점 없이 원래 숫자 표시
            ),
            showlegend=False,
        )

        if to == 'str':
            # 그래프 HTML로 변환 (string 형식으로 저장)
            graph_html = plot(fig, output_type='div')
            return graph_html
        elif to == 'png':
            # 그래프를 PNG 파일로 저장
            fig.write_image(f"myLSTM_{self.code}.png")
            return None
        elif to == 'htmlfile':
            # 그래프를 HTML로 저장
            plot(fig, filename=f'myLSTM_{self.code}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

    def visualization(self, refresh=True):
        future_dates, final_future_predictions = self.get_final_predictions(refresh=refresh)

        # 시각화1
        plt.figure(figsize=(10, 6))

        # 실제 주가
        plt.plot(self.raw_data.index, self.raw_data['Close'], label='Actual Price')

        # 미래 주가 예측
        plt.plot(future_dates, final_future_predictions, label='Future Predicted Price', linestyle='--')

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.title('Apple Stock Price Prediction with LSTM')
        plt.show()

        """# 시각화2
        plt.figure(figsize=(10, 6))
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], self.lstm_data.data_2d[self.lstm_data.train_size + 60:], label='Actual Price')
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], lstm_grade.mean_test_predictions_2d, label='Predicted Price')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.title('Stock Price Prediction with LSTM Ensemble')
        plt.show()"""

    @staticmethod
    def caching_based_on_prophet_ranking(refresh: bool, top=20):
        ranking_topn = OrderedDict(itertools.islice(MyProphet.ranking().items(), top))
        tsa_logger.info(ranking_topn)
        mylstm = MyLSTM('005930')
        print(f"*** LSTM prediction redis cashing top{top} items ***")
        for i, (code, _) in enumerate(ranking_topn.items()):
            mylstm.code = code
            print(f"{i+1}. {mylstm.code}/{mylstm.name}")
            mylstm.get_final_predictions(refresh=refresh, num=5)




