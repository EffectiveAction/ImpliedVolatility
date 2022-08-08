import requests
import numpy as np

def import_series(ticker,frequency):

    #api url using personal key (obtained for free at AlphaVantage.co)
    api_key='3YRQLT1HMDH8L3S7'

    #select ticker
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_'+frequency+'&symbol='+ticker+'&interval=5min&apikey='+api_key

    r=requests.get(url)
    data=r.json()

    """The second key in the dictionary has an irregular naming convention 
    and hence let us call it through its index"""

    key=list(data.keys())[1]
    time_series=data[key]

    #time_series contains a dictionary where the keys are dates

    dates, prices = [], []

    for key, value in time_series.items():
        dates.append(key)
        prices.append(value['4. close'])
    
    #in the json file the first item in the list is the most recent date so let us reverse the order
    dates.reverse()
    prices.reverse()

    return dates, prices



def trendline(prices,N):
    """This function will find the trend of the time series, prices should be given in log-return space. 
    and in terms of a consecutive market time unit (days/months/weeks)"""

    #the corresponding list of market time is therefore:
    market_days=list(range(len(prices)))


    #to detrend the data we will use a simple moving average similar to:
    #Physica A: Statistical Mechanics and its ApplicationsVolume 587, 1 February 2022, 126487
    #2N+1 will be the size of the MA window


    #To have a smooth trend_line it is easiest to truncate the data with half the chosen window size

    price_trend=[]
    trunc_market_time=[]
    trunc_market_price=[]
    for i in range(N,len(prices)-N):
            price_trend.append(np.average(prices[i-N:i+N]))
            trunc_market_time.append(i)
            trunc_market_price.append(prices[i])



 
    #we return the truncated market time and price and also the corresponding MA trend
    return trunc_market_time, trunc_market_price, price_trend

def implied_volatility(x_detrend):
    """This function will calculate the implied volatility of a pure
     Wiener time series in "x_detrend" which should be givein n terms of consecutive and equal market-time steps"""
     
    x_diff=[  x_detrend[i]-x_detrend[i-1] for i in range(1,len(x_detrend))]

    return np.sqrt(np.var(x_diff))









    


