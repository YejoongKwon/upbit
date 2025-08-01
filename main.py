# main.py
# market.py, account.py 등 필요없다.
import os
from dotenv import load_dotenv
import pyupbit

load_dotenv()
access_key = os.environ.get('UPBIT_ACCESS_KEY')
secret_key = os.environ.get('UPBIT_SECRET_KEY')
upbit=pyupbit.Upbit(access_key, secret_key)

#전체잔고
BALANCE = upbit.get_balances()
#원화 잔고
KRW_BALANCE = upbit.get_balance('KRW')
#비트코인 잔고
BTC_BALANCE = upbit.get_balance('BTC')

#원화 마켓 티커
krw_tickers = pyupbit.get_tickers("KRW")

#print(BALANCE)