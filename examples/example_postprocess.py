#!/usr/bin/env python
import fileinput
import random
import sys

# generate a list of symbols via ascii code
SYMBOLS = [str(unichr(i)) for i in range(33, 65)]


def rng_delimitor(password):
    words = password.split()
    n_words = len(words)

    # zip the split password and an equivalent number of symbols
    # join, and drop the first symbol
    return " ".join(i for l in zip(
        [random.choice(SYMBOLS) for _ in range(n_words)],
        words
    ) for i in l)[2:]


if __name__ == "__main__":
    # fileinput.input allows us to iterate over stdin
    for line in fileinput.input():
        rng_delim_line = rng_delimitor(line)
        sys.stdout.write(rng_delim_line + "\n")
