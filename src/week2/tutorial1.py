import sys

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_timeseries(symbols, timestamps, prices, filepath, xlabel = 'Date', ylabel = 'Close'):
    plt.clf()
    plt.plot(timestamps, prices)
    plt.legend(symbols)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filepath, format = 'png')
    plt.close()


def plot_returns(timestamps, returns1, returns2, legend1, legend2, filepath, xlabel = 'Date', ylabel = 'Daily Returns'):
    plt.clf()
    plt.plot(timestamps, returns1)
    plt.plot(timestamps, returns2)
    plt.axhline(y = 0, color = 'r')
    plt.legend([legend1, legend2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filepath, format = 'png')
    plt.close()


def plot_scatter(returns1, returns2, filepath, xlabel, ylabel):
    plt.clf()
    plt.scatter(returns1, returns2, c = 'blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filepath, format = 'png')
    plt.close()


def main(argv):
    dt_start       = dt.datetime(2006, 1, 1)
    dt_end         = dt.datetime(2010, 12, 31)
    dt_timeofday   = dt.timedelta(hours = 16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    ls_symbols     = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
    ls_keys        = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    c_dataobj      = da.DataAccess('Yahoo')
    ldf_data       = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data         = dict(zip(ls_keys, ldf_data))
    na_price       = d_data['close'].values
    plot_timeseries(ls_symbols, ldt_timestamps, na_price, './src/week2/close1.png', ylabel = 'Adjusted Close')

    na_normalized_price = na_price / na_price[0, :]
    plot_timeseries(ls_symbols, ldt_timestamps, na_normalized_price, './src/week2/close2.png', ylabel = 'Normalized Close')

    na_rets        = na_normalized_price.copy()
    tsu.returnize0(na_rets)
    plot_returns(ldt_timestamps[0:50], na_rets[0:50, 3], na_rets[0:50, 4], '$SPX', 'XOM', './src/week2/returns1.png', ylabel = 'Daily Returns')

    plot_scatter(na_rets[:, 3], na_rets[:, 4], './src/week2/scatter1.png', '$SPX', 'XOM')
    plot_scatter(na_rets[:, 3], na_rets[:, 1], './src/week2/scatter2.png', '$SPX', 'GLD')

    # na_cum_rets    = np.cumprod(na_price + 1, axis = 0)
    # plot_timeseries(ls_symbols, ldt_timestamps, na_cum_rets, './src/week2/close3.png', ylabel = 'Cumulative Daily Returns')


if __name__ == "__main__":
    main(sys.argv[1:])
