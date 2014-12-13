import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da


def plot_figure(timestamps, component_totals, portfolio_totals, portfolio_symbols):
    plt.clf()
    fig = plt.figure()
    fig.add_subplot(111)
    plt.plot(timestamps, component_totals, alpha = 0.4)
    plt.plot(timestamps, portfolio_totals)

    portfolio_symbols.append('Portfolio')
    plt.legend(portfolio_symbols)

    plt.ylabel('Cumulative Returns')
    plt.xlabel('Date')
    fig.autofmt_xdate(rotation = 45)

    plt.savefig('./src/week3/tutorial3.png', format = 'png')
    plt.close()


def main():
    na_portfolio = np.loadtxt('./src/week3/tutorial3.csv', dtype = 'S5,f4', delimiter = ',', comments = "#", skiprows = 1)
    na_portfolio = sorted(na_portfolio, key = lambda x: x[0])

    ls_port_syms  = []
    lf_port_alloc = []
    for port in na_portfolio:
        ls_port_syms.append(port[0])
        lf_port_alloc.append(port[1])

    c_dataobj   = da.DataAccess('Yahoo')
    ls_all_syms = c_dataobj.get_all_symbols()
    ls_bad_syms = list(set(ls_port_syms) - set(ls_all_syms))

    if len(ls_bad_syms) != 0:
        print "Portfolio contains bad symbols : ", ls_bad_syms

    for s_sym in ls_bad_syms:
        i_index = ls_port_syms.index(s_sym)
        ls_port_syms.pop(i_index)
        lf_port_alloc.pop(i_index)

    dt_end         = dt.datetime(2011, 1, 1)
    dt_start       = dt_end - dt.timedelta(days = 1095)
    dt_timeofday   = dt.timedelta(hours = 16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    ls_keys   = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data  = c_dataobj.get_data(ldt_timestamps, ls_port_syms, ls_keys)

    d_data  = dict(zip(ls_keys, ldf_data))
    df_rets = d_data['close'].copy()
    df_rets = df_rets.fillna(method = 'ffill')
    df_rets = df_rets.fillna(method = 'bfill')
    df_rets = df_rets.fillna(1.0)

    na_rets = df_rets.values
    tsu.returnize0(na_rets)

    na_portrets        = np.sum(na_rets * lf_port_alloc, axis = 1)
    na_port_total      = np.cumprod(na_portrets + 1)
    na_component_total = np.cumprod(na_rets + 1, axis = 0)

    plot_figure(ldt_timestamps, na_component_total, na_port_total, ls_port_syms)


if __name__ == '__main__':
    main()
