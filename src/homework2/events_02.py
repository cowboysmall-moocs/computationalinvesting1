import sys
import copy

import datetime as dt
import pandas   as pd
import numpy    as np

import QSTK.qstkutil.qsdateutil     as du
import QSTK.qstkutil.DataAccess     as da
import QSTK.qstkutil.tsutil         as tsu
import QSTK.qstkstudy.EventProfiler as ep


def find_events(symbols, data, threshold):
    close      = data['actual_close']
    events     = copy.deepcopy(close)
    events     = events * np.NAN
    timestamps = close.index

    for symbol in symbols:
        for i in xrange(1, len(timestamps)):
            symbol_price_today     = close[symbol].ix[timestamps[i]]
            symbol_price_yesterday = close[symbol].ix[timestamps[i - 1]]
            if symbol_price_today < threshold and symbol_price_yesterday >= threshold:
                events[symbol].ix[timestamps[i]] = 1

    return events


def file_name(output_dir, symbol_list, start_date, end_date):
    return '%s/event_study_%s_%s-%s.pdf' % (
        output_dir, 
        symbol_list, 
        start_date.strftime('%Y%m%d'), 
        end_date.strftime('%Y%m%d')
    )


def main(argv):
    start_date  = dt.datetime.strptime(argv[0], "%Y-%m-%d")
    end_date    = dt.datetime.strptime(argv[1], "%Y-%m-%d")
    threshold   = float(argv[2])
    symbol_list = argv[3] #sp5002012
    output_dir  = argv[4]

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

    events = find_events(symbols, data_dict, threshold)

    ep.eventprofiler(
        events, 
        data_dict, 
        i_lookback = 20, 
        i_lookforward = 20,
        s_filename = file_name(output_dir, symbol_list, start_date, end_date), 
        b_market_neutral = True, 
        b_errorbars = True,
        s_market_sym = 'SPY'
    )


if __name__ == "__main__":
    main(sys.argv[1:])
