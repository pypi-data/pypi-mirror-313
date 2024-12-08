from dataclasses import dataclass, asdict

from utils_hj3415 import utils, helpers
from typing import Tuple
from db_hj3415 import myredis, mymongo
import math
from analyser_hj3415.cli import AnalyserSettingsManager
from collections import OrderedDict
import logging

eval_logger = helpers.setup_logger('eval_logger', logging.WARNING)

expire_time = 3600 * 12

class Tools:
    @staticmethod
    def cal_deviation(v1: float, v2: float) -> float:
        """
        괴리율 구하는 공식
        :param v1:
        :param v2:
        :return:
        """
        try:
            deviation = abs((v1 - v2) / v1) * 100
        except ZeroDivisionError:
            deviation = math.nan
        return deviation

    @staticmethod
    def date_set(*args) -> list:
        """
        비유효한 내용 제거(None,nan)하고 중복된 항목 제거하고 리스트로 반환한다.
        여기서 set의 의미는 집합을 뜻함
        :param args:
        :return:
        """
        return [i for i in {*args} if i != "" and i is not math.nan and i is not None]

    @staticmethod
    def calc당기순이익(c103: myredis.C103, refresh: bool) -> Tuple[str, float]:
        """
        지배지분 당기순이익 계산

        일반적인 경우로는 직전 지배주주지분 당기순이익을 찾아서 반환한다.\n
        금융기관의 경우는 지배당기순이익이 없기 때문에\n
        계산을 통해서 간접적으로 구한다.\n
        """
        name = myredis.Corps(c103.code, 'c101').get_name(refresh=refresh)

        eval_logger.info(f'{c103.code} / {name} Tools : 당기순이익 계산.. refresh : {refresh}')
        c103.page = 'c103재무상태표q'

        d1, 지배당기순이익 = c103.latest_value_pop2('*(지배)당기순이익', refresh)
        eval_logger.debug(f"*(지배)당기순이익: {지배당기순이익}")

        if math.isnan(지배당기순이익):
            eval_logger.warning(f"{c103.code} / {name} - (지배)당기순이익이 없는 종목. 수동으로 계산합니다.")
            c103.page = 'c103손익계산서q'
            d2, 최근4분기당기순이익 = c103.sum_recent_4q('당기순이익', refresh)
            eval_logger.debug(f"{c103.code} / {name} - 최근4분기당기순이익 : {최근4분기당기순이익}")
            c103.page = 'c103재무상태표y'
            d3, 비지배당기순이익 = c103.latest_value_pop2('*(비지배)당기순이익', refresh)
            eval_logger.debug(f"{c103.code} / {name} - 비지배당기순이익y : {비지배당기순이익}")
            # 가변리스트 언패킹으로 하나의 날짜만 사용하고 나머지는 버린다.
            # 여기서 *_는 “나머지 값을 다 무시하겠다”는 의미
            eval_logger.debug(f"d2:{d2}, d3: {d3}")
            try:
                date, *_ = Tools.date_set(d2, d3)
            except ValueError:
                # 날짜 데이터가 없는경우
                date = ''
            계산된지배당기순이익= round(최근4분기당기순이익 - utils.nan_to_zero(비지배당기순이익), 1)
            eval_logger.debug(f"{c103.code} / {name} - 계산된 지배당기순이익 : {계산된지배당기순이익}")
            return date, 계산된지배당기순이익
        else:
            return d1, 지배당기순이익

    @staticmethod
    def calc유동자산(c103: myredis.C103, refresh: bool) -> Tuple[str, float]:
        """유효한 유동자산 계산

        일반적인 경우로 유동자산을 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        """
        name = myredis.Corps(c103.code, 'c101').get_name(refresh=refresh)

        eval_logger.info(f'{c103.code} / {name} Tools : 유동자산계산... refresh : {refresh}')
        c103.page = 'c103재무상태표q'

        d, 유동자산 = c103.sum_recent_4q('유동자산', refresh)
        if math.isnan(유동자산):
            eval_logger.warning(f"{c103.code} / {name} - 유동자산이 없는 종목. 수동으로 계산합니다(금융관련업종일 가능성있음).")
            d1, v1 = c103.latest_value_pop2('현금및예치금', refresh)
            d2, v2 = c103.latest_value_pop2('단기매매금융자산', refresh)
            d3, v3 = c103.latest_value_pop2('매도가능금융자산', refresh)
            d4, v4 = c103.latest_value_pop2('만기보유금융자산', refresh)
            eval_logger.debug(f'{c103.code} / {name} 현금및예치금 : {d1}, {v1}')
            eval_logger.debug(f'{c103.code} / {name} 단기매매금융자산 : {d2}, {v2}')
            eval_logger.debug(f'{c103.code} / {name} 매도가능금융자산 : {d3}, {v3}')
            eval_logger.debug(f'{c103.code} / {name} 만기보유금융자산 : {d4}, {v4}')

            try:
                date, *_ = Tools.date_set(d1, d2, d3, d4)
            except ValueError:
                # 날짜 데이터가 없는경우
                date = ''
            계산된유동자산value = round(utils.nan_to_zero(v1) + utils.nan_to_zero(v2) + utils.nan_to_zero(v3) + utils.nan_to_zero(v4),1)

            eval_logger.info(f"{c103.code} / {name} - 계산된 유동자산 : {계산된유동자산value}")
            return date, 계산된유동자산value
        else:
            return d, 유동자산

    @staticmethod
    def calc유동부채(c103: myredis.C103, refresh: bool) -> Tuple[str, float]:
        """유효한 유동부채 계산

        일반적인 경우로 유동부채를 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        """
        name = myredis.Corps(c103.code, 'c101').get_name(refresh=refresh)

        eval_logger.info(f'{c103.code} / {name} Tools : 유동부채계산... refresh : {refresh}')
        c103.page = 'c103재무상태표q'

        d, 유동부채 = c103.sum_recent_4q('유동부채', refresh)
        if math.isnan(유동부채):
            eval_logger.warning(f"{c103.code} / {name} - 유동부채가 없는 종목. 수동으로 계산합니다.")
            d1, v1 = c103.latest_value_pop2('당기손익인식(지정)금융부채', refresh)
            d2, v2 = c103.latest_value_pop2('당기손익-공정가치측정금융부채', refresh)
            d3, v3 = c103.latest_value_pop2('매도파생결합증권', refresh)
            d4, v4 = c103.latest_value_pop2('단기매매금융부채', refresh)
            eval_logger.debug(f'{c103.code} / {name} 당기손익인식(지정)금융부채 : {d1}, {v1}')
            eval_logger.debug(f'{c103.code} / {name} 당기손익-공정가치측정금융부채 : {d2}, {v2}')
            eval_logger.debug(f'{c103.code} / {name} 매도파생결합증권 : {d3}, {v3}')
            eval_logger.debug(f'{c103.code} / {name} 단기매매금융부채 : {d4}, {v4}')

            try:
                date, *_ = Tools.date_set(d1, d2, d3, d4)
            except ValueError:
                # 날짜 데이터가 없는경우
                date = ''
            계산된유동부채value = round(utils.nan_to_zero(v1) + utils.nan_to_zero(v2) + utils.nan_to_zero(v3) + utils.nan_to_zero(v4), 1)

            eval_logger.info(f"{c103.code} / {name} - 계산된 유동부채 : {계산된유동부채value}")
            return date, 계산된유동부채value
        else:
            return d, 유동부채







@dataclass
class RedData:
    code: str
    name: str

    # 사업가치 계산 - 지배주주지분 당기순이익 / 기대수익률
    사업가치: float
    지배주주당기순이익: float
    expect_earn: float

    # 재산가치 계산 - 유동자산 - (유동부채*1.2) + 고정자산중 투자자산
    재산가치: float
    유동자산: float
    유동부채: float
    투자자산: float
    투자부동산: float

    # 부채평가 - 비유동부채
    부채평가: float

    # 발행주식수
    발행주식수: int

    date: list

    red_price: float
    score: int

    def __post_init__(self):
        if not utils.is_6digit(self.code):
            raise ValueError(f"code는 6자리 숫자형 문자열이어야합니다. (입력값: {self.code})")


class Red:
    expect_earn = float(AnalyserSettingsManager().get_value('EXPECT_EARN'))

    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Red : 초기화 ({code})")
        self.c101 = myredis.C101(code)
        self.c103 = myredis.C103(code, 'c103재무상태표q')

        self.name = self.c101.get_name()
        self._code = code

    def __str__(self):
        return f"Red({self.code}/{self.name})"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Red : 종목코드 변경({self.code} -> {code})")
        self.c101.code = code
        self.c103.code = code

        self.name = self.c101.get_name()
        self._code = code

    def _calc비유동부채(self, refresh: bool) -> Tuple[str, float]:
        """유효한 비유동부채 계산

        일반적인 경우로 비유동부채를 찾아서 반환한다.\n
        금융기관의 경우는 간접적으로 계산한다.\n
        """
        eval_logger.info(f'In the calc비유동부채... refresh : {refresh}')
        self.c103.page = 'c103재무상태표q'

        d, 비유동부채 = self.c103.sum_recent_4q('비유동부채', refresh)
        if math.isnan(비유동부채):
            eval_logger.warning(f"{self} - 비유동부채가 없는 종목. 수동으로 계산합니다.")
            # 보험관련업종은 예수부채가 없는대신 보험계약부채가 있다...
            d1, v1 = self.c103.latest_value_pop2('예수부채', refresh)
            d2, v2 = self.c103.latest_value_pop2('보험계약부채(책임준비금)', refresh)
            d3, v3 = self.c103.latest_value_pop2('차입부채', refresh)
            d4, v4 = self.c103.latest_value_pop2('기타부채', refresh)
            eval_logger.debug(f'예수부채 : {d1}, {v1}')
            eval_logger.debug(f'보험계약부채(책임준비금) : {d2}, {v2}')
            eval_logger.debug(f'차입부채 : {d3}, {v3}')
            eval_logger.debug(f'기타부채 : {d4}, {v4}')

            try:
                date, *_ = Tools.date_set(d1, d2, d3, d4)
            except ValueError:
                # 날짜 데이터가 없는경우
                date = ''
            계산된비유동부채value = round(utils.nan_to_zero(v1) + utils.nan_to_zero(v2) + utils.nan_to_zero(v3) + utils.nan_to_zero(v4),1)
            eval_logger.info(f"{self} - 계산된 비유동부채 : {계산된비유동부채value}")
            return date, 계산된비유동부채value
        else:
            return d, 비유동부채

    def _score(self, red_price: int, refresh: bool) -> int:
        """red price와 최근 주가의 괴리율 파악

            Returns:
                int : 주가와 red price 비교한 괴리율
            """
        try:
            recent_price = utils.to_int(self.c101.get_recent(refresh)['주가'])
        except KeyError:
            return 0

        deviation = Tools.cal_deviation(recent_price, red_price)
        if red_price < 0 or (recent_price >= red_price):
            score = 0
        else:
            score = utils.to_int(math.log10(deviation + 1) * 33)  # desmos그래프상 33이 제일 적당한듯(최대100점에 가깝게)

        eval_logger.debug(f"최근주가 : {recent_price} red가격 : {red_price} 괴리율 : {utils.to_int(deviation)} score : {score}")

        return score

    def _generate_data(self, refresh: bool) -> RedData:
        d1, 지배주주당기순이익 = Tools.calc당기순이익(self.c103, refresh)
        eval_logger.debug(f"{self} 지배주주당기순이익: {지배주주당기순이익}")
        d2, 유동자산 = Tools.calc유동자산(self.c103, refresh)
        d3, 유동부채 = Tools.calc유동부채(self.c103, refresh)
        d4, 부채평가 = self._calc비유동부채(refresh)

        self.c103.page = 'c103재무상태표q'
        d5, 투자자산 = self.c103.latest_value_pop2('투자자산', refresh)
        d6, 투자부동산 = self.c103.latest_value_pop2('투자부동산', refresh)

        # 사업가치 계산 - 지배주주지분 당기순이익 / 기대수익률
        사업가치 = round(지배주주당기순이익 / Red.expect_earn, 2)

        # 재산가치 계산 - 유동자산 - (유동부채*1.2) + 고정자산중 투자자산
        재산가치 = round(유동자산 - (유동부채 * 1.2) + utils.nan_to_zero(투자자산) + utils.nan_to_zero(투자부동산), 2)

        _, 발행주식수 = self.c103.latest_value_pop2('발행주식수', refresh)
        if math.isnan(발행주식수):
            발행주식수 = utils.to_int(self.c101.get_recent(refresh).get('발행주식'))
        else:
            발행주식수 = 발행주식수 * 1000

        try:
            red_price = round(((사업가치 + 재산가치 - 부채평가) * 100000000) / 발행주식수)
        except (ZeroDivisionError, ValueError):
            red_price = math.nan

        score = self._score(red_price, refresh)

        try:
            date_list = Tools.date_set(d1, d2, d3, d4)
        except ValueError:
            # 날짜 데이터가 없는경우
            date_list = ['',]

        return RedData(
            code = self.code,
            name = self.name,
            사업가치 = 사업가치,
            지배주주당기순이익 = 지배주주당기순이익,
            expect_earn = Red.expect_earn,
            재산가치 = 재산가치,
            유동자산 = 유동자산,
            유동부채 = 유동부채,
            투자자산 = 투자자산,
            투자부동산 = 투자부동산,
            부채평가 = 부채평가,
            발행주식수 = 발행주식수,
            date = date_list,
            red_price = red_price,
            score = score,
        )

    def get(self, refresh = False, verbose = True) -> RedData:
        """
        RedData 형식의 데이터를 계산하여 리턴하고 레디스 캐시에 저장한다.
        :param refresh:
        :return:
        """
        redis_name = f"{self.code}_red"
        eval_logger.info(f"{self} RedData를 레디스캐시에서 가져오거나 새로 생성합니다.. refresh : {refresh}")
        expire_time = 3600 * 12
        if verbose:
            print(f"{self} redisname: '{redis_name}' / expect_earn: {Red.expect_earn} / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_generate_data(refresh_in: bool) -> dict:
            return asdict(self._generate_data(refresh_in))

        return RedData(**myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_generate_data, refresh, timer=expire_time))

    @classmethod
    def ranking(cls, expect_earn: float = None, refresh = False) -> OrderedDict:
        """
            redis를 사용하며 red score를 계산해서 0이상의 값을 가지는 종목을 순서대로 저장하여 반환한다.
            :param expect_earn: 기대수익률(일반적으로 0.06 - 0.10)
            :param refresh: 캐시를 사용하지 않고 강제로 다시 계산
            :return: OrderedDict([('023590', 101),
                     ('010060', 91),...]), 레디스이름
            """

        print("**** Start red_ranking... ****")
        # expect_earn 및 refresh 설정
        if expect_earn is None:
            expect_earn = cls.expect_earn
        eval_logger.info(f"기대수익률을 {expect_earn}으로 설정합니다.")
        previous_expect_earn = float(AnalyserSettingsManager().get_value('RED_RANKING_EXPECT_EARN'))
        eval_logger.debug(f"previous red ranking expect earn : {previous_expect_earn}")
        if previous_expect_earn != expect_earn:
            eval_logger.warning(f"expect earn : {expect_earn} / RED_RANKING_EXPECT_EARN : {previous_expect_earn} 두 값이 달라 refresh = True")
            refresh = True

        redis_name = 'red_ranking'

        print(f"redisname: '{redis_name}' / expect_earn: {expect_earn} / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_ranking(expect_earn_in: float, refresh_in: bool) -> dict:
            data = {}
            # 저장된 기대수익률을 불러서 임시저장
            ee_orig = Red.expect_earn
            # 원하는 기대수익률로 클래스 세팅
            Red.expect_earn = expect_earn_in
            AnalyserSettingsManager().set_value('RED_RANKING_EXPECT_EARN', str(expect_earn_in))
            red = Red('005930')
            for i, code in enumerate(myredis.Corps.list_all_codes()):
                red.code = code
                red_score = red.get(refresh=refresh_in, verbose=False).score
                if red_score > 0:
                    data[code] = red_score
                    print(f"{i}: {red} - {red_score}")
            # 원래 저장되었던 기대수익률로 다시 복원
            Red.expect_earn = ee_orig
            return data

        data_dict = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_ranking, expect_earn, refresh, timer=expire_time)

        return OrderedDict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))


@dataclass
class MilData:
    code: str
    name: str

    시가총액억: float

    주주수익률: float
    재무활동현금흐름: float

    이익지표: float
    영업활동현금흐름: float
    지배주주당기순이익: float

    #투자수익률
    roic_r: float
    roic_dict: dict
    roe_r: float
    roe_106: dict
    roa_r: float

    #가치지표
    fcf_dict: dict
    pfcf_dict: dict
    pcr_dict: dict

    score: list
    date: list


class Mil:
    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Mil : 종목코드 ({code})")

        self.c101 = myredis.C101(code)
        self.c103 = myredis.C103(code, 'c103현금흐름표q')
        self.c104 = myredis.C104(code, 'c104q')
        self.c106 = myredis.C106(code, 'c106q')

        self.name = self.c101.get_name()
        self._code = code

    def __str__(self):
        return f"Mil({self.code}/{self.name})"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Mil : 종목코드 변경({self.code} -> {code})")

        self.c101.code = code
        self.c103.code = code
        self.c104.code = code
        self.c106.code = code

        self.name = self.c101.get_name()
        self._code = code

    def get_marketcap억(self, refresh: bool) -> float:
        """
        시가총액(억원) 반환
        :return:
        """
        c101r = self.c101.get_recent(refresh)
        시가총액 = int(utils.to_int(c101r.get('시가총액', math.nan)) / 100000000)
        eval_logger.debug(f"시가총액: {시가총액}억원")
        return 시가총액

    def _calc주주수익률(self, 시가총액_억: float, refresh: bool) -> Tuple[str, float, float]:
        self.c103.page = 'c103현금흐름표q'
        d, 재무활동현금흐름 = self.c103.sum_recent_4q('재무활동으로인한현금흐름', refresh)
        try:
            주주수익률 = round((재무활동현금흐름 / 시가총액_억 * -100), 2)
        except ZeroDivisionError:
            주주수익률 = math.nan
            eval_logger.warning(f'{self} 주주수익률: {주주수익률} 재무활동현금흐름: {재무활동현금흐름}')
        return d, 주주수익률, 재무활동현금흐름

    def _calc이익지표(self, 시가총액_억: float, refresh: bool) -> Tuple[str, float, float, float]:
        d1, 지배주주당기순이익 = Tools.calc당기순이익(self.c103, refresh)
        self.c103.page = 'c103현금흐름표q'
        d2, 영업활동현금흐름 = self.c103.sum_recent_4q('영업활동으로인한현금흐름', refresh)
        try:
            이익지표 = round(((지배주주당기순이익 - 영업활동현금흐름) / 시가총액_억) * 100, 2)
        except ZeroDivisionError:
            이익지표 = math.nan
            eval_logger.warning(f'{self} 이익지표: {이익지표} 영업활동현금흐름: {영업활동현금흐름} 지배주주당기순이익: {지배주주당기순이익}')
        try:
            date, *_ = Tools.date_set(d1, d2)
        except ValueError:
            # 날짜 데이터가 없는경우
            date = ''
        return date , 이익지표, 영업활동현금흐름, 지배주주당기순이익

    def _calc투자수익률(self, refresh: bool) -> tuple:
        self.c104.page = 'c104q'
        self.c106.page = 'c106q'
        d1, roic_r = self.c104.sum_recent_4q('ROIC', refresh)
        _, roic_dict = self.c104.find('ROIC', remove_yoy=True, del_unnamed_key=True, refresh=refresh)
        d2, roe_r = self.c104.latest_value_pop2('ROE', refresh)
        roe106 = self.c106.find('ROE', refresh)
        d3, roa_r = self.c104.latest_value_pop2('ROA', refresh)

        try:
            date, *_ = Tools.date_set(d1, d2, d3)
        except ValueError:
            # 날짜 데이터가 없는경우
            date = ''

        return date, roic_r, roic_dict, roe_r, roe106, roa_r

    def _calcFCF(self, refresh: bool) -> dict:
        """
        FCF 계산
        Returns:
            dict: 계산된 fcf 딕셔너리 또는 영업현금흐름 없는 경우 - {}

        Note:
            CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.\n

        """
        self.c103.page = 'c103현금흐름표y'
        _, 영업활동현금흐름_dict = self.c103.find('영업활동으로인한현금흐름', remove_yoy=True, del_unnamed_key=True, refresh=refresh)

        self.c103.page = 'c103재무상태표y'
        _, capex = self.c103.find('*CAPEX', remove_yoy=True, del_unnamed_key=True, refresh=refresh)

        eval_logger.debug(f'영업활동현금흐름 {영업활동현금흐름_dict}')
        eval_logger.debug(f'CAPEX {capex}')

        if len(영업활동현금흐름_dict) == 0:
            return {}

        if len(capex) == 0:
            # CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.
            eval_logger.warning(f"{self} - CAPEX가 없는 업종으로 영업현금흐름을 그대로 사용합니다..")
            return 영업활동현금흐름_dict

        # 영업 활동으로 인한 현금 흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 리턴값으로 fcf 딕셔너리를 반환한다.
        fcf_dict = {}
        for i in range(len(영업활동현금흐름_dict)):
            # 영업활동현금흐름에서 아이템을 하나씩 꺼내서 CAPEX 전체와 비교하여 같으면 차를 구해서 fcf_dict 에 추가한다.
            영업활동현금흐름date, 영업활동현금흐름value = 영업활동현금흐름_dict.popitem()
            # 해당 연도의 capex 가 없는 경우도 있어 일단 capex를 0으로 치고 먼저 추가한다.
            fcf_dict[영업활동현금흐름date] = 영업활동현금흐름value
            for CAPEXdate, CAPEXvalue in capex.items():
                if 영업활동현금흐름date == CAPEXdate:
                    fcf_dict[영업활동현금흐름date] = round(영업활동현금흐름value - CAPEXvalue, 2)

        eval_logger.debug(f'fcf_dict {fcf_dict}')
        # 연도순으로 정렬해서 딕셔너리로 반환한다.
        return dict(sorted(fcf_dict.items(), reverse=False))

    def _calcPFCF(self, 시가총액_억: float, fcf_dict: dict) -> dict:
        """Price to Free Cash Flow Ratio(주가 대비 자유 현금 흐름 비율)계산

            PFCF = 시가총액 / FCF

            Note:
                https://www.investopedia.com/terms/p/pricetofreecashflow.asp
            """
        if math.isnan(시가총액_억):
            eval_logger.warning(f"{self} - 시가총액이 nan으로 pFCF를 계산할수 없습니다.")
            return {}

        # pfcf 계산
        pfcf_dict = {}
        for FCFdate, FCFvalue in fcf_dict.items():
            if FCFvalue == 0:
                pfcf_dict[FCFdate] = math.nan
            else:
                pfcf_dict[FCFdate] = round(시가총액_억 / FCFvalue, 2)

        pfcf_dict = mymongo.C1034.del_unnamed_key(pfcf_dict)

        eval_logger.debug(f'pfcf_dict : {pfcf_dict}')
        return pfcf_dict

    def _calc가치지표(self, 시가총액_억: float, refresh: bool) -> tuple:
        self.c104.page = 'c104q'

        fcf_dict = self._calcFCF(refresh)
        pfcf_dict = self._calcPFCF(시가총액_억, fcf_dict)

        d, pcr_dict = self.c104.find('PCR', remove_yoy=True, del_unnamed_key=True, refresh=refresh)
        return d, fcf_dict, pfcf_dict, pcr_dict

    def _score(self) -> list:
        return [0,]

    def _generate_data(self, refresh: bool) -> MilData:
        eval_logger.info(f"In generate_data..refresh : {refresh}")
        시가총액_억 = self.get_marketcap억(refresh)
        eval_logger.info(f"{self} 시가총액(억) : {시가총액_억}")

        d1, 주주수익률, 재무활동현금흐름 = self._calc주주수익률(시가총액_억, refresh)
        eval_logger.info(f"{self} 주주수익률 : {주주수익률}, {d1}")

        d2, 이익지표, 영업활동현금흐름, 지배주주당기순이익 = self._calc이익지표(시가총액_억, refresh)
        eval_logger.info(f"{self} 이익지표 : {이익지표}, {d2}")

        d3, roic_r, roic_dict, roe_r, roe106, roa_r = self._calc투자수익률(refresh)
        d4, fcf_dict, pfcf_dict, pcr_dict = self._calc가치지표(시가총액_억, refresh)

        score = self._score()

        try:
            date_list = Tools.date_set(d1, d2, d3, d4)
        except ValueError:
            # 날짜 데이터가 없는경우
            date_list = ['',]

        return MilData(
            code= self.code,
            name= self.name,

            시가총액억= 시가총액_억,

            주주수익률= 주주수익률,
            재무활동현금흐름= 재무활동현금흐름,

            이익지표= 이익지표,
            영업활동현금흐름= 영업활동현금흐름,
            지배주주당기순이익= 지배주주당기순이익,

            roic_r= roic_r,
            roic_dict= roic_dict,
            roe_r= roe_r,
            roe_106= roe106,
            roa_r= roa_r,

            fcf_dict= fcf_dict,
            pfcf_dict= pfcf_dict,
            pcr_dict= pcr_dict,

            score= score,
            date = date_list,
        )

    def get(self, refresh = False, verbose = True) -> MilData:
        """
        MilData 형식의 데이터를 계산하여 리턴하고 레디스 캐시에 저장한다.
        :param refresh:
        :return:
        """
        redis_name = f"{self.code}_mil"
        eval_logger.info(f"{self} MilData를 레디스캐시에서 가져오거나 새로 생성합니다.. refresh : {refresh}")
        if verbose:
            print(f"{self} redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_generate_data(refresh_in: bool) -> dict:
            return asdict(self._generate_data(refresh_in))

        return MilData(**myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_generate_data, refresh, timer=expire_time))


@dataclass()
class BlueData:
    code: str
    name: str

    유동비율: float

    이자보상배율_r: float
    이자보상배율_dict: dict

    순운전자본회전율_r: float
    순운전자본회전율_dict: dict

    재고자산회전율_r: float
    재고자산회전율_dict: dict
    재고자산회전율_c106: dict

    순부채비율_r: float
    순부채비율_dict: dict

    score: list
    date: list


class Blue:
    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Blue : 종목코드 ({code})")

        self.c101 = myredis.C101(code)
        self.c103 = myredis.C103(code, 'c103재무상태표q')
        self.c104 = myredis.C104(code, 'c104q')
        
        self.name = self.c101.get_name()
        self._code = code

    def __str__(self):
        return f"Blue({self.code}/{self.name})"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Blue : 종목코드 변경({self.code} -> {code})")

        self.c101.code = code
        self.c103.code = code
        self.c104.code = code

        self.name = self.c101.get_name()
        self._code = code

    def _calc유동비율(self, pop_count: int, refresh: bool) -> Tuple[str, float]:
        """유동비율계산 - Blue에서 사용

        c104q에서 최근유동비율 찾아보고 유효하지 않거나 \n
        100이하인 경우에는수동으로 계산해서 다시 한번 평가해 본다.\n
        """
        eval_logger.info(f'In the calc유동비율... refresh : {refresh}')
        self.c104.page = 'c104q'

        유동비율date, 유동비율value = self.c104.latest_value('유동비율', pop_count=pop_count)
        eval_logger.info(f'{self} 유동비율 : {유동비율value}/({유동비율date})')

        if math.isnan(유동비율value) or 유동비율value < 100:
            유동자산date, 유동자산value = Tools.calc유동자산(self.c103, refresh)
            유동부채date, 유동부채value = Tools.calc유동부채(self.c103, refresh)

            self.c103.page = 'c103현금흐름표q'
            추정영업현금흐름date, 추정영업현금흐름value = self.c103.sum_recent_4q('영업활동으로인한현금흐름', refresh)
            eval_logger.debug(f'{self} 계산전 유동비율 : {유동비율value} / ({유동비율date})')

            계산된유동비율 = 0
            try:
                계산된유동비율 = round(((유동자산value + 추정영업현금흐름value) / 유동부채value) * 100, 2)
            except ZeroDivisionError:
                eval_logger.info(f'유동자산: {유동자산value} + 추정영업현금흐름: {추정영업현금흐름value} / 유동부채: {유동부채value}')
                계산된유동비율 = float('inf')
            finally:
                eval_logger.debug(f'{self} 계산된 유동비율 : {계산된유동비율}')

                try:
                    date, *_ = Tools.date_set(유동자산date, 유동부채date, 추정영업현금흐름date)
                except ValueError:
                    # 날짜 데이터가 없는경우
                    date = ''
                eval_logger.warning(f'{self} 유동비율 이상(100 이하 또는 nan) : {유동비율value} -> 재계산 : {계산된유동비율}')
                return date, 계산된유동비율
        else:
            return 유동비율date, 유동비율value

    def _score(self) -> list:
        return [0,]

    def _generate_data(self, refresh: bool) -> BlueData:
        d1, 유동비율 = self._calc유동비율(pop_count=3, refresh=refresh)
        eval_logger.info(f'유동비율 {유동비율} / [{d1}]')

        재고자산회전율_c106 = myredis.C106.make_like_c106(self.code, 'c104q', '재고자산회전율', refresh)

        self.c104.page = 'c104y'
        _, 이자보상배율_dict = self.c104.find('이자보상배율', remove_yoy=True, refresh=refresh)
        _, 순운전자본회전율_dict = self.c104.find('순운전자본회전율', remove_yoy=True, refresh=refresh)
        _, 재고자산회전율_dict = self.c104.find('재고자산회전율', remove_yoy=True, refresh=refresh)
        _, 순부채비율_dict = self.c104.find('순부채비율', remove_yoy=True, refresh=refresh)

        self.c104.page = 'c104q'
        d6, 이자보상배율_r = self.c104.latest_value_pop2('이자보상배율', refresh)
        d7, 순운전자본회전율_r = self.c104.latest_value_pop2('순운전자본회전율', refresh)
        d8, 재고자산회전율_r = self.c104.latest_value_pop2('재고자산회전율', refresh)
        d9, 순부채비율_r = self.c104.latest_value_pop2('순부채비율', refresh)

        if len(이자보상배율_dict) == 0:
            eval_logger.warning(f'empty dict - 이자보상배율 : {이자보상배율_r} / {이자보상배율_dict}')

        if len(순운전자본회전율_dict) == 0:
            eval_logger.warning(f'empty dict - 순운전자본회전율 : {순운전자본회전율_r} / {순운전자본회전율_dict}')

        if len(재고자산회전율_dict) == 0:
            eval_logger.warning(f'empty dict - 재고자산회전율 : {재고자산회전율_r} / {재고자산회전율_dict}')

        if len(순부채비율_dict) == 0:
            eval_logger.warning(f'empty dict - 순부채비율 : {순부채비율_r} / {순부채비율_dict}')

        score = self._score()

        try:
            date_list = Tools.date_set(d1, d6, d7, d8, d9)
        except ValueError:
            # 날짜 데이터가 없는경우
            date_list = ['',]

        return BlueData(
            code= self.code,
            name= self.name,
            유동비율= 유동비율,
            이자보상배율_r= 이자보상배율_r,
            이자보상배율_dict= 이자보상배율_dict,

            순운전자본회전율_r= 순운전자본회전율_r,
            순운전자본회전율_dict= 순운전자본회전율_dict,

            재고자산회전율_r= 재고자산회전율_r,
            재고자산회전율_dict= 재고자산회전율_dict,
            재고자산회전율_c106= 재고자산회전율_c106,

            순부채비율_r= 순부채비율_r,
            순부채비율_dict= 순부채비율_dict,

            score= score,
            date= date_list,
        )

    def get(self, refresh = False, verbose = True) -> BlueData:
        """
        BlueData 형식의 데이터를 계산하여 리턴하고 레디스 캐시에 저장한다.
        :param refresh:
        :return:
        """
        redis_name = f"{self.code}_blue"
        eval_logger.info(f"{self} BlueData를 레디스캐시에서 가져오거나 새로 생성합니다.. refresh : {refresh}")
        if verbose:
            print(f"{self} redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_generate_data(refresh_in: bool) -> dict:
            return asdict(self._generate_data(refresh_in))

        return BlueData(**myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_generate_data, refresh, timer=expire_time))



@dataclass()
class GrowthData:
    code: str
    name: str

    매출액증가율_r: float
    매출액증가율_dict: dict

    영업이익률_c106: dict

    score: list
    date: list


class Growth:
    def __init__(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Growth : 종목코드 ({code})")

        self.c101 = myredis.C101(code)
        self.c104 = myredis.C104(code, 'c104q')
        self.c106 = myredis.C106(code, 'c106q')

        self.name = self.c101.get_name()
        self._code = code

    def __str__(self):
        return f"Growth({self.code}/{self.name})"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        eval_logger.debug(f"Growth : 종목코드 변경({self.code} -> {code})")

        self.c101.code = code
        self.c104.code = code
        self.c106.code = code

        self.name = self.c101.get_name()
        self._code = code

    def _score(self) -> list:
        return [0,]

    def _generate_data(self, refresh=False) -> GrowthData:
        self.c104.page = 'c104y'
        _, 매출액증가율_dict = self.c104.find('매출액증가율', remove_yoy=True, refresh=refresh)

        self.c104.page = 'c104q'
        d2, 매출액증가율_r = self.c104.latest_value_pop2('매출액증가율')

        eval_logger.info(f'매출액증가율 : {매출액증가율_r} {매출액증가율_dict}')

        # c106 에서 타 기업과 영업이익률 비교
        self.c106.page = 'c106y'
        영업이익률_c106 = self.c106.find('영업이익률', refresh)

        score = self._score()

        try:
            date_list = Tools.date_set(d2)
        except ValueError:
            # 날짜 데이터가 없는경우
            date_list = ['', ]

        return GrowthData(
            code= self.code,
            name= self.name,

            매출액증가율_r= 매출액증가율_r,
            매출액증가율_dict= 매출액증가율_dict,

            영업이익률_c106= 영업이익률_c106,

            score= score,
            date= date_list,
        )

    def get(self, refresh = False, verbose = True) -> GrowthData:
        """
        GrowthData 형식의 데이터를 계산하여 리턴하고 레디스 캐시에 저장한다.
        :param refresh:
        :return:
        """
        redis_name = f"{self.code}_growth"
        eval_logger.info(f"{self} GrowthData를 레디스캐시에서 가져오거나 새로 생성합니다.. refresh : {refresh}")
        if verbose:
            print(f"{self} redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time/3600}h")

        def fetch_generate_data(refresh_in: bool) -> dict:
            return asdict(self._generate_data(refresh_in))

        return GrowthData(**myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_generate_data, refresh, timer=expire_time))




"""
- 각분기의 합이 연이 아닌 타이틀(즉 sum_4q를 사용하면 안됨)
'*(지배)당기순이익'
'*(비지배)당기순이익'
'장기차입금'
'현금및예치금'
'매도가능금융자산'
'매도파생결합증권'
'만기보유금융자산'
'당기손익-공정가치측정금융부채'
'당기손익인식(지정)금융부채'
'단기매매금융자산'
'단기매매금융부채'
'예수부채'
'차입부채'
'기타부채'
'보험계약부채(책임준비금)'
'*CAPEX'
'ROE'
"""

"""
- sum_4q를 사용해도 되는 타이틀
'자산총계'
'당기순이익'
'유동자산'
'유동부채'
'비유동부채'

'영업활동으로인한현금흐름'
'재무활동으로인한현금흐름'
'ROIC'
"""
