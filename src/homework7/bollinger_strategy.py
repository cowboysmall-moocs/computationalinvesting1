import sys
import csv

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil     as du
import QSTK.qstkutil.DataAccess     as da
import QSTK.qstkstudy.EventProfiler as ep



def write_output(output_file, trades):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for trade in trades:
            writer.writerow([trade[0].year, trade[0].month, trade[0].day, trade[1], trade[2], trade[3], ''])



def find_trades(symbols, data, timestamps):
    trades = []

    for symbol in symbols[:-1]:
        for i in xrange(1, len(timestamps)):
            value_today     = data[symbol].ix[timestamps[i]]
            value_yesterday = data[symbol].ix[timestamps[i - 1]]
            spy_today       = data['SPY'].ix[timestamps[i]]
            # if value_today < -2.0 and value_yesterday >= -2.0 and spy_today >= 1.1:
            if value_today <= -2.0 and value_yesterday >= -2.0 and spy_today >= 1:
                trades.append((timestamps[i], symbol, 'Buy', 100))
                if len(timestamps) - i < 6:
                    trades.append((timestamps[-1], symbol, 'Sell', 100))
                else:
                    trades.append((timestamps[i + 5], symbol, 'Sell', 100))

    return trades



def bollinger_bands(symbols, data, timestamps):
    bollinger = pd.DataFrame(index = timestamps, columns = symbols)
    bollinger = bollinger.fillna(0)

    for symbol in symbols:
        rolling_mean      = pd.rolling_mean(data[symbol], 20)
        rolling_std       = pd.rolling_std(data[symbol], 20)
        bollinger[symbol] = (data[symbol] - rolling_mean) / rolling_std

    return bollinger



def file_name(output_dir, symbol_list, start_date, end_date):
    return '%s/bollinger_trading_strategy_output_%s_%s-%s.csv' % (
        output_dir, 
        symbol_list, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d')
    )



def main(argv):
    start_date  = dt.datetime.strptime(argv[0], "%Y-%m-%d")
    end_date    = dt.datetime.strptime(argv[1], "%Y-%m-%d")
    symbol_list = argv[2] #sp5002012
    output_dir  = argv[3]

    timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    symbols    = dataobj.get_symbols_from_list(symbol_list)
    symbols.append('SPY')

    keys       = ['close', 'actual_close']
    data_dict  = dict(zip(keys, dataobj.get_data(timestamps, symbols, keys)))

    for key in keys:
        data_dict[key] = data_dict[key].fillna(method = 'ffill')
        data_dict[key] = data_dict[key].fillna(method = 'bfill')
        data_dict[key] = data_dict[key].fillna(1.0)

    bollinger = bollinger_bands(symbols, data_dict['close'], timestamps)
    trades    = find_trades(symbols, bollinger, timestamps)

    write_output(
        file_name(output_dir, symbol_list, start_date, end_date), 
        trades
    )



if __name__ == "__main__":
    main(sys.argv[1:])
