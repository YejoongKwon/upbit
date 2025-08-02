import os
import pyupbit
import pandas as pd
import numpy as np
import time
def GET_ROR(df: pd.DataFrame, K: float) -> float:
    """역할: 특정 K 값에 대해 백테스트를 수행하여 최종 누적수익률(hpr)을 반환"""
    df = df.copy()  # 원본 df를 변경하지 않기 위해 복사

    # range → 당일 변동폭 × K
    df['range'] = (df['high']-df['low']) * K
    # target → 오늘의 매수 목표가 = 오늘 시가(open) + 어제 변동폭(K배)
    df['target'] = df['open'] + df['range'].shift(1)

    # 거래수수로 0.05%
    tax=0.0005
    # ror : 수익률
    df['ror'] = np.where(df['high'] > df['target'], # 조건: 당일 고가(high) > 목표가(target) → 목표 돌파 성공 시 매수
                         ( df['close']*(1-tax) ) / ( df['target']*(1+tax) ),## 참일 때 → 수익률 = (종가 / 목표가) (수수료 반영)
                         1) ## 거짓일 때 → 매수하지 않음 → 수익률 1 유지
    # hpr : 누적수익률
    df['hpr'] = df['ror'].cumprod() # 누적곱(ex. 첫날 1.02, 둘째날 0.99 → 전체 수익률 1.02×0.99)
    return df['hpr'].iloc[-1]

# ✅ API 호출은 한 번만!
df = pyupbit.get_ohlcv(ticker="KRW-BTC")

if df is None:
    raise ValueError("⚠️ get_ohlcv()에서 데이터를 가져오지 못했습니다.")

for i in np.arange(0.01, 1, 0.05):
    ROR = GET_ROR(df, i)
    print(i, ROR)
