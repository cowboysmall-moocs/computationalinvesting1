import sys
import random


def run_simulation(starting_amount, winning_margin):
    success_ammount = starting_amount + winning_margin
    current_stake   = 1

    while starting_amount < success_ammount and starting_amount > 0:
        if random.randint(0, 1) == 1:
            starting_amount += current_stake
        else:
            starting_amount -= current_stake
            current_stake *= 2

    return starting_amount > 0


def main(argv):
    total_iterations = int(argv[0])
    starting_amount  = int(argv[1])
    winning_margin   = int(argv[2])

    success_count = 0

    for iterations in xrange(total_iterations):
        if run_simulation(starting_amount, winning_margin):
            success_count += 1

    winnings   = success_count * winning_margin
    losses     = (total_iterations - success_count) * starting_amount
    proportion = success_count / float(total_iterations)

    print
    print 'Vegas Simulation - %s iterations' % (total_iterations)
    print
    print ' Probability'
    print '       Successes: %15s'   % (success_count)
    print '      Proportion: %15.2f' % (proportion)
    print ' Expected Profit: %15.2f' % ((proportion * winning_margin) - ((1 - proportion) * starting_amount))
    print
    print ' Balance Sheet'
    print '  Total Winnings: %15.2f' % (winnings)
    print '    Total Losses: %15.2f' % (losses)
    print '   Actual Profit: %15.2f' % (winnings - losses)
    print
    print


if __name__ == "__main__":
    main(sys.argv[1:])
