import sys
import csv

import datetime          as dt
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da



def bollinger_bands(timestamps, close, symbol):
    bollinger = pd.DataFrame(index = timestamps, columns = ['price', 'mean', 'upper', 'lower', 'value'])
    bollinger = bollinger.fillna(0)

    rolling_mean       = pd.rolling_mean(close[symbol], 20)
    rolling_std        = pd.rolling_std(close[symbol], 20)

    bollinger['price'] = close[symbol]
    bollinger['mean']  = rolling_mean
    bollinger['upper'] = rolling_mean + rolling_std
    bollinger['lower'] = rolling_mean - rolling_std
    bollinger['value'] = (close[symbol] - rolling_mean) / rolling_std

    return bollinger



def plot_bollinger(timestamps, bollinger, symbol, filepath, xlabel = 'Date', ylabel = 'Adjusted Close'):
    plt.clf()

    f, axarr = plt.subplots(2, sharex = True)

    axarr[0].plot(timestamps, bollinger['price'], color = 'blue')
    axarr[0].plot(timestamps, bollinger['mean'], color = 'red')
    axarr[0].plot(timestamps, bollinger['upper'], color = 'grey')
    axarr[0].plot(timestamps, bollinger['lower'], color = 'grey')
    axarr[0].fill_between(timestamps, bollinger['lower'], bollinger['upper'], facecolor = 'grey', alpha = 0.1)
    axarr[0].legend([symbol], loc = 2)
    axarr[0].set_ylabel('Adjusted Close')

    axarr[1].plot(timestamps, bollinger['value'], color = 'blue')
    axarr[1].fill_between(timestamps, -1, 1, facecolor = 'grey', alpha = 0.1)
    axarr[1].set_ylabel('Bollinger Feature')

    f.autofmt_xdate(rotation = 45)

    plt.savefig(filepath, format = 'png')
    plt.close()



def write_bollinger(start_date, end_date, bollinger, symbol, filepath):
    with open(filepath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for index, row in bollinger.iterrows():
            writer.writerow([index.year, index.month, index.day, row['value']])



def file_name(output_dir, symbol, start_date, end_date, file_type = 'png'):
    return '%s/bollinger_%s_%s-%s.%s' % (
        output_dir, 
        symbol, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d'), 
        file_type
    )



def main(argv):
    symbol     = argv[0]
    start_date = dt.datetime.strptime(argv[1], "%Y-%m-%d")
    end_date   = dt.datetime.strptime(argv[2], "%Y-%m-%d")
    image_dir  = argv[3]
    data_dir   = argv[4]

    timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    keys       = ['close', 'actual_close']
    data       = dataobj.get_data(timestamps, [symbol], keys)
    data_dict  = dict(zip(keys, data))

    for key in keys:
        data_dict[key] = data_dict[key].fillna(method = 'ffill')
        data_dict[key] = data_dict[key].fillna(method = 'bfill')
        data_dict[key] = data_dict[key].fillna(1.0)

    bollinger  = bollinger_bands(timestamps, data_dict['close'], symbol)

    plot_bollinger(
        timestamps, 
        bollinger, 
        symbol, 
        file_name(image_dir, symbol, timestamps[0], timestamps[-1])
    )

    write_bollinger(
        timestamps[0], 
        timestamps[-1], 
        bollinger,
        symbol, 
        file_name(data_dir, symbol, timestamps[0], timestamps[-1], 'csv')
    )

    # for index, row in bollinger[-20:].iterrows():
    #     print '%s: %12.6f' % (index, row['value'])



if __name__ == "__main__":
    main(sys.argv[1:])
