import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


def train_test_split(df, cutoff):
    train = df.loc['2000-01-01':cutoff]
    test = df.loc[cutoff:]
    return train, test


data = pd.read_csv("../data/imputed.csv")
data['Date'] = pd.to_datetime(data['Date'])
df_max_temp = data.loc[:, ["Date", "Max_Temp"]]
df_max_temp = df_max_temp.set_index("Date")
train, test = train_test_split(df_max_temp, "2015-01-01")
ar_ma_1_model = ARIMA(train, order=(2, 0, 1))
ar_ma_1_results = ar_ma_1_model.fit()
predictions = ar_ma_1_results.predict(start=6000, end=8000)
fig, ax = plt.subplots(figsize=(16, 6))
train.plot(ax=ax)
test.plot(ax=ax)
predictions.plot(ax=ax)
plt.legend(['train data', 'test data', 'forecasted'])
plt.axvline(x='2020-01-01', color='black', linestyle='--')
plt.show()
