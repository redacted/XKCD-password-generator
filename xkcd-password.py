#!/usr/bin/env python
# encoding: utf-8

import random
import os
import optparse
import re
import math
import sys

__LICENSE__ = """
Copyright (c) 2011, 2012, Steven Tobin and Contributors.
All rights reserved.

Contributors: Steven Tobin,
              Rob Lanphier <robla@robla.net>,
              Mithrandir <mithrandiragain@lavabit.com>,
              Daniel Beecham <daniel@lunix.se>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# random.SystemRandom() should be cryptographically secure
try:
    rng = random.SystemRandom
except AttributeError:
    sys.stderr.write("WARNING: System does not support cryptographically "
                     "secure random number generator or you are using Python "
                     "version < 2.4.\n"
                     "Continuing with less-secure generator.\n")
    rng = random.Random

# Python 3 compatibility
if sys.version[0] == "3":
    raw_input = input


def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """

    if options.max_length < options.min_length:
        sys.stderr.write("The maximum length of a word can not be "
                         "lesser then minimum length.\n"
                         "Check the specified settings.\n")
        sys.exit(1)

    if len(args) > 1:
        parser.error("Too many arguments.")

    if len(args) == 1:
        # supporting either -w or args[0] for wordlist, but not both
        if options.wordfile is None:
            options.wordfile = args[0]
        elif options.wordfile == args[0]:
            pass
        else:
            parser.error("Conflicting values for wordlist: " + args[0] +
                         " and " + options.wordfile)

    if options.wordfile is not None:
        if not os.path.exists(os.path.abspath(options.wordfile)):
            sys.stderr.write("Could not open the specified word file.\n")
            sys.exit(1)
    else:
        common_word_files = ["/usr/share/dict/words",
                             "/usr/dict/words"]

        for wfile in common_word_files:
            if os.path.exists(wfile):
                options.wordfile = wfile
                break

        if options.wordfile is None:
            sys.stderr.write("Could not find a word file, or word file does "
                             "not exist.\n")
            sys.exit(1)


def generate_wordlist(wordfile=None,
                      min_length=5,
                      max_length=9,
                      valid_chars='.'):
    """
    Generate a word list from either a kwarg wordfile, or a system default
    valid_chars is a regular expression match condition (default - all chars)
    """

    words = []

    regexp = re.compile("^%s{%i,%i}$" % (valid_chars, min_length, max_length))

    # At this point wordfile is set
    wordfile = os.path.expanduser(wordfile)  # just to be sure
    wlf = open(wordfile)

    for line in wlf:
        thisword = line.strip()
        if regexp.match(thisword) is not None:
            words.append(thisword)

    wlf.close()

    return words


def verbose_reports(length, options):
    """
    Report entropy metrics based on word list and requested password size"
    """

    numwords = options.numwords
    bits = math.log(length, 2)

    print("The supplied word list is located at %s."
          % os.path.abspath(options.wordfile))

    if (int(bits) == bits):
        print("Your word list contains %i words, or 2^%i words."
              % (length, bits))
    else:
        print("Your word list contains %i words, or 2^%0.2f words."
              % (length, bits))

    print("A %i word password from this list will have roughly "
          "%i (%0.2f * %i) bits of entropy, " %
          (numwords, int(bits * numwords), bits, numwords)),
    print("assuming truly random word selection.")


def generate_xkcdpassword(wordlist, n_words=4, interactive=False):
    """
    Generate an XKCD-style password from the words in wordlist.
    """

    if len(wordlist) < n_words:
        sys.stderr.write("Could not get enough words!\n"
                         "This could be a result of either your wordfile\n"
                         "being too small, or your settings too strict.\n")
        sys.exit(1)

    # useful if driving the logic from other code
    if not interactive:
        return " ".join(rng().sample(wordlist, n_words))

    # else, interactive session
    custom_n_words = raw_input("Enter number of words (default 4): ")

    if custom_n_words:
        n_words = int(custom_n_words)

    accepted = "n"

    while accepted.lower() not in ["y", "yes"]:
        passwd = " ".join(rng().sample(wordlist, n_words))
        print("Generated: ", passwd)
        accepted = raw_input("Accept? [yN] ")

    return passwd


if __name__ == '__main__':

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-w", "--wordfile", dest="wordfile",
                      default=None,
                      help="List of valid words for password")
    parser.add_option("--min", dest="min_length",
                      default=5, type="int",
                      help="Minimum length of words to make password")
    parser.add_option("--max", dest="max_length",
                      default=9, type="int",
                      help="Maximum length of words to make password")
    parser.add_option("-n", "--numwords", dest="numwords",
                      default=4, type="int",
                      help="Number of words to make password")
    parser.add_option("-i", "--interactive", dest="interactive",
                      default=False, action="store_true",
                      help="Interactively select a password")
    parser.add_option("-v", "--valid_chars", dest="valid_chars",
                      default='.',
                      help="Valid chars, using regexp style (e.g. '[a-z]')")
    parser.add_option("-V", "--verbose", dest="verbose",
                      default=False, action="store_true",
                      help="Report various metrics for given options")

    (options, args) = parser.parse_args()
    validate_options(options, args)

    my_wordlist = generate_wordlist(wordfile=options.wordfile,
                                    min_length=options.min_length,
                                    max_length=options.max_length,
                                    valid_chars=options.valid_chars)

    if options.verbose:
        verbose_reports(len(my_wordlist), options)

    print(generate_xkcdpassword(my_wordlist, interactive=options.interactive,
                                n_words=options.numwords))
