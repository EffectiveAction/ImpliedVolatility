from function_file import import_series,  trendline, implied_volatility
from matplotlib import pyplot as plt
import numpy as np
import csv
import time
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

#Here we import the list containing the S&P500 ticker symbols from a CSV file
filename = 'sp500_companies.csv'
with open(filename) as f:
    reader=csv.reader(f)
    header_row=next(reader)

    symbols=[]
    for row in reader:
        symbols.append(row[1])


#selecting N largest companies in the S&P500
N=10
#GOOGL had a recent stock split, while we could deal with it let us discard GOOGL for now in this current version


ticker_list=symbols[0:N+2] 
ticker_list.remove('GOOGL')
ticker_list.remove('GOOG')


print('We are using: '+str(ticker_list))



#if you are interested in a sinlge ticker just change symbols to e.g. ["TSLA"]


implied_volatilities=[]

print(ticker_list)
for ticker in ticker_list:

    #frequency can be chosen DAILY/WEEKLY/MONTHLY.
    frequency='DAILY' 

    #import dates and closing prices
    dates, prices =import_series(ticker,frequency)
    prices=[float(i) for i in prices]
    freq_iterations=list(range(len(prices)))

    #transform to log-space
    x_prices=np.log(np.array(prices)/prices[0])

    #From this point on we assume the frequency is 'Daily' for further analysis.
    trunc_market_time,trunc_market_price, price_trend =trendline(x_prices,10)

    x_detrend=np.array(trunc_market_price)-np.array(price_trend)
    imp_vol=implied_volatility(x_detrend)
    implied_volatilities.append(imp_vol)
    print(imp_vol)

    #AlphaVantage has a limit of 5 request/minute
    time.sleep(20)

my_style=LS('#333366', base_style=LCS)
chart=pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title='Historical volatility of the '+str(N)+' largest companies of the S&P500 (stock-split exempted)'
chart.x_labels=ticker_list
chart.add('',implied_volatilities)

chart.render_to_file('bar_chart.svg')



#if you are interested to check trendline for individual ticker, uncomment below after setting e.g. ticker_list=['TSLA'] to a single company of interest 

# plt.plot(trunc_market_time,trunc_market_price,linewidth=2,c='red')
# plt.plot(trunc_market_time,price_trend,linewidth=2,c='blue')
# plt.xlabel('Market closing price '+'('+frequency.lower()+')')
# plt.ylabel('Stock price (USD)')
# plt.show() 
# ^ uncomment to show plot