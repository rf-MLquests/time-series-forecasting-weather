import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics import tsaplots
from statsmodels.tsa.arima.model import ARIMA
import os


def init_read():
    directory = '../data'
    paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".csv")]
    save_path = directory + "/weather_dava.csv"
    individual_dfs = [read_file(path) for path in paths]
    data = pd.concat(individual_dfs)
    column_names = ["Date", "Year", "Month", "Day", "Max_Temp", "Min_Temp", "Mean_Temp"]
    data["Date/Time"] = pd.to_datetime(data["Date/Time"])
    data.sort_values(by="Date/Time", inplace=True)
    data.to_csv(save_path, index=False, header=column_names)


def read_file(path):
    current = pd.read_csv(path)
    return current.iloc[:, [4, 5, 6, 7, 9, 11, 13]]


def preprocess():
    data = pd.read_csv("../data/weather_dava.csv")
    to_drop = data[(data["Max_Temp"].isnull()) & (data["Min_Temp"].isnull()) & (data["Mean_Temp"].isnull())]
    data.drop(to_drop.index, inplace=True)
    save_path = "../data/processed.csv"
    data.to_csv(save_path, index=False, header=True)


def fill_in_missing_dates():
    data = pd.read_csv("../data/processed.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    all_days = (pd.date_range(start='2000-01-01', end='2022-12-31'))
    df = data.reindex(all_days)
    df = df.reset_index().rename(columns={'index': 'Date'})
    print(df.info())

    # df.loc[df["Year"].isnull(), "Year"] = df["Date"].year
    # print(df.tail(10))


fill_in_missing_dates()

# data.drop(data[data["Year"] == 2013].index, inplace=True)
# to_drop = data[(data["Year"] == 2013) & data is not None]
# print(to_drop)


# data["time"] = pd.to_datetime(data["timestamp"], unit="s")
#
# df = data.loc[:, ["temperature", "time"]].groupby(pd.Grouper(key="time", freq="1D")).mean()
# print(df)
# print(df.info())
# df_shift = df.shift(periods=1)
# print(df_shift)
# print(df_shift.info())
# diff = df - df_shift
# print(diff[1:])
#
# decomposition = sm.tsa.seasonal_decompose(diff[1:])
# decomposed_data = pd.DataFrame()
# decomposed_data["trend"] = decomposition.trend
# decomposed_data["seasonal"] = decomposition.seasonal
# decomposed_data["random_noise"] = decomposition.resid
#
# fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(20, 16))
# decomposed_data['trend'].plot(ax=ax1)
# decomposed_data['seasonal'].plot(ax=ax2)
# decomposed_data['random_noise'].plot(ax=ax3)
# plt.show()
