import statistics
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from dateutil.relativedelta import relativedelta


def apple_one_year_proj():
    style.use('ggplot')

    stock_ticker = 'AAPL'

    start = dt.datetime(2015, 5, 22)
    end = dt.datetime(2020, 5, 22)


    prices = web.DataReader(stock_ticker, 'yahoo', start, end).reset_index()['Close']
    returns = prices.pct_change()

    last_price = prices[len(prices)-1]

    # Number of Simulations
    num_simulations = 1000
    num_days = 252

    simulation_df = pd.DataFrame()

    for x in range(num_simulations):
        count = 0
        daily_volatility = returns.std()
        avg_daily_returns = returns.mean()

        price_series = []

        price = last_price * (1 + np.random.normal(avg_daily_returns, daily_volatility)) #shock constant
        price_series.append(price)

        for y in range(num_days):
            if count == 251:
                break
            price = price_series[count] * (1 + np.random.normal(avg_daily_returns, daily_volatility)) #shock constant
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    end_of_year_averages = simulation_df.values[-1].tolist()
    end_of_year_estimation = statistics.mean(end_of_year_averages)
    print("Estimated Price: " + str(end_of_year_estimation))

    #print(simulation_df)
    fig = plt.figure()
    fig.suptitle('Monte Carlo Simulation: ' + stock_ticker)
    plt.plot(simulation_df)
    plt.axhline(y=last_price, color='r', linestyle='-')
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.show()

def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    return dt

def monte_carlo_simulation(ticker_symbol:str, duration:float):
    style.use('ggplot')

    #Looking at the data from past 5 years
    end = dt.datetime.today()

    start = end - dt.timedelta(days=5*365)


    prices = web.DataReader(ticker_symbol, 'yahoo', start, end).reset_index()['Close']
    returns = prices.pct_change()

    last_price = prices[len(prices) - 1]

    # Number of Simulations
    num_of_simulations = 1000
    projection_duration = round(252*duration)

    simulation_df = pd.DataFrame()

    for x in range(num_of_simulations):
        count = 0
        daily_volatility = returns.std()
        avg_daily_returns = returns.mean()

        price_series = []

        price = last_price * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
        price_series.append(price)

        for y in range(projection_duration):
            if count == 251:
                break
            price = price_series[count] * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    end_of_year_averages = simulation_df.values[-1].tolist()
    end_of_year_estimation = statistics.mean(end_of_year_averages)
    print("Estimated Price: " + str(end_of_year_estimation))

    # print(simulation_df)
    fig = plt.figure()
    fig.suptitle('Monte Carlo Simulation: ' + ticker_symbol)
    plt.plot(simulation_df)
    plt.axhline(y=last_price, color='r', linestyle='-')
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.show()





def main():
    tikr = input("Which stock are you interested in?")
    tikr = tikr.upper()
    if tikr == "AAPL":
        apple_one_year_proj()
    else:
        dur = float(input("How far do you want to project (in years)?"))
        monte_carlo_simulation(tikr, dur)


if __name__ == "__main__":
    main()