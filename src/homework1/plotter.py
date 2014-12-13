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
