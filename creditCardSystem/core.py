import re
import sys
from decimal import Decimal

from creditCardSystem.exceptions import ParseError
from creditCardSystem.logsModule import set_logger

log = set_logger('logger')

class Processor(object):

    def __init__(self, *args, **kwargs):
        self.db = kwargs.get('db', {})
        if not isinstance(self.db, dict):
            raise TypeError('데이터베이스는 반드시 dictionary 타입이어야 합니다.')

    def parse_event(self, event):
        """
        하나의 event 값을 3개의 구성 요소(event_type, name, numbers)로 분리.
        :param event:
        :return:
        """

        if not isinstance(event, str):
            raise ValueError('이벤트 타입은 string 타입이어야 합니다(Add, Credit, Charge)')

        # *numbers: 인자의 갯수가 명확하지 않을 때, 가변적 파라미터를 넘겨야 하는 경우 사용.
        event_type, name, *numbers = event.split()

        if not numbers:
            raise ParseError(
                "numbers 구문 분석에서 오류가 발생했습니다. "
                "이벤트 타입, 이름, 그리고 추가 정보: {0}가 필요합니다.".format(numbers)
            )

        # $ 기호 삭
        args = map(self.parse_dollars, numbers)

        # 이벤트 타입에 따른 core 함수 호출
        method = getattr(self, event_type.lower())
        method(name, *args)

    @staticmethod
    def parse_dollars(number):
        """
        number 값에 어떤 값이 들어올지 모르는 상황에서(카드번호, 또는 한도금액)
        한도 금액이 들어 올 경우, '$' 표시를 제거하고 반환,
        카드 번호가 들어올 경우, numeric type 인지를 검증 후 반환.
        :param number:
        :return:
        """
        if not re.match(r'[$+-]?(\d+(\.\d*)?|\.\d+)', number):
            raise ValueError('숫자는 반드시 numeric 타입이어야 합니다.')
        if '$' in number:
            return Decimal(number.strip('$'))
        else:
            return number

    @staticmethod
    def check_amount(amount):
        """
        금액 값이 Decimal 타입인지를 검증
        :param amount
        :return
        """
        if not isinstance(amount, Decimal):
            raise TypeError(
                '유효하지 않은 파라미터 타입임. '
                'amount={0} 는 반드시 Decimal 타입이어야 함.'.format(type(amount))
            )

    @staticmethod
    def luhn_checksum(card_number):
        """
        luhn10 algirithm
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def is_luhn_valid(self, card_number):
        """
        luhn 유효성 검증
        """
        return self.luhn_checksum(card_number) == 0

    def add(self, name, card_number, limit):
        """
        새로운 카드 번호를 등록함.
        카드 번호만 검증.
        카드 번호가 유효한지 luhn 알고리즘을 통해서 검증.
        """
        log.info('신규 카드 등록, 번호:{0}, 이름:{1}, 한도:{2}'.format(card_number, name, limit))

        if self.is_luhn_valid(card_number):
            balance = Decimal(0)
        else:
            log.warning('유효하지 않은 카드번호: {0}'.format(card_number))
            balance = 'error'

        self.db[name] = {'card_number': card_number, 'limit': limit, 'balance': balance}

    def get_account_details(self, name):
        """
        사용자의 계좌에 대한 상세 내용을 추출.
        account, balance, card_number, limit = self.get_account_details(name)
        """

        try:  # to get account
            account = self.db[name]
        except KeyError as e:
            log.error('계좌가 존재하지 않습니다.')
            raise

        if not isinstance(name, str):
            raise TypeError(
                '유효하지 않은 파라미터 타입입니다. '
                'name={0} 은 반드시 string 타입 이어야 합니다.'.format(type(name))
            )

        balance = account.get('balance', None)
        card_number = account.get('card_number', None)
        limit = account.get('limit', None)

        if any(param is None for param in [balance, card_number, limit]):
            raise KeyError((
                'Missing parameter(s) required for processing charge - '
                'balance={0} card_number={1} limit={2}'.format(balance, card_number, limit)
            ))

        return account, balance, card_number, limit

    def charge(self, name, amount):
        """
        특정 사용자에게 일정 금액(신용카드를 통해서 지불해야 할 금액)을 계좌에 더함.
        카드 번호 유효성을 검증한다.

        """
        log.info('{0}에게 {1}를 더함'.format(name, amount))
        self.check_amount(amount)
        account, balance, card_number, limit = self.get_account_details(name)

        if not self.is_luhn_valid(card_number) or amount + balance > limit:
            return balance

        account['balance'] += amount

    def credit(self, name, amount):
        """
        특정 사용자의 계좌에 일정 금액(신용카드로 지불한 금액) 뺌.
        """
        log.info('{0}에게서 {1}을 뺌.'.format(name, amount))
        self.check_amount(amount)

        account, balance, card_number, limit = self.get_account_details(name)

        if not self.is_luhn_valid(card_number):
            return balance

        account = self.db.get(name, None)
        account['balance'] -= amount

    def gen_totalinfo(self):
        """
        output을 위한 string 결과값을 생성.
        name은 알파벳 순서.
        dollar 값에는 $ 기호 붙여서 기록.
        한줄 한줄 기록됨.
        :return:
        """
        summary = ''
        for key in sorted(self.db.keys()):
            balance = '${0}'.format(self.db[key].get('balance'))

            if 'error' in balance:
                balance = balance.strip('$')

            summary += '{0}: {1}\n'.format(key, balance)
        return summary

    @staticmethod
    def write_output(summary):
        """
        STDOUT 값을 출력하기 위한 함수
        """
        sys.stdout.write(summary)
