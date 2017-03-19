#!/usr/bin/env python
import sys
import fileinput
import random

SYMBOLS = [str(unichr(i)) for i in range(33, 65)]


def rng_delimitor(password):
    words = password.split()
    n_words = len(words)

    return " ".join(i for l in zip(
        [random.choice(SYMBOLS) for _ in range(n_words)],
        words
    ) for i in l)[2:]


if __name__ == "__main__":
    for line in fileinput.input():
        rng_delim_line = rng_delimitor(line)
        sys.stdout.write(rng_delim_line + "\n")
