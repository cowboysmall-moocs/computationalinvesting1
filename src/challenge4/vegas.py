import sys
import random


black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35] 


def run_simulation(starting_amount, winning_margin, green_pockets):
    success_ammount = starting_amount + winning_margin
    current_stake   = 1
    total_pockets   = 35 + green_pockets

    while starting_amount < success_ammount and starting_amount > 0:
        if random.randint(0, total_pockets) in black:
            starting_amount += current_stake
        else:
            starting_amount -= current_stake
            current_stake *= 2

    return starting_amount > 0


def main(argv):
    total_iterations = int(argv[0])
    starting_amount  = int(argv[1])
    winning_margin   = int(argv[2])

    if len(argv) > 3:
        green_pockets = int(argv[3])
    else:
        green_pockets = 2

    success_count = 0

    for iterations in xrange(total_iterations):
        if run_simulation(starting_amount, winning_margin, green_pockets):
            success_count += 1

    winnings   = success_count * winning_margin
    losses     = (total_iterations - success_count) * starting_amount
    proportion = success_count / float(total_iterations)

    print
    print 'Vegas Simulation - %s iterations' % (total_iterations)
    print
    print ' Probability'
    print '       Successes: %15s' % (success_count)
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
