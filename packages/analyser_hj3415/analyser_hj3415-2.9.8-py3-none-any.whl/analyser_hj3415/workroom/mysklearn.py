import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. 데이터 다운로드 (애플 주식 데이터를 사용)
# 데이터 기간: 2020년 1월 1일부터 2023년 1월 1일까지
#stock_data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')
# 삼성전자 주식 데이터 가져오기 (KOSPI 상장)
stock_data = yf.download('005930.KS', start='2020-01-01', end='2024-08-01')
# 크래프톤 주식 데이터 가져오기 (KOSPI 상장)
#stock_data = yf.download('259960.KS', start='2020-01-01', end='2024-10-08')

# 2. 필요한 열만 선택 (종가만 사용)
df = stock_data[['Close']]

# 3. 주가 데이터를 시계열 데이터로 변환하여 예측
# 일자를 숫자로 변환 (날짜 자체는 예측 모델에 사용하기 어렵기 때문에 숫자로 변환)
df['Date'] = np.arange(len(df))

# 4. 독립 변수(X)와 종속 변수(y) 분리
X = df[['Date']]  # 독립 변수 (날짜)
y = df['Close']  # 종속 변수 (주가)

# 5. 데이터를 학습용과 테스트용으로 분리 (80% 학습, 20% 테스트)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. 선형 회귀 모델 생성 및 학습
model = LinearRegression()
model.fit(X_train, y_train)

# 7. 테스트 데이터를 사용하여 예측 수행
y_pred = model.predict(X_test)

# 8. 결과 시각화
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, color='blue', label='Training data')  # 학습 데이터
plt.scatter(X_test, y_test, color='green', label='Test data')  # 실제 테스트 데이터
plt.plot(X_test, y_pred, color='red', label='Predicted price')  # 예측된 주가
plt.xlabel('Date (numeric)')
plt.ylabel('Stock Price (Close)')
plt.legend()
plt.title('Apple Stock Price Prediction')
plt.show()

# 9. 모델 평가 (R^2 스코어)
r2_score = model.score(X_test, y_test)
print(f"모델의 R^2 스코어: {r2_score:.2f}")