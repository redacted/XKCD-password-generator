#!/usr/bin/env python
# encoding: utf-8

import random
import os

def generate_wordlist(min_length=5, max_length=9):
    ## OS X
    # word_list = "/usr/share/dict/words"
    ## Linux
    # word_list = "/usr/dict/words"
    ## Downloaded || custom
    word_list = os.path.expanduser("~/local/share/dict/common")

    words = []

    try:
        with open(word_list) as wlf:
            for line in wlf:
                if min_length <= len(line.strip()) <= max_length:
                    words.append(line.strip())
    except:
            print 'File not found.'
            raise SystemExit
    return words

if __name__ == '__main__':
    n_words = raw_input("Enter number of words (default 4): ")
    if not n_words: n_words = 4
    else: n_words = int(n_words)
    
    accepted = "n"
    wordlist = generate_wordlist()

    while accepted.lower() not in [ "y", "yes" ]:
        try:
            passwd = " ".join(random.SystemRandom().sample(wordlist, n_words))
        except NotImplementedError:
            print 'System does not support random number generator or Python version < 2.4.'
        print "Generated: ", passwd
        accepted = raw_input("Accept? [yN] ")


