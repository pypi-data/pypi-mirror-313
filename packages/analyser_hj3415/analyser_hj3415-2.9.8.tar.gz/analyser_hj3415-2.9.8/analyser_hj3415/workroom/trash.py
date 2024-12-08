

def _make_df_part(db_addr, codes: list, q):
    def make_record(my_client, my_code: str) -> dict:
        # 장고에서 사용할 eval 테이블을 만들기 위해 각각의 레코드를 구성하는 함수
        c101 = mongo.C101(my_client, my_code).get_recent()

        red_dict = red(my_client, my_code)
        mil_dict = mil(my_client, my_code)
        growth_dict = growth(my_client, my_code)

        mil_date = mil_dict['date']
        red_date = red_dict['date']
        growth_date = growth_dict['date']

        return {
            'code': c101['코드'],
            '종목명': c101['종목명'],
            '주가': utils.to_int(c101['주가']),
            'PER': utils.to_float(c101['PER']),
            'PBR': utils.to_float(c101['PBR']),
            '시가총액': utils.to_float(c101['시가총액']),
            'RED': utils.to_int(red_dict['red_price']),
            '주주수익률': utils.to_float(mil_dict['주주수익률']),
            '이익지표': utils.to_float(mil_dict['이익지표']),
            'ROIC': utils.to_float(mil_dict['투자수익률']['ROIC']),
            'ROE': utils.to_float(mil_dict['투자수익률']['ROE']),
            'PFCF': utils.to_float(mongo.Corps.latest_value(mil_dict['가치지표']['PFCF'])[1]),
            'PCR': utils.to_float(mongo.Corps.latest_value(mil_dict['가치지표']['PCR'])[1]),
            '매출액증가율': utils.to_float(growth_dict['매출액증가율'][0]),
            'date': list(set(mil_date + red_date + growth_date))
        }
    # 각 코어별로 디비 클라이언트를 만들어야만 한다. 안그러면 에러발생
    client = mongo.connect_mongo(db_addr)
    t = len(codes)
    d = []
    for i, code in enumerate(codes):
        print(f'{i+1}/{t} {code}')
        try:
            d.append(make_record(client, code))
        except:
            logger.error(f'error on {code}')
            continue
    df = pd.DataFrame(d)
    logger.info(df)
    q.put(df)


def make_today_eval_df(client, refresh: bool = False) -> pd.DataFrame:
    """ 멀티프로세싱을 사용하여 전체 종목의 eval 을 데이터프레임으로 만들어 반환

    기본값으로 refresh 는 False 로 설정되어 당일자의 저장된 데이터프레임이 있으면 새로 생성하지 않고 mongo DB를 이용한다.
    """
    today_str = datetime.datetime.today().strftime('%Y%m%d')
    df = mongo.EvalByDate(client, today_str).load_df()
    if refresh or len(df) == 0:
        codes_in_db = mongo.Corps.get_all_codes(client)

        print('*' * 25, f"Eval all using multiprocess(refresh={refresh})", '*' * 25)
        print(f'Total {len(codes_in_db)} items..')
        logger.debug(codes_in_db)
        n, divided_list = utils.code_divider_by_cpu_core(codes_in_db)

        addr = mongo.extract_addr_from_client(client)

        start_time = time.time()
        q = Queue()
        ths = []
        for i in range(n):
            ths.append(Process(target=_make_df_part, args=(addr, divided_list[i], q)))
        for i in range(n):
            ths[i].start()

        df_list = []
        for i in range(n):
            df_list.append(q.get())
        # 부분데이터프레임들을 하나로 합침
        final_df = pd.concat(df_list, ignore_index=True)

        for i in range(n):
            ths[i].join()

        print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')
        logger.debug(final_df)
        print(f"Save to mongo db(db: eval col: {today_str})")
        mongo.EvalByDate(client, today_str).save_df(final_df)
    else:
        print(f"Use saved dataframe from mongo db..")
        final_df = df
    return final_df


def yield_valid_spac(client) -> tuple:
    """
    전체 스팩주의 현재가를 평가하여 2000원 이하인 경우 yield한다.

    Returns:
        tuple: (code, name, price)
    """
    codes = mongo.Corps.get_all_codes(client)
    logger.debug(f'len(codes) : {len(codes)}')
    print('<<< Finding valuable SPAC >>>')
    for i, code in enumerate(codes):
        name = mongo.Corps.get_name(client, code)
        logger.debug(f'code : {code} name : {name}')
        if '스팩' in str(name):
            logger.debug(f'>>> spac - code : {code} name : {name}')
            price, _, _ = utils.get_price_now(code=code)
            if price <= 2000:
                logger.warning(f'현재가:{price}')
                print(f"code: {code} name: {name}, price: {price}")
                yield code, name, price



class GetDFTest(unittest.TestCase):
    def test_make_df_part(self):
        codes = ['025320', '000040', '060280', '003240']
        from multiprocessing import Queue
        q = Queue()
        eval._make_df_part(addr, codes, q)

    def test_get_df(self):
        print(eval.make_today_eval_df(client, refresh=True))
        print(eval.make_today_eval_df(client, refresh=False))


class SpacTest(unittest.TestCase):
    def test_valid_spac(self):
        for code, name, price in eval.yield_valid_spac(client):
            print(code, name, price)




def mil(code: str) -> Tuple[int, int, int, int]:
    """
    - 재무활동현금흐름이 마이너스라는 것은 배당급 지급했거나, 자사주 매입했거나, 부채를 상환한 상태임.
    - 반대는 채권자로 자금을 조달했거나 신주를 발행했다는 의미
    <주주수익률> - 재무활동현금흐름/시가총액 => 5%이상인가?

    투하자본수익률(ROIC)가 30%이상인가
    ROE(자기자본이익률) 20%이상이면 아주 우수 다른 투자이익률과 비교해볼것 10%미만이면 별로...단, 부채비율을 확인해야함.

    이익지표 ...영업현금흐름이 순이익보다 많은가 - 결과값이 음수인가..

    FCF는 영업현금흐름에서 자본적 지출(유·무형투자 비용)을 차감한 순수한 현금력이라 할 수 있다.
    말 그대로 자유롭게(Free) 사용할 수 있는 여윳돈을 뜻한다.
    잉여현금흐름이 플러스라면 미래의 투자나 채무상환에 쓸 재원이 늘어난 것이다.
    CAPEX(Capital expenditures)는 미래의 이윤을 창출하기 위해 지출된 비용을 말한다.
    이는 기업이 고정자산을 구매하거나, 유효수명이 당회계년도를 초과하는 기존의 고정자산에 대한 투자에 돈이 사용될 때 발생한다.

    잉여현금흐름이 마이너스일때는 설비투자가 많은 시기라 주가가 약세이며 이후 설비투자 마무리되면서 주가가 상승할수 있다.
    주가는 잉여현금흐름이 증가할때 상승하는 경향이 있다.
    fcf = 영업현금흐름 - capex

    가치지표평가
    price to fcf 계산
    https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    pcr보다 정확하게 주식의 가치를 평가할수 있음. 10배이하 추천

    Returns:
        tuple: 주주수익률, 이익지표, 투자수익률, PFCF포인트
    """
    mil_dict = eval.mil(code)

    print(pprint.pformat(mil_dict, width=200))

    # 주주수익률 평가
    if math.isnan(mil_dict['주주수익률']):
        score1 = 0
    else:
        주주수익률평가 = math.ceil(mil_dict['주주수익률'] - (eval.EXPECT_EARN * 100))
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
    _, pfcf = mongo.Corps.latest_value(pfcf_dict)

    logger.debug(f'recent pfcf {_}, {pfcf}')
    try:
        p = round(-40 * math.log10(pfcf) + 40)
    except ValueError:
        p = 0
    score4 = 0 if 0 > p else p

    return score1, score2, score3, score4




def dbmanager():
    cmd = ['repair', 'sync', 'eval', 'update']
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help=f"Command - {cmd}")
    parser.add_argument('target', help="Target for scraping (type 6digit code or 'all' or 'parts')")
    parser.add_argument('-d', '--db_path', help="Set mongo database path")

    args = parser.parse_args()

    db_path = args.db_path if args.db_path else "mongodb://192.168.0.173:27017"
    client = mongo.connect_mongo(db_path)

    if args.cmd in cmd:
        if args.cmd == 'repair':
            if args.target == 'all' or utils.is_6digit(args.target):
                need_for_repair_codes = chk_db.chk_integrity_corps(client, args.target)
                # repair dict 예시 - {'343510': ['c106', 'c104', 'c103'], '298000': ['c104'], '091810': ['c104']}
                print(f"Need for repairing codes :{need_for_repair_codes}")
                if need_for_repair_codes:
                    # x = input("Do you want to try to repair db by scraping? (y/N)")
                    # if x == 'y' or x == 'Y':
                        for code, failed_page_list in need_for_repair_codes.items():
                            for page in failed_page_list:
                                if page == 'c101':
                                    nfsrun.c101([code, ], db_path)
                                elif page == 'c103':
                                    nfsrun.c103([code, ], db_path)
                                elif page == 'c104':
                                    nfsrun.c104([code, ], db_path)
                                elif page == 'c106':
                                    nfsrun.c106([code, ], db_path)
                            recheck_result = chk_db.chk_integrity_corps(client, code)
                            if recheck_result:
                                # 다시 스크랩해도 오류가 지속되는 경우
                                print(f"The db integrity failure persists..{recheck_result}")
                                # x = input(f"Do you want to delete {code} on DB? (y/N)")
                                # if x == 'y' or x == 'Y':
                                #    mongo.Corps.del_db(client, code)
                                # else:
                                #    print("Canceled.")
                                mongo.Corps.del_db(client, code)
                    # else:
                    #     print("Done.")
                else:
                    print("Done.")
            else:
                print(f"Invalid target option : {args.target}")
        elif args.cmd == 'update':
            if args.target == 'all' or utils.is_6digit(args.target):
                need_for_update_codes = list(chk_db.chk_modifying_corps(client, args.target).keys())
                # need_for_update_codes 예시 - [codes....]
                print(f"Need for updating codes :{need_for_update_codes}")
                if need_for_update_codes:
                    nfsrun.c103(need_for_update_codes, db_path)
                    nfsrun.c104(need_for_update_codes, db_path)
                    nfsrun.c106(need_for_update_codes, db_path)
            elif args.target == 'parts':
                pass
            else:
                print(f"Invalid target option : {args.target}")
        elif args.cmd == 'sync':
            if args.target == 'all':
                chk_db.sync_mongo_with_krx(client)
            else:
                print(f"The target should be 'all' in sync command.")
        elif args.cmd == 'eval':
            if args.target == 'all':
                # eval을 평가해서 데이터베이스에 저장한다.
                eval.make_today_eval_df(client, refresh=True)
            else:
                print(f"The target should be 'all' in sync command.")
    else:
        print(f"The command should be in {cmd}")

    client.close()
