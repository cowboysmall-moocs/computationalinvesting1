import sys
import csv

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

from collections import defaultdict


def write_output(output_file, totals):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for total in totals:
            writer.writerow([total[0].year, total[0].month, total[0].day, total[1]])


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


def read_prices(start, end, symbols):
    timestamps = du.getNYSEdays(start, end, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    return timestamps, dataobj.get_data(timestamps, symbols, ['close'])[0]


def calculate_cash_value(date, orders, stocks, prices):
    total = 0.0

    for order in orders[date]:
        if order[1] == 'Buy':
            total -= order[2] * prices[order[0]].ix[date]
            stocks[order[0]] += order[2]
        else:
            total += order[2] * prices[order[0]].ix[date]
            stocks[order[0]] -= order[2]

    return total


def calculate_stock_value(date, stocks, prices):
    total = 0.0

    for symbol, count in stocks.items():
        total += count * prices[symbol].ix[date]

    return total


def calculate_totals(cash_total, timestamps, orders, stocks, prices):
    totals = []

    for timestamp in timestamps:
        if timestamp in orders:
            cash_total += calculate_cash_value(timestamp, orders, stocks, prices)
        stock_total = calculate_stock_value(timestamp, stocks, prices)
        totals.append((timestamp, cash_total + stock_total))

    return totals


def main(argv):
    starting_cash = int(argv[0])
    input_file    = argv[1]
    output_file   = argv[2]

    stocks = defaultdict(int)

    symbols, dates, orders = read_orders(input_file)
    timestamps, prices     = read_prices(dates[0], dates[-1], symbols)
    totals                 = calculate_totals(starting_cash, timestamps, orders, stocks, prices)

    write_output(output_file, totals)


if __name__ == "__main__":
    main(sys.argv[1:])
