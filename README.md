> 전반적인 설계에 대한 간략한 설명

참조: https://github.com/alexanderattar/credit-card-processor

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

