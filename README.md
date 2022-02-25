# death_cross
Death Cross happens when an index's 50-day moving averages crossing below its 200-day moving averages, which usually indicates the potential for a major selloff.

The purpose of this code is to find the dates death cross happened for the any major index. In this code, we will retrieve the index data from Tushare for analyzing. 
Tushare is a free and open financial big data platform of all data categories. You can easily retrieve the data you want by simply a few lines of code, and do not need to worry about the integrality and the accuracy of the data, which will greatly improve the productivity and eliminate the need for data preprocessing.

If you would like to have a try, please register through the following link: https://tushare.pro/register?reg=456046.

Codes:

  First, we need to import tushare and pandas, and read the tushare token and the index code from config.txt (You can get your token from Profile-TOKEN and the index code from Data Api).

      import tushare as ts, pandas as pd

      with open("config.txt") as f:
          config = f.readlines()
      api = config[0][:-1]
      code = config[1]

      pro = ts.pro_api(api)

  Then, retrieve the data of the index from tushare and store it to a DataFrame (We only need one line to retrieve all the data we need).

      df = pro.index_global(ts_code=code, start_date="20150101", end_date="20220224")

  Sort the data by trade_date in ascending order.

      df["trade_date"] = pd.to_datetime(df["trade_date"])
      df.sort_values("trade_date", inplace=True, ascending=True)
      df.dropna(1, inplace=True)

  Use the function rolling from Pandas to calculate the 50-day and 200-day moving averages.

      ma_short = 50
      ma_long = 200
      df.insert(len(df.columns), 'ma_short', df['close'].rolling(ma_short, min_periods=1).mean())
      df.insert(len(df.columns), 'ma_long', df['close'].rolling(ma_long, min_periods=1).mean())

  Find the dates when death cross happened:
    1. Find the dates when 50-day moveing averages are below those of 200-day
    2. Find the dates when the previous day's 50-day moveing averages are above those of 200-day
    3. Combine them together to find the dates of death cross, set their signal to 1.

      condition1 = df['ma_short'] < df['ma_long']  #ma_short < ma_long
      condition2 = df['ma_short'].shift(1) >= df['ma_long'].shift(1)
      df.loc[condition1 & condition2, 'signal'] = 1

  Finally, store the data to csv files.

      #store the death cross dates and the data
      df.to_csv(f"{code}.csv", encoding="utf-8-sig", index=False)
      dc = df[df["signal"]==1]
      dc.to_csv(f"{code}_death_cross.csv", encoding="utf-8-sig", index=False)

Result:

  By applying this code, we found that the most recent death cross about S&P500 happend on at 3/30/2020.

  ![image](https://user-images.githubusercontent.com/78573538/155663828-4019a4ea-3dd1-4ce7-9b1d-99c486ec29f0.png)

  And from 01/01/2015 to 02/24/2022, there are 4 death cross.

  ![image](https://user-images.githubusercontent.com/78573538/155663702-4721f27e-24be-4f97-be23-9515c1c8c772.png)

