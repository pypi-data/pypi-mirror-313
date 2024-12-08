import math
import numpy
import pprint
import copy
from typing import Tuple

from db_hj3415 import myredis, mymongo
from utils_hj3415 import utils

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)



def mil(code: str, expect_earn: float) -> Tuple[int, int, int, int]:
    """
    이익 지표 일반적인 기준 설정

	1.	비율이 10% 이상일 경우 주의:
	•	이 비율이 10%를 넘을 경우, 이는 기업의 순이익이 현금 흐름과 비교하여 너무 높아졌음을 나타냅니다.
	•	순이익이 과도하게 부풀려졌을 가능성이 있으며, 회계적인 항목(예: 미수금, 재고자산의 평가차익 등)이나 비현금성 이익이 이익에 크게 기여하고 있을 수 있습니다. 이런 경우, 현금 흐름이 제대로 발생하지 않고 있음에도 순이익만 높게 기록되는 상황이 발생할 수 있어 이익의 질이 낮다고 평가됩니다.
	•	특히, 비율이 지속적으로 높다면 재무 건전성에 문제가 있을 수 있습니다.
	2.	비율이 5% 이상 ~ 10% 미만일 때:
	•	비율이 5% ~ 10% 사이라면, 기업의 이익이 여전히 현금 흐름과 괴리가 있지만, 업종에 따라 일정 부분은 허용될 수 있습니다.
	•	예를 들어, 기술 기업이나 고성장 산업에서는 초기 투자나 R&D 비용이 많기 때문에 순이익과 현금 흐름의 차이가 다소 발생할 수 있습니다. 이런 경우 비율이 5%를 넘더라도 성장성을 고려한 투자 관점에서 용인될 수 있습니다.
	•	다만, 일반적인 제조업 등 현금 창출이 중요한 업종에서는 5% 이상의 괴리도 주의 깊게 볼 필요가 있습니다.
	3.	비율이 5% 미만일 때:
	•	비율이 5% 미만이라면, 기업의 순이익과 현금 흐름 간의 차이가 크지 않으므로, 이익의 질이 높고 재무 건전성이 양호하다고 평가할 수 있습니다.
	•	특히 음수일 경우, 영업활동에서 벌어들인 현금이 순이익을 초과한다는 것을 의미하므로, 이는 매우 긍정적인 신호입니다. 기업이 순이익보다도 더 많은 현금을 창출하고 있는 상태로, 이익이 실제 현금 흐름으로 뒷받침되고 있음을 나타냅니다.

	참고할 수 있는 기준
    1. 경고 신호: 10% 이상
	•	비율이 10% 이상이라면, 기업의 이익이 실제 현금 흐름과 크게 괴리되어 있음을 의미하며, 이익의 질이 낮고 재무 건전성이 떨어질 가능성이 큽니다. 특히, 이 비율이 지속적으로 높다면, 주의가 필요합니다.
    2. 주의: 5% ~ 10%
	•	이 비율은 어느 정도 괴리가 있는 상태이며, 업종 특성에 따라 감안할 수 있지만, 일반적인 기업의 경우 주의를 요합니다.
    3. 안정적: 5% 미만
	•	5% 미만은 비교적 안정적인 상태로 평가될 수 있습니다. 이익과 현금 흐름 간의 괴리가 크지 않기 때문에, 기업의 재무 상태와 이익의 질이 건전하다고 볼 수 있습니다.
    4. 매우 긍정적: 음수
	•	비율이 음수일 경우, 현금 창출 능력이 매우 우수한 상태입니다. 현금 흐름이 순이익보다 더 크므로, 이는 매우 긍정적인 신호로 평가됩니다.

    사례별 해석

	1.	비율이 15%:
	•	회사는 순이익이 영업활동현금흐름에 비해 과도하게 높습니다. 이는 비현금성 이익이 많이 포함되어 있거나, 회계적인 처리로 인해 순이익이 부풀려졌을 가능성이 큽니다. 기업의 이익 질에 의문을 가져야 하며, 장기적으로 재무 구조에 문제가 생길 수 있습니다.
	2.	비율이 7%:
	•	괴리가 존재하지만, 일부 산업에서는 용인될 수 있는 범위입니다. 다만, 현금 흐름이 안정적인지 추가적인 분석이 필요합니다.
	3.	비율이 -3%:
	•	매우 긍정적인 상황입니다. 회사는 순이익보다 더 많은 현금을 벌어들이고 있어, 이익의 질이 매우 높으며, 주주들에게도 더 많은 이익을 돌려줄 가능성이 큽니다.

    기타 고려 사항

	•	업종별 차이: 기술 기업, 스타트업 등은 고정자산 투자나 R&D 비용이 많아 현금 흐름과 이익이 괴리될 수 있습니다. 이 경우 이익의 질이 낮다고 단정할 수는 없으므로 산업 특성을 고려해야 합니다.
	•	기업의 성장 단계: 빠르게 성장하는 기업일수록 현금 흐름보다 순이익이 클 수 있지만, 시간이 지나면서 현금 창출 능력이 증가할 수 있습니다.
	•	비현금성 항목 분석: 감가상각, 미수금 등의 비현금성 항목이 이익에 얼마나 영향을 미치는지 분석하여 이익의 질을 파악하는 것이 중요합니다.
	ROIC 평가 기준

	1.	10% 이상:
	•	일반적으로 ROIC가 10% 이상이면 매우 우수한 기업으로 평가됩니다.
	•	이는 기업이 투자된 자본으로 높은 수익을 창출하고 있음을 의미하며, 자본의 사용 효율성이 매우 높다는 것을 나타냅니다.
	2.	7% ~ 10%:
	•	ROIC가 7%에서 10% 사이라면, 기업은 자본을 비교적 효율적으로 사용하고 있는 상태입니다.
	•	자본비용(WACC)이 이보다 낮다면, 투자자는 기업이 가치 창출을 하고 있다고 판단할 수 있습니다.
	3.	5% ~ 7%:
	•	이 범위에서는 보통 수준의 효율성을 보여줍니다. ROIC가 자본비용보다 낮지 않다면 투자자에게 긍정적일 수 있지만, 이 수익률이 경쟁사 대비 낮다면 경쟁력이 떨어질 수 있음을 시사할 수 있습니다.
	4.	5% 미만:
	•	ROIC가 5% 미만이라면, 기업은 자본을 비효율적으로 사용하고 있음을 의미할 수 있습니다.
	•	자본을 투입해 수익을 내지 못하거나, 투자된 자본으로부터 적절한 수익을 창출하지 못하고 있는 상태일 수 있습니다.
    :param code:
    :param expect_earn:
    :return:
    """

    mil_dict = eval.mil(code)

    # print(pprint.pformat(mil_dict, width=200))

    # 주주수익률 평가
    if math.isnan(mil_dict['주주수익률']):
        score1 = 0
    else:
        주주수익률평가 = math.ceil(mil_dict['주주수익률'] - (expect_earn * 100))
        score1 = 0 if 0 > 주주수익률평가 else 주주수익률평가

    # 이익지표 평가
    score2 = 10 if mil_dict['이익지표'] < 0 else 0

    # 투자수익률 평가
    MAX3 = 20
    score3 = 0
    roic = mil_dict['투자수익률']['ROIC']
    roe = mil_dict['투자수익률']['ROE']
    if math.isnan(roic) or roic <= 0:
        # roic 가 비정상이라 평가할 수 없는 경우
        if 10 < roe <= 20:
            score3 += round(MAX3 * 0.333)
        elif 20 < roe:
            score3 += round(MAX3 * 0.666)
    elif 0 < roic:
        # roic 로 평가할 수 있는 경우
        if 0 < roic <= 15:
            score3 += round(MAX3 * 0.333)
        elif 15 < roic <= 30:
            score3 += round(MAX3 * 0.666)
        elif 30 < roic:
            score3 += MAX3

    # PFCF 평가
    pfcf_dict = mil_dict['가치지표']['PFCF']
    _, pfcf = mymongo.C1034.latest_dict_value(pfcf_dict)

    logger.debug(f'recent pfcf {_}, {pfcf}')
    try:
        p = round(-40 * math.log10(pfcf) + 40)
    except ValueError:
        p = 0
    score4 = 0 if 0 > p else p

    return score1, score2, score3, score4


def blue(code: str) -> Tuple[int, int, int, int, int]:
    """회사의 안정성을 보는 지표들

    0을 기준으로 상태가 좋치 않을 수록 마이너스 값을 가진다.

    Returns:
        tuple : 유동비율, 이자보상배율, 순부채비율, 순운전자본회전율, 재고자산회전율 평가 포인트

    Notes:
    """
    def _calc_point_with_std(data: dict) -> int:
        """표준편차를 통해 점수를 계산하는 내부 함수

        Args:
            data(dict): 재무재표상의 연/분기 딕셔너리 데이터
        """
        NEG_MAX = -5
        d_values = [i for i in data.values() if not math.isnan(i)]
        logger.debug(f'd_values : {d_values}')
        if len(d_values) == 0:
            p = NEG_MAX
        else:
            std = numpy.std(d_values)
            # 표준편차가 작을수록 데이터의 변환가 적다는 의미임.
            logger.debug(f'표준편차 : {std}')
            p = NEG_MAX if float(std) > -NEG_MAX else -math.floor(float(std))

        return int(p)

    c104y = myredis.C104(code, 'c104y')

    blue_dict = eval.blue(code)

    # print(pprint.pformat(blue_dict, width=200))

    def 유동비율평가(유동비율: float) -> int:
        # 채점은 0을 기준으로 마이너스 해간다. 즉 0이 제일 좋은 상태임.
        # 유동비율 평가 - 100 이하는 문제 있음
        NEG_MAX = -10
        if math.isnan(유동비율) or 유동비율 <= 0:
            p = NEG_MAX
        elif math.isinf(유동비율):
            p = 0
        else:
            p = 0 if 100 < round(유동비율) else NEG_MAX + round(유동비율/10)
        logger.debug(f'유동비율평가 point : {p}')
        return int(p)

    p1 = 유동비율평가(blue_dict['유동비율'])

    def 이자보상배율평가(이자보상배율: tuple) -> int:
        # 이자보상배율평가 : 1이면 자금사정 빡빡 5이상이면 양호
        NEG_MAX = -5
        최근이자보상배율q, dict_y = 이자보상배율

        if math.isnan(최근이자보상배율q) or 최근이자보상배율q <= 1:
            # 최근 분기의 값이 비정상이면 최근 년도를 한번 더 비교해 보지만 좀더 엄격하게 전년대비도 비교한다.

            _, 최근이자보상배율y = mymongo.C1034.latest_dict_value(dict_y)
            c104y.page = 'c104y'
            전년대비 = c104y.find_yoy(title='이자보상배율')

            if math.isnan(최근이자보상배율y) or 최근이자보상배율y <= 1 or math.isnan(전년대비) or 전년대비 < 0:
                p = NEG_MAX
            else:
                p = 0 if 5 < 최근이자보상배율y else NEG_MAX + round(최근이자보상배율y)
        else:
            p = 0 if 5 < 최근이자보상배율q else NEG_MAX + round(최근이자보상배율q)
        logger.debug(f'이자보상배율평가 point : {p}')
        return int(p)

    p2 = 이자보상배율평가(blue_dict['이자보상배율'])

    def 순부채비율평가(순부채비율: tuple) -> int:
        # 부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
        # 순부채 비율이 30%이상이면 좋치 않다.
        NEG_MAX = -5
        최근순부채비율q, dict_y = 순부채비율

        if math.isnan(최근순부채비율q) or 최근순부채비율q >= 80:
            # 최근 분기의 값이 비정상이면 최근 년도를 한번 더 비교해 보지만 좀더 엄격하게 전년대비도 비교한다.
            _, 최근순부채비율y = mymongo.C1034.latest_dict_value(dict_y)
            c104y.page = 'c104y'
            전년대비 = c104y.find_yoy(title='순부채비율')
            if math.isnan(최근순부채비율y) or 최근순부채비율y >= 80 or math.isnan(전년대비) or 전년대비 > 0:
                p = NEG_MAX
            else:
                p = 0 if 최근순부채비율y < 30 else round((30 - 최근순부채비율y) / 10)
        else:
            p = 0 if 최근순부채비율q < 30 else round((30 - 최근순부채비율q) / 10)
        logger.debug(f'순부채비율평가 point : {p}')
        return int(p)

    p3 = 순부채비율평가(blue_dict['순부채비율'])

    def 순운전자본회전율평가(순운전자본회전율: tuple) -> int:
        # 순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
        _, dict_y = 순운전자본회전율
        p = _calc_point_with_std(data=dict_y)
        logger.debug(f'순운전자본회전율평가 point : {p}')
        return p

    p4 = 순운전자본회전율평가(blue_dict['순운전자본회전율'])

    def 재고자산회전율평가(재고자산회전율: tuple) -> int:
        # 재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
        # 재고자산회전율이 작아지면 재고가 쌓인다는뜻
        _, dict_y = 재고자산회전율
        p = _calc_point_with_std(data=dict_y)
        # 라이벌기업과 비교점수 추가
        logger.debug(f'재고자산회전율평가 point : {p}')
        return p

    p5 = 재고자산회전율평가(blue_dict['재고자산회전율'])

    return p1, p2, p3, p4, p5


def growth(code: str) -> Tuple[int, int]:
    """회사의 성장성을 보는 지표들

    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈

    Returns:
        tuple : 매출액증가율, 영업이익률 평가 포인트
    """
    growth_dict = eval.growth(code)

    logger.debug(pprint.pformat(growth_dict, width=200))

    def 매출액증가율평가(매출액증가율: tuple) -> int:
        # 매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
        MAX = 20
        최근매출액증가율q, dict_y = 매출액증가율
        _, 최근매출액증가율y = mymongo.C1034.latest_dict_value(dict_y)

        # 최근 자료가 성장하는 중인지 판단
        if math.isnan(최근매출액증가율q):
            최근매출액증가율q = 최근매출액증가율y

        sp1 = 0
        if math.isnan(최근매출액증가율y):
            pass
        elif 0 < 최근매출액증가율y and 0 < 최근매출액증가율q:
            # 최근에 마이너스 성장이 아닌경우 MAX/10점 보너스
            sp1 += MAX / 10
            if 최근매출액증가율y < 최근매출액증가율q:
                # 최근에 이전보다 더 성장중이면 MAX/10점 보너스
                sp1 += MAX / 10
            # 나머지는 성장률 기반 점수 배정
            sp1 += MAX / 2 if 최근매출액증가율q > MAX else 최근매출액증가율q / 2
        elif 최근매출액증가율y <= 0 < 최근매출액증가율q:
            # 직전에 마이너스였다가 최근에 회복된 경우 MAX/10점 보너스
            sp1 += MAX / 10
            # 나머지는 성장률 기반 점수 배정
            sp1 += MAX / 2 if 최근매출액증가율q > MAX else 최근매출액증가율q / 2
        else:
            # 최근 자료가 마이너스인 경우 마이너스만큼 점수를 차감한다.
            sp1 += -(MAX / 2) if 최근매출액증가율q < -MAX else 최근매출액증가율q / 2

        # 평균매출액증가율 구하기
        d_values = [i for i in dict_y.values() if not math.isnan(i)]
        logger.debug(f'평균매출액증가율 d_values : {d_values}')

        if len(d_values) == 0:
            평균매출액증가율 = float('nan')
        else:
            평균매출액증가율 = float(numpy.mean(d_values))
        logger.debug(f'평균 : {평균매출액증가율}')

        sp2 = 0
        if math.isnan(평균매출액증가율):
            sp2 += -(MAX/2)
        elif 평균매출액증가율 <= 0:
            # 평균매출액증가율이 마이너스인 경우 마이너스만큼 점수를 차감한다.
            sp2 += -(MAX / 2) if 평균매출액증가율 < -MAX else 평균매출액증가율 / 2
        else:
            sp2 = MAX / 2 if 평균매출액증가율 > MAX else 평균매출액증가율 / 2

        logger.debug(f'매출액증가율평가 point : {sp1 + sp2}')

        return int(sp1 + sp2)

    p1 = 매출액증가율평가(growth_dict['매출액증가율'])

    def 영업이익률평가(영업이익률: dict) -> int:
        # 영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
        영업이익률 = copy.deepcopy(영업이익률)
        name = myredis.Corps.get_name(code)

        p = 0
        try:
            myprofit = utils.to_float(영업이익률.pop(name))
        except KeyError:
            logger.warning(f'{name} 영업이익률 does not exist.')
            return 0
        logger.debug(f'종목영업이익률 : {myprofit}')

        for profit in 영업이익률.values():
            profit = utils.to_float(profit)
            if math.isnan(profit):
                continue
            elif myprofit > profit:
                p += 1
            else:
                continue

        logger.debug(f'영업이익률평가 point : {p}')
        return p

    p2 = 영업이익률평가(growth_dict['영업이익률'])

    return p1, p2
