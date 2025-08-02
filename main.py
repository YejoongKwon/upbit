# main.py
# market.py, account.py 등 필요없다.
import os
from dotenv import load_dotenv
import pyupbit
import time, datetime
import pandas as pd
import numpy as np

load_dotenv()
access_key = os.environ.get('UPBIT_ACCESS_KEY')
secret_key = os.environ.get('UPBIT_SECRET_KEY')
upbit=pyupbit.Upbit(access_key, secret_key)
#
# #전체잔고
# BALANCE = upbit.get_balances()
# #원화 잔고
# KRW_BALANCE = upbit.get_balance('KRW')
# #비트코인 잔고
# BTC_BALANCE = upbit.get_balance('BTC')
#
# #원화 마켓 티커
# krw_tickers = pyupbit.get_tickers("KRW")

#K 30일마다 갱신해주자
def GET_TARGET_PRICE(K):
    df = pyupbit.get_ohlcv("KRW-BTC", count=2)
    gap = df['high'][0] - df['low'][0] #전날 고점 저점의 변동폭
    target = df['open'][-1] + gap*K # 오늘의 목표가(도달시 매수)
    return target

def SET_START_TIME():
    df = pyupbit.get_ohlcv("KRW-BTC",count=1)
    start = df.index[0] # 오늘 캔들의 시작 시각
    return start

def GET_BALANCE(ticker):
    """코인(KRW 또는 BTC) 보유 수량을 가져옴"""
    balances = upbit.get_balances()
    for balance in balances:
        if balance['currency'] == ticker and balance['balance'] != None:
            return float(balance['balance'])
        else:
            return 0

def GET_CURRENT_PRICE_LIST():
    """역할: 현재 오더북(호가창)을 DataFrame으로 변환 → 매수·매도 호가 리스트를 확인 가능"""
    current = pyupbit.get_orderbook(ticker="KRW-BTC")
    df = pd.DataFrame(current)
    return df

def GET_CURRENT_PRICE():
    """역할: 현재 매도 1호가(ask_price, 즉 즉시 살 수 있는 가격)를 가져옴"""
    price = pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]
    return price

while True:
    try:
        NOW = datetime.datetime.now()
        START_TIME=SET_START_TIME()
        END_TIME = START_TIME + datetime.timedelta(days=1)

        KRW_BALANCE=GET_BALANCE("KRW")
        BTC_BALANCE=GET_BALANCE("BTC")
        # 매매로직
        ## 매매 시간일 때 (하루 중)
        if START_TIME <= NOW < END_TIME : #장이 열려있음
            TARGET_PRICE=GET_TARGET_PRICE(0.7)
            CURRENT_PRICE = GET_CURRENT_PRICE()

            # 목표가 < 현재가 & 내 보유현금 10만원 이상임
            if TARGET_PRICE < CURRENT_PRICE and KRW_BALANCE >100000:
                upbit.buy_market_order("KRW-BTC", KRW_BALANCE*0.9995)
                # 거래수수로 0.05% 고려해서 0.9995 곱해줌.
                ## 즉, 100,000원을 시장가 매수하면 실제로는 약 99,950원치의 비트코인을 사게 됩니다.
        else:
            # 장 마감 후: 비트코인을 모두 시장가 매도
            if BTC_BALANCE > 0 :
                upbit.sell_market_order("KRW-BTC", BTC_BALANCE)

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)