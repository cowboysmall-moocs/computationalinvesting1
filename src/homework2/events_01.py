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


def main(argv):
    start      = dt.datetime(2008, 1, 1)
    end        = dt.datetime(2009, 12, 31)

    timestamps = du.getNYSEdays(start, end, dt.timedelta(hours = 16))
    dataobj    = da.DataAccess('Yahoo')

    symbols_2008 = dataobj.get_symbols_from_list('sp5002008')
    symbols_2008.append('SPY')
    symbols_2012 = dataobj.get_symbols_from_list('sp5002012')
    symbols_2012.append('SPY')

    keys       = ['close', 'actual_close']
    data_2008  = dataobj.get_data(timestamps, symbols_2008, keys)
    data_2012  = dataobj.get_data(timestamps, symbols_2012, keys)
    dict_2008  = dict(zip(keys, data_2008))
    dict_2012  = dict(zip(keys, data_2012))

    for key in keys:
        dict_2008[key] = dict_2008[key].fillna(method = 'ffill')
        dict_2008[key] = dict_2008[key].fillna(method = 'bfill')
        dict_2008[key] = dict_2008[key].fillna(1.0)
        dict_2012[key] = dict_2012[key].fillna(method = 'ffill')
        dict_2012[key] = dict_2012[key].fillna(method = 'bfill')
        dict_2012[key] = dict_2012[key].fillna(1.0)

    events_2008 = find_events(symbols_2008, dict_2008, 10.0)
    ep.eventprofiler(
        events_2008, 
        dict_2008, 
        i_lookback = 20, 
        i_lookforward = 20,
        s_filename = './src/homework2/output/event_study_2008.pdf', 
        b_market_neutral = True, 
        b_errorbars = True,
        s_market_sym = 'SPY'
    )

    events_2012 = find_events(symbols_2012, dict_2012, 8.0)
    ep.eventprofiler(
        events_2012, 
        dict_2012, 
        i_lookback = 20, 
        i_lookforward = 20,
        s_filename = './src/homework2/output/event_study_2012.pdf', 
        b_market_neutral = True, 
        b_errorbars = True,
        s_market_sym = 'SPY'
    )


if __name__ == "__main__":
    main(sys.argv[1:])
