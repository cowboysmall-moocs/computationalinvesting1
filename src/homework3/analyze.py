import sys
import csv
import math

import datetime          as dt
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil     as tsu


def read_orders(input_file):
    dates  = []
    prices = []

    with open(input_file) as csvfile:
        for line in csv.reader(csvfile):
            date = dt.datetime(int(line[0]), int(line[1]), int(line[2]), 16)
            dates.append(date)
            prices.append(float(line[3]))

    return dates, np.array(prices, float)


def read_prices(start, end, symbol):
    timestamps = du.getNYSEdays(start, end, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    return dataobj.get_data(timestamps, [symbol], ['close'])[0][symbol].values


def plot_timeseries(timestamps, prices, bm_prices, symbol, filepath, xlabel = 'Date', ylabel = 'Close'):
    plt.clf()
    fig = plt.figure()
    fig.add_subplot(111)

    plt.plot(timestamps, prices)
    plt.plot(timestamps, bm_prices)

    plt.legend(['Portfolio', symbol], loc = 2)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    fig.autofmt_xdate(rotation = 45)

    plt.savefig(filepath, format = 'png')
    plt.close()


def print_results(dates, symbol, values, bm_values, returns, bm_returns, total):
    print
    print 'The final value of the portfolio using the sample file is -- %s,%s,%s, %0.0f' % (dates[-1].year, dates[-1].month, dates[-1].day, total)
    print 
    print 'Details of the Performance of the portfolio :'
    print
    print 'Data Range :  %s  to  %s' % (dates[0].strftime('%Y-%m-%d %H:%M:%S'), dates[-1].strftime('%Y-%m-%d %H:%M:%S'))
    print
    print 'Sharpe Ratio of Fund : %s' % ((values.mean() / values.std()) * math.sqrt(252))
    print 'Sharpe Ratio of %s : %s' % (symbol, (bm_values.mean() / bm_values.std()) * math.sqrt(252))
    print
    print 'Total Return of Fund : %s' % (returns)
    print 'Total Return of %s : %s' % (symbol, bm_returns)
    print
    print 'Standard Deviation of Fund : %s' % (values.std())
    print 'Standard Deviation of %s : %s' % (symbol, bm_values.std())
    print
    print 'Average Daily Return of Fund : %s' % (values.mean())
    print 'Average Daily Return of %s : %s' % (symbol, bm_values.mean())
    print


def main(argv):
    input_file = argv[0]
    benchmark  = argv[1]

    dates, prices = read_orders(input_file)
    bm_prices     = read_prices(dates[0], dates[-1], benchmark)

    total       = prices[-1]
    returns     = prices[-1] / prices[0]
    bm_returns  = bm_prices[-1] / bm_prices[0]

    n_prices    = prices / prices[0]
    n_bm_prices = bm_prices / bm_prices[0]
    plot_timeseries(dates, n_prices, n_bm_prices, benchmark, './src/homework3/images/timeseries.png', ylabel = 'Normalized Close')

    tsu.returnize0(prices)
    tsu.returnize0(bm_prices)
    print_results(dates, benchmark, prices, bm_prices, returns, bm_returns, total)


if __name__ == "__main__":
    main(sys.argv[1:])
