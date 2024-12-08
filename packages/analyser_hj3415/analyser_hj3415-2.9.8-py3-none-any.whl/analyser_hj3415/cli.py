import argparse
import os
import pprint

from utils_hj3415 import noti, utils
from utils_hj3415.helpers import SettingsManager
from db_hj3415 import myredis


class AnalyserSettingsManager(SettingsManager):
    DEFAULT_SETTINGS = {
        'EXPECT_EARN': 0.06,
        'RED_RANKING_EXPECT_EARN': 0.06,
    }
    TITLES = DEFAULT_SETTINGS.keys()

    def __init__(self):
        settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')
        super().__init__(settings_file)

    def set_value(self, title: str, value: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        self.settings_dict[title] = value
        self.save_settings()
        print(f"{title}: {value}가 저장되었습니다")

    def get_value(self, title: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        return self.settings_dict.get(title, self.DEFAULT_SETTINGS[title])

    def reset_value(self, title: str):
        assert title in self.TITLES, f"title 인자는 {self.TITLES} 중에 있어야 합니다."
        self.set_value(title, self.DEFAULT_SETTINGS[title])
        print(f"{title}이 기본값 ({self.DEFAULT_SETTINGS[title]}) 으로 초기화 되었습니다.")


def analyser_manager():
    settings_manager = AnalyserSettingsManager()
    expect_earn_from_setting = settings_manager.get_value('EXPECT_EARN')

    parser = argparse.ArgumentParser(description="Analyser Commands")
    type_subparsers = parser.add_subparsers(dest='type', help='분석 타입')

    # prophet 명령어 서브파서
    prophet_parser = type_subparsers.add_parser('prophet', help='MyProphet 타입')
    prophet_subparser = prophet_parser.add_subparsers(dest='command', help='prophet 관련된 명령')
    # ranking 파서
    ranking_parser = prophet_subparser.add_parser('ranking', help='prophet 랭킹 책정 및 레디스 저장')
    ranking_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    ranking_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # lstm 명령어 서브파서
    lstm_parser = type_subparsers.add_parser('lstm', help='MyLSTM 타입')
    lstm_subparser = lstm_parser.add_subparsers(dest='command', help='lstm 관련된 명령')
    # caching 파서
    caching_parser = lstm_subparser.add_parser('caching', help='lstm 랭킹 책정 및 레디스 저장')
    caching_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    caching_parser.add_argument('-t', '--top', type=int, help='prophet ranking 몇위까지 작업을 할지')
    caching_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')
    # red - get 파서
    lstm_get_parser = lstm_subparser.add_parser('get', help='lstm get 책정 및 레디스 저장')
    lstm_get_parser.add_argument('code', type=str, help='종목코드')
    lstm_get_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    lstm_get_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # red 명령어 서브파서
    red_parser = type_subparsers.add_parser('red', help='red 타입')
    red_subparser = red_parser.add_subparsers(dest='command', help='red 관련된 명령')
    # red - ranking 파서
    ranking_parser = red_subparser.add_parser('ranking', help='red 랭킹 책정 및 레디스 저장')
    ranking_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    ranking_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    ranking_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')
    # red - get 파서
    red_get_parser = red_subparser.add_parser('get', help='red get 책정 및 레디스 저장')
    red_get_parser.add_argument('code', type=str, help='종목코드 or all')
    red_get_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    red_get_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    red_get_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # mil 명령어 서브파서
    mil_parser = type_subparsers.add_parser('mil', help='millennial 타입')
    mil_subparser = mil_parser.add_subparsers(dest='command', help='mil 관련된 명령')
    # mil - get 파서
    mil_get_parser = mil_subparser.add_parser('get', help='mil get 책정 및 레디스 저장')
    mil_get_parser.add_argument('code', type=str, help='종목코드 or all')
    mil_get_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    mil_get_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    mil_get_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # blue 명령어 서브파서
    blue_parser = type_subparsers.add_parser('blue', help='Blue 타입')
    blue_subparser = blue_parser.add_subparsers(dest='command', help='blue 관련된 명령')
    # blue - get 파서
    blue_get_parser = blue_subparser.add_parser('get', help='blue get 책정 및 레디스 저장')
    blue_get_parser.add_argument('code', type=str, help='종목코드 or all')
    blue_get_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    blue_get_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    blue_get_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # growth 명령어 서브파서
    growth_parser = type_subparsers.add_parser('growth', help='Growth 타입')
    growth_subparser = growth_parser.add_subparsers(dest='command', help='growth 관련된 명령')
    # growth - get 파서
    growth_get_parser = growth_subparser.add_parser('get', help='growth get 책정 및 레디스 저장')
    growth_get_parser.add_argument('code', type=str, help='종목코드 or all')
    growth_get_parser.add_argument('-e', '--expect_earn', type=float, help='기대수익률 (실수 값 입력)')
    growth_get_parser.add_argument('-r', '--refresh', action='store_true', help='래디스 캐시를 사용하지 않고 강제로 재계산 할지')
    growth_get_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # setting 명령어 서브파서
    setting_parser = type_subparsers.add_parser('setting', help='Set and Get settings')
    setting_subparser = setting_parser.add_subparsers(dest='command', help='setting 관련된 명령')
    # setting - set 파서
    set_parser = setting_subparser.add_parser('set', help='세팅값 저장')
    set_parser.add_argument('title', choices=AnalyserSettingsManager.TITLES, help='타이틀')
    set_parser.add_argument('value', help='세팅값')
    # setting - get 파서
    get_parser = setting_subparser.add_parser('get', help='타이틀 세팅값 불러오기')
    get_parser.add_argument('title', choices=AnalyserSettingsManager.TITLES, help='타이틀')
    # setting - print 파서
    setting_subparser.add_parser('print', help='전체 세팅값 출력')

    args = parser.parse_args()

    from analyser_hj3415 import eval, tsa

    if args.type == 'red':
        if args.command == 'get':
            if args.code == 'all':
                # 저장된 기대수익률을 불러서 임시저장
                ee_orig = eval.Red.expect_earn

                red = eval.Red('005930')
                if args.expect_earn:
                    eval.Red.expect_earn = float(args.expect_earn)

                print("**** Red - all codes ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    red.code = code
                    print(f"*** {i} / {red} ***")
                    pprint.pprint(red.get(args.refresh, verbose=False))

                # 원래 저장되었던 기대수익률로 다시 복원
                eval.Red.expect_earn = ee_orig
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                # 저장된 기대수익률을 불러서 임시저장
                ee_orig = eval.Red.expect_earn

                red = eval.Red(args.code)
                if args.expect_earn:
                    args.refresh = True
                    eval.Red.expect_earn = float(args.expect_earn)

                print(f"*** Red - {red} ***")
                pprint.pprint(red.get(args.refresh))

                # 원래 저장되었던 기대수익률로 다시 복원
                eval.Red.expect_earn = ee_orig
            if args.noti:
                noti.telegram_to('manager', f"오늘의 Red({args.code})를 레디스캐시에 저장했습니다.(유효 12시간)")

        elif args.command == 'ranking':
            result = eval.Red.ranking(expect_earn=args.expect_earn, refresh=args.refresh)
            print(result)
            if args.noti:
                noti.telegram_to('manager', "오늘의 red ranking을 레디스캐시에 저장했습니다.(유효 12시간)")

    elif args.type == 'mil':
        if args.command == 'get':
            if args.code == 'all':
                mil = eval.Mil('005930')
                print("**** Mil - all codes ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    mil.code = code
                    print(f"*** {i} / {mil} ***")
                    pprint.pprint(mil.get(args.refresh, verbose=False))
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                mil = eval.Mil(args.code)
                print(f"*** Mil - {mil} ***")
                pprint.pprint(mil.get(args.refresh))
            if args.noti:
                noti.telegram_to('manager', f"오늘의 Mil({args.code})를 레디스 캐시에 저장했습니다.(유효 12시간)")

    elif args.type == 'blue':
        if args.command == 'get':
            if args.code == 'all':
                blue = eval.Blue('005930')
                print("**** Blue - all codes ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    blue.code = code
                    print(f"*** {i} / {blue} ***")
                    pprint.pprint(blue.get(args.refresh, verbose=False))
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                blue = eval.Blue(args.code)
                print(f"*** Blue - {blue} ***")
                pprint.pprint(blue.get(args.refresh))
            if args.noti:
                noti.telegram_to('manager', f"오늘의 Blue({args.code})를 레디스 캐시에 저장했습니다.(유효 12시간)")

    elif args.type == 'growth':
        if args.command == 'get':
            if args.code == 'all':
                growth = eval.Growth('005930')
                print("**** Growth - all codes ****")
                for i, code in enumerate(myredis.Corps.list_all_codes()):
                    growth.code = code
                    print(f"*** {i} / {growth} ***")
                    pprint.pprint(growth.get(args.refresh, verbose=False))
            else:
                assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
                growth = eval.Growth(args.code)
                print(f"*** growth - {growth} ***")
                pprint.pprint(growth.get(args.refresh))
            if args.noti:
                noti.telegram_to('manager', f"오늘의 Growth({args.code})를 레디스 캐시에 저장했습니다.(유효 12시간)")
    elif args.type == 'prophet':
        if args.command == 'ranking':
            myprophet = tsa.MyProphet
            myprophet.expire_time_h = 72
            result = myprophet.ranking(refresh=args.refresh)
            print(result)
            if args.noti:
                noti.telegram_to('manager', f"오늘의 prophet ranking을 레디스캐시에 저장했습니다.(유효 {myprophet.expire_time_h}시간)")
    elif args.type == 'lstm':
        mylstm = tsa.MyLSTM
        mylstm.expire_time_h = 72
        if args.command == 'caching':
            if args.top:
                mylstm.caching_based_on_prophet_ranking(refresh=args.refresh, top=args.top)
            else:
                mylstm.caching_based_on_prophet_ranking(refresh=args.refresh)
            if args.noti:
                noti.telegram_to('manager', f"오늘의 lstm caching(top={args.top if args.top else 20})을 레디스캐시에 저장했습니다.(유효 {mylstm.expire_time_h}시간)")
        elif args.command == 'get':
            assert utils.is_6digit(args.code), "code 인자는 6자리 숫자이어야 합니다."
            result = mylstm(args.code).get_final_predictions(refresh=args.refresh)
            if args.noti:
                noti.telegram_to('manager', f"LSTM 분석을({args.code})를 레디스 캐시에 저장했습니다.(유효 {mylstm.expire_time_h}시간)")
    elif args.type == 'setting':
        if args.command == 'set':
            settings_manager.set_value(args.title, args.value)
        elif args.command == 'get':
            value = settings_manager.get_value(args.title)
            print(f"{args.title} 값: {value}")
        elif args.command == 'print':
            print(settings_manager.load_settings())
    else:
        parser.print_help()
