> 전반적인 설계에 대한 간략한 설명
>> Add: 새로운 신용카드에 새 사용자 이름, 새 카드 번호(Luhn10 알고리즘 통과한 카드번호), 한도액을 설정함.
is_luhn_valid -> luhn_checksum 함수를 통해서 luhn 알고리즘으로 카드번호 검증:
카드번호가 검증되면 저장.

>> Charge: 사용자 이름과 신용카드로 지불할 금액을 전달하여 잔고의 잔액을 증가시킴.
get_account_details을 통해서 사용자의 account, balance, card_number, limit 정보를 취득.
카드 번호 유효성 검증 완료 후, Charge 함수 호출시 넘겨 받은 신용카드로 지할 금액을 사용자 계좌 잔액에 더함.

>> Credit: 사용자 이름과 부과할 금액을 전달하여, 잔고의 잔액을 감소시킴.
get_account_details을 통해서 사용자의 account, balance, card_number, limit 정보를 취득.
카드 번호 유효성 검증 완료 후, Credit 함수 호출시 넘겨 받은 신용카드로 지불한 금액을 사용자 계좌 잔액에서 뺌 .

>> get_account_details: 사용자 이름을 통해서 사용자의 계좌 정보를 확인할 수 있다.
사용자 계좌의 잔액, 사용자 카드번호, 사용자 카드 한도


> 실행 조건
>> 요구사항
Python >= 3.5



>> 설치해야 할 라이브러리
>> pip(또는 pip3) install {}
sys 설치(import sys)
unittest 설치(import unittest)
path 설치(from os import path)
Decimal 설치(from decimal import Decimal)

process_time 설치(from time import process_time)
re 설치(import re)
logging 설치(import logging)



>> 실행 예시
python3(또는 python) start.py input.txt
python3(또는 python) start.py < input.txt



>> 테스트 방법
python3(또는 python) -m unittest discover tests
python3(또는 python) tests/test.py



>> 프로젝트(cdTest_syhan) 구조
├─.idea
│  └─inspectionProfiles
├─creditCardSystem
│  ├─core.py
│  ├─exceptions.py
│  ├─logsModule.py
│  └─__pycache__
├─.gitignore
├─input.txt
├─process.log
├─README.md
├─start.py
└─tests
    └─test.py



>> 개선 가능한 부분
1. 검증 알고리즘: Luhn 알고리즘은 전체 카드 번호에 대한 각각의 한자리 숫자를 이용해서 유효성을 검증하는 간단한 방법임.
더 복잡한 유효성 체크로 Verhoeff algorithm 와 Damm algorithm 를 사용할 수 있다.

2. 암호화: 카드 번호, 사용자 이름, 금액 정보에 대한 암호화.
간단하게는  AES256을 적용하여 대칭 암호화를 통한 정보 보호를 할 수 있다.

3. 알림시스템: 로그에 찍히는 레벨을 기준으로 WARNING이상에서는 관리자에게 알림을 주는 시스템을 추가 구축할 수 있다.

