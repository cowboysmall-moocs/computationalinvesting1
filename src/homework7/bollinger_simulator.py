import sys
import csv

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da


from collections import defaultdict



def write_output(output_file, cash):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for index, row in cash.iterrows():
            writer.writerow([index.year, index.month, index.day, row['Total']])



def read_orders(input_file):
    symbols = []
    dates   = []
    orders  = defaultdict(list)

    with open(input_file, 'rU') as csvfile:
        for line in csv.reader(csvfile):
            date = dt.datetime(int(line[0]), int(line[1]), int(line[2]), 16)
            dates.append(date)
            symbols.append(line[3])
            orders[date].append((line[3], line[4], int(line[5])))

    symbols = list(set(symbols))
    dates   = list(set(dates))
    dates.sort()

    return symbols, dates, orders



def create_matrices(symbols, orders, timestamps):
    trades   = pd.DataFrame(index = timestamps, columns = symbols)
    trades   = trades.fillna(0)

    holdings = pd.DataFrame(index = timestamps, columns = symbols)
    holdings = holdings.fillna(0)

    for date, items in orders.items():
        for order in items:
            if order[1] == 'Buy':
                trades[order[0]].ix[date] += -order[2]
                holdings[order[0]].ix[date:timestamps[-1]] +=  order[2]
            else:
                trades[order[0]].ix[date] +=  order[2]
                holdings[order[0]].ix[date:timestamps[-1]] += -order[2]

    return trades, holdings



def create_cash(cash_value, trades, prices, timestamps):
    cash = pd.DataFrame(index = timestamps, columns = ['Cash'])

    for timestamp in timestamps:
        cash_value += np.sum(trades.ix[timestamp] * prices.ix[timestamp], axis = 1)
        cash['Cash'].ix[timestamp] = cash_value

    return cash



def file_name(output_dir, symbol_list, start_date, end_date):
    return '%s/bollinger_trading_strategy_simulation_%s_%s-%s.csv' % (
        output_dir, 
        symbol_list, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d')
    )



def main(argv):
    starting_cash = int(argv[0])
    symbol_list   = argv[1] #sp5002012
    input_file    = argv[2]
    output_dir    = argv[3]

    symbols, dates, orders = read_orders(input_file)

    timestamps = du.getNYSEdays(dates[0], dates[-1], dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    keys       = ['close', 'actual_close']
    data_dict  = dict(zip(keys, dataobj.get_data(timestamps, symbols, keys)))

    for key in keys:
        data_dict[key] = data_dict[key].fillna(method = 'ffill')
        data_dict[key] = data_dict[key].fillna(method = 'bfill')
        data_dict[key] = data_dict[key].fillna(1.0)

    prices           = data_dict['close']
    prices['Cash']   = 1

    trades, holdings = create_matrices(symbols, orders, timestamps)
    cash             = create_cash(starting_cash, trades, prices, timestamps)
    holdings['Cash'] = cash
    cash['Total']    = holdings.mul(prices, 1).sum(1)

    write_output(
        file_name(output_dir, symbol_list, dates[0], dates[-1]), 
        cash
    )



if __name__ == "__main__":
    main(sys.argv[1:])
