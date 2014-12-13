import sys
import csv

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da


def write_output(output_file, cash):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for index, row in cash.iterrows():
            writer.writerow([index.year, index.month, index.day, row['Total']])


def read_orders(input_file):
    dates = []
    names = ['Year', 'Month', 'Day', 'Symbol', 'Action', 'Count', '']

    orders = pd.read_csv(input_file, header = None, names = names)
    for index, row in orders.iterrows():
        dates.append(dt.datetime(int(row['Year']), int(row['Month']), int(row['Day'])) + dt.timedelta(hours = 16))
    orders = orders.set_index(pd.Series(dates))[['Symbol', 'Action', 'Count']].sort()

    symbols = list(set(orders['Symbol']))
    dates.sort()

    return dates, symbols, orders


def read_prices(start, end, symbols):
    timestamps = du.getNYSEdays(start, end, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    return timestamps, dataobj.get_data(timestamps, symbols, ['close'])[0]


def create_matrices(timestamps, symbols, orders):
    trades   = pd.DataFrame(index = timestamps, columns = symbols)
    trades   = trades.fillna(0)

    holdings = pd.DataFrame(index = timestamps, columns = symbols)
    holdings = holdings.fillna(0)

    for index, row in orders.iterrows():
        if row['Action'] == 'Buy':
            trades[row['Symbol']].ix[index] += -row['Count']
            holdings[row['Symbol']].ix[index:timestamps[-1]] +=  row['Count']
        else:
            trades[row['Symbol']].ix[index] +=  row['Count']
            holdings[row['Symbol']].ix[index:timestamps[-1]] += -row['Count']

    return trades, holdings


def create_cash(timestamps, trades, holdings, prices, cash_value):
    cash   = pd.DataFrame(index = timestamps, columns = ['Cash'])
    totals = pd.DataFrame(index = timestamps, columns = ['Total'])

    for timestamp in timestamps:
        cash_value     += np.sum(trades.ix[timestamp] * prices.ix[timestamp], axis = 1)
        portfolio_value = np.sum(holdings.ix[timestamp] * prices.ix[timestamp], axis = 1)
        cash['Cash'].ix[timestamp]   = cash_value
        totals['Total'].ix[timestamp] = cash_value + portfolio_value

    return cash, totals


def main(argv):
    starting_cash = int(argv[0])
    input_file    = argv[1]
    output_file   = argv[2]

    dates, symbols, orders = read_orders(input_file)
    timestamps, prices     = read_prices(dates[0], dates[-1], symbols)
    trades, holdings       = create_matrices(timestamps, symbols, orders)
    cash, totals           = create_cash(timestamps, trades, holdings, prices, starting_cash)

    write_output(output_file, totals)


if __name__ == "__main__":
    main(sys.argv[1:])
