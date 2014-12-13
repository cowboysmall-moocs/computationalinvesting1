import sys
import csv
import random

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


def read_data(file_path):
    data = []

    with open(file_path) as file:
        file.readline()

        for row in csv.reader(file):
            data.append((int(row[1]), float(row[2]) / 1.96))

    return data


def run_simulation(data):
    success = 0

    for params in data:
        if random.gauss(params[0], params[1]) > 0:
            success += 1

    return success


def print_results(results):
    print
    print '           Minimum: %s' % (np.amin(results))
    print '   25th Percentile: %s' % (np.percentile(results, 25))
    print '            Median: %s' % (np.median(results))
    print '   75th Percentile: %s' % (np.percentile(results, 75))
    print '           Maximum: %s' % (np.amax(results))
    print
    print '              Mean: %s' % (np.mean(results))
    print 'Standard Deviation: %s' % (np.std(results))
    print '          Variance: %s' % (np.var(results))
    print
    print ' Victory (Percent): %s' % (float(sum(i > 20 for i in results)) / len(results))
    print ' Victory (P-Value): %s' % (1 - st.norm(np.mean(results), np.std(results)).cdf(21))
    print


def plot_results(results):
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = True)
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Frequency')
    plt.show()


def main(argv):
    data = read_data(argv[0])

    results   = []
    for _ in xrange(int(argv[1])):
        results.append(run_simulation(data))

    print_results(results)
    plot_results(results)


if __name__ == "__main__":
    main(sys.argv[1:])
