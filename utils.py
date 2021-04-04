from collections import defaultdict


def count_options(column):
    count = defaultdict(lambda: 0)
    for options in (row.split('; ') for row in column):
        for option in options:
            count[option] += 1
    return count