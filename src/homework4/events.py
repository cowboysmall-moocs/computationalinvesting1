import sys
import csv

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil     as du
import QSTK.qstkutil.DataAccess     as da
import QSTK.qstkutil.tsutil         as tsu
import QSTK.qstkstudy.EventProfiler as ep


def write_output(output_file, trades):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for trade in trades:
            writer.writerow([trade[0].year, trade[0].month, trade[0].day, trade[1], trade[2], trade[3], ''])


def find_events(symbols, data, threshold):
    close      = data['actual_close']
    timestamps = close.index
    trades     = []

    for symbol in symbols:
        for i in xrange(1, len(timestamps)):
            symbol_price_today     = close[symbol].ix[timestamps[i]]
            symbol_price_yesterday = close[symbol].ix[timestamps[i - 1]]
            if symbol_price_today < threshold and symbol_price_yesterday >= threshold:
                trades.append((timestamps[i], symbol, 'Buy', 100))
                if len(timestamps) - i < 6:
                    trades.append((timestamps[-1], symbol, 'Sell', 100))
                else:
                    trades.append((timestamps[i + 5], symbol, 'Sell', 100))

    return trades


def main(argv):
    start_date  = dt.datetime.strptime(argv[0], "%Y-%m-%d")
    end_date    = dt.datetime.strptime(argv[1], "%Y-%m-%d")
    threshold   = float(argv[2])
    symbol_list = argv[3] #sp5002012

    timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    symbols    = dataobj.get_symbols_from_list(symbol_list)
    symbols.append('SPY')

    keys       = ['close', 'actual_close']
    data       = dataobj.get_data(timestamps, symbols, keys)
    data_dict  = dict(zip(keys, data))

    for key in keys:
        data_dict[key] = data_dict[key].fillna(method = 'ffill')
        data_dict[key] = data_dict[key].fillna(method = 'bfill')
        data_dict[key] = data_dict[key].fillna(1.0)

    trades = find_events(symbols, data_dict, threshold)

    write_output(argv[4], trades)


if __name__ == "__main__":
    main(sys.argv[1:])

