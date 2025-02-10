#importing libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

#importing dataset
data = pd.read_csv("geocode_coordinates.csv")

#cleaning dataset
data["quarter"] = pd.to_datetime(data["quarter"])                   #converting "quarter" to pandas datetime
data.set_index("quarter", inplace=True)                             #setting quarter to index
data["avg"] = round((data["onebhk"] + data["twobhk"] + data["threebhk"]) / 3, 2)
data = data.drop(data.columns[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10]], axis = 1)   #dropping extra columns
data["type"] = "Historical Prices"          #marking data as historical


def get_forecast(city):
    df = data[data["city"] == city]
    df = df.asfreq("QS-JUN") 
    df_city = df 

    # Transforming Data
    df.loc[:, "Log"] = np.log(df["avg"])            #applying log transformation
    df.loc[:, "LogDiff1"] = df["Log"].diff()        # 1st order differencing
    df.loc[:, "LogDiff2"] = df["LogDiff1"].diff()   # 2nd order diffrencing

    # Training ARIMA Model on dataset
    model = ARIMA(df["LogDiff1"].dropna(), order = (1, 0, 1)).fit()

    #forecasting next 4 quarters
    forecast_steps = 4
    forecast = model.forecast(steps = forecast_steps)

    #reverse transforming data
    LastVal_LogDiff1 = df["LogDiff2"].iloc[-1]
    Undiff2 = LastVal_LogDiff1 + forecast.cumsum()          #reversing 2nd order differencing
    LastVal_Log = df["Log"].iloc[-1]
    Undiff1 = LastVal_Log + Undiff2.cumsum()                #reversing 1st order differencing
    final_forecast = np.exp(Undiff1)                        #reversing log transformation
    final_forecast = final_forecast.to_frame(name="avg")    #converting from pd.series to pd.dataframe and giving it name as avg
    final_forecast["type"] = "Forecasted Prices"            #marking data as forecast
    historical = df_city.drop(data.columns[0], axis = 1)       #dropping city name
    df_all = pd.concat([historical, final_forecast])        #concatinating both
    df_all.to_csv("city.csv")

    return df_all



