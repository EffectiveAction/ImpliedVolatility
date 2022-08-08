# ImpliedVolatility
In this project we compute the implied stock volatility of all the companies of the S&P500 based on historical data

main script file (run this) : stock_analysis.py
necessary files (add to the same folder): function_file.py (contains all the functions), sp500_companies.cvs (contains symbols of all S&P500 companies as of 2022)

The code makes an API call to AlphaVantage's free historical stock data for which it uses the sp500_companies.cvs to automatically run it for N largest companies.

For each company, the daily stock price at close is imported using import_series() as a time series for the latest ~100 days.
NOTE: In the current version of the code, stock splits within this period have to be exempted manually as is done here with GOOGL.


The time series is then transformed into log-space in "x_prices" which it it is assumed to behave according to a Geometric Brownian Motion.

The function trendline() then finds a trend using standard moving average techniques (see Physica A: Statistical Mechanics and its ApplicationsVolume 587, 2022, 126487)

After removing the trend within the assumptions of the Black-Scholes model we have a pure Wiener motion for which we find the implied volatility in the function implied_volatility()

Repeating this for multiple ticker symbols yields the bar chart as a final outcome.
