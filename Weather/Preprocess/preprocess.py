import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics import tsaplots
from statsmodels.tsa.stattools import adfuller
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


def drop_duplicates():
    data = pd.read_csv("../data/weather_dava.csv")
    to_drop = data[(data["Max_Temp"].isnull()) & (data["Min_Temp"].isnull()) & (data["Mean_Temp"].isnull())]
    data.drop(to_drop.index, inplace=True)
    save_path = "../data/processed.csv"
    data.to_csv(save_path, index=False, header=True)


def process_missing_values():
    data = pd.read_csv("../data/processed.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    all_days = (pd.date_range(start='2000-01-01', end='2022-12-31'))
    df = data.reindex(all_days)
    df = df.reset_index().rename(columns={'index': 'Date'})
    df.loc[df["Year"].isnull(), "Year"] = df["Date"].dt.year
    df.loc[df["Month"].isnull(), "Month"] = df["Date"].dt.month
    df.loc[df["Day"].isnull(), "Day"] = df["Date"].dt.day
    df = df.astype({"Year": int, "Month": int, "Day": int})
    df["Max_Temp"] = df.groupby(["Month", "Day"])["Max_Temp"].transform(lambda x: x.fillna(x.mean().round(1)))
    df["Min_Temp"] = df.groupby(["Month", "Day"])["Min_Temp"].transform(lambda x: x.fillna(x.mean().round(1)))
    df["Mean_Temp"] = df.groupby(["Month", "Day"])["Mean_Temp"].transform(lambda x: x.fillna(x.mean().round(1)))
    save_path = "../data/imputed.csv"
    df.to_csv(save_path, index=False, header=True)


def seasonality_analysis():
    data = pd.read_csv("../data/imputed.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    df_max_temp = data.loc[:, ["Date", "Max_Temp"]]
    df_max_temp = df_max_temp.set_index("Date")
    decomposition = sm.tsa.seasonal_decompose(df_max_temp)
    decomposed_data = pd.DataFrame()
    decomposed_data["trend"] = decomposition.trend
    decomposed_data["seasonal"] = decomposition.seasonal
    decomposed_data["random_noise"] = decomposition.resid
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(16, 12))
    decomposed_data['trend'].plot(ax=ax1)
    decomposed_data['seasonal'].plot(ax=ax2)
    decomposed_data['random_noise'].plot(ax=ax3)
    plt.show()


def stationarity_analysis():
    data = pd.read_csv("../data/imputed.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    df_max_temp = data.loc[:, ["Date", "Max_Temp"]]
    df_max_temp = df_max_temp.set_index("Date")
    train, test = train_test_split(df_max_temp, '2020-01-01')
    result = adfuller(train['Max_Temp'])
    print(result[0])
    print(result[1])  # To get the p-value
    print(result[4])


def acf_pacf_plots():
    data = pd.read_csv("../data/imputed.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    df_max_temp = data.loc[:, ["Date", "Max_Temp"]]
    df_max_temp = df_max_temp.set_index("Date")
    train, test = train_test_split(df_max_temp, '2020-01-01')
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    tsaplots.plot_acf(train, zero=False, ax=ax1)
    tsaplots.plot_pacf(train, zero=False, ax=ax2, lags=8)
    plt.show()


def train_test_split(df, cutoff):
    train = df.loc['2000-01-01':cutoff]
    test = df.loc[cutoff:]
    return train, test
