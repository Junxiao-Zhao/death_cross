import tushare as ts, pandas as pd

#read tushare api and the ts_code from config.txt
with open("config.txt") as f:
    config = f.readlines()
api = config[0][:-1]
code = config[1]

#get data
pro = ts.pro_api(api)
df = pro.index_global(ts_code=code, start_date="20150101", end_date="20220224")

#pretreat
df["trade_date"] = pd.to_datetime(df["trade_date"])
df.sort_values("trade_date", inplace=True, ascending=True)
df.dropna(1, inplace=True)

#moving-average
ma_short = 50
ma_long = 200
df.insert(len(df.columns), 'ma_short', df['close'].rolling(ma_short, min_periods=1).mean())
df.insert(len(df.columns), 'ma_long', df['close'].rolling(ma_long, min_periods=1).mean())

#find when the death cross happened
condition1 = df['ma_short'] < df['ma_long']  #ma_short < ma_long
condition2 = df['ma_short'].shift(1) >= df['ma_long'].shift(1)  #the previous day's ma_short > ma_long
df.loc[condition1 & condition2, 'signal'] = 1   #the signal of death cross

#store the death cross dates and the data
df.to_csv(f"{code}.csv", encoding="utf-8-sig", index=False)
dc = df[df["signal"]==1]
dc.to_csv(f"{code}_death_cross.csv", encoding="utf-8-sig", index=False)
