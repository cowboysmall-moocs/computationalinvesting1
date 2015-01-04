import sys
import random

import numpy as np
import matplotlib.pyplot as plt


def run_simulation(men, women, pool_size):
    married = 0

    while len(men) > 0 and max(men) > min(women):
        random.shuffle(men)
        random.shuffle(women)
        for man, woman in zip(men, women):
            if man > woman:
                married += 1
                men.remove(man)
                women.remove(woman)

    return float(married) / pool_size


def print_results(results, title):
    print
    print '                    %s' % (title)
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


def plot_results(results, title):
    plt.hist(results, normed = True)
    plt.title(title)
    plt.xlabel('Married')
    plt.ylabel('Frequency')
    plt.show()


def main(argv):
    pool_size  = int(argv[0])
    iterations = int(argv[1])

    uniform = []
    for _ in xrange(iterations):
        men     = np.random.random_integers(0, 200, pool_size).tolist()
        women   = np.random.random_integers(0, 200, pool_size).tolist()
        uniform.append(run_simulation(men, women, pool_size))

    normal = []
    for _ in xrange(iterations):
        men     = np.random.normal(100, 33, pool_size).tolist()
        women   = np.random.normal(100, 33, pool_size).tolist()
        normal.append(run_simulation(men, women, pool_size))

    even = []
    for _ in xrange(iterations):
        men     = [200 * (float(val) / pool_size) for val in xrange(pool_size)]
        women   = [200 * (float(val) / pool_size) for val in xrange(pool_size)]
        even.append(run_simulation(men, women, pool_size))

    print_results(uniform, 'Marriage (Uniform)')
    print_results(normal, 'Marriage (Normal)')
    print_results(even, 'Marriage (Even)')
    plot_results(uniform, 'Marriage (Uniform)')
    plot_results(normal, 'Marriage (Normal)')
    plot_results(even, 'Marriage (Even)')


if __name__ == "__main__":
    main(sys.argv[1:])
