#!/usr/bin/env python
# encoding: utf-8

import random
import os
import os.path
import argparse
import re
import math
import sys

__LICENSE__ = """
Copyright (c) 2011 - 2017, Steven Tobin and Contributors.
All rights reserved.

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
except AttributeError as ex:
    sys.stderr.write("WARNING: System does not support cryptographically "
                     "secure random number generator or you are using Python "
                     "version < 2.4.\n")
    if "XKCDPASS_ALLOW_WEAKRNG" in os.environ or \
       "--allow-weak-rng" in sys.argv:
        sys.stderr.write("Continuing with less-secure generator.\n")
        rng = random.Random
    else:
        raise ex


# Python 3 compatibility
if sys.version_info[0] >= 3:
    raw_input = input
    xrange = range


def validate_options(parser, options):
    """
    Given a parsed collection of options, performs various validation checks.
    """

    if options.max_length < options.min_length:
        sys.stderr.write("The maximum length of a word can not be "
                         "less than the minimum length.\n"
                         "Check the specified settings.\n")
        sys.exit(1)

    if options.wordfile is not None:
        if not os.path.isfile(os.path.abspath(options.wordfile)):
            sys.stderr.write("Could not open the specified word file.\n")
            sys.exit(1)
    else:
        options.wordfile = locate_wordfile()

        if not options.wordfile:
            sys.stderr.write("Could not find a word file, or word file does "
                             "not exist.\n")
            sys.exit(1)


def locate_wordfile():
    static_default = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static',
        'default.txt')
    common_word_files = ["/usr/share/cracklib/cracklib-small",
                         "/usr/share/dict/cracklib-small",
                         static_default,
                         "/usr/dict/words",
                         "/usr/share/dict/words"]

    for wfile in common_word_files:
        if os.path.isfile(wfile):
            return wfile


def generate_wordlist(wordfile=None,
                      min_length=5,
                      max_length=9,
                      valid_chars='.'):
    """
    Generate a word list from either a kwarg wordfile, or a system default
    valid_chars is a regular expression match condition (default - all chars)
    """

    if wordfile is None:
        wordfile = locate_wordfile()

    words = []

    regexp = re.compile("^{0}{{{1},{2}}}$".format(valid_chars,
                                                  min_length,
                                                  max_length))

    # At this point wordfile is set
    wordfile = os.path.expanduser(wordfile)  # just to be sure

    # read words from file into wordlist
    with open(wordfile) as wlf:
        for line in wlf:
            thisword = line.strip()
            if regexp.match(thisword) is not None:
                words.append(thisword)

    return list(set(words))  # deduplicate, just in case


def wordlist_to_worddict(wordlist):
    """
    Takes a wordlist and returns a dictionary keyed by the first letter of
    the words. Used for acrostic pass phrase generation
    """

    worddict = {}

    # Maybe should be a defaultdict, but this reduces dependencies
    for word in wordlist:
        try:
            worddict[word[0]].append(word)
        except KeyError:
            worddict[word[0]] = [word, ]

    return worddict


def verbose_reports(length, numwords, wordfile):
    """
    Report entropy metrics based on word list and requested password size"
    """

    bits = math.log(length, 2)

    print("The supplied word list is located at"
          " {0}.".format(os.path.abspath(wordfile)))

    if int(bits) == bits:
        print("Your word list contains {0} words, or 2^{1} words."
              "".format(length, bits))
    else:
        print("Your word list contains {0} words, or 2^{1:.2f} words."
              "".format(length, bits))

    print("A {0} word password from this list will have roughly "
          "{1} ({2:.2f} * {3}) bits of entropy,"
          "".format(numwords, int(bits * numwords), bits, numwords)),
    print("assuming truly random word selection.")


def find_acrostic(acrostic, worddict):
    """
    Constrain choice of words to those beginning with the letters of the
    given word (acrostic).
    Second argument is a dictionary (output of wordlist_to_worddict)
    """

    words = []

    for letter in acrostic:
        try:
            words.append(rng().choice(worddict[letter]))
        except KeyError:
            sys.stderr.write("No words found starting with " + letter + "\n")
            sys.exit(1)
    return words


def choose_words(wordlist, numwords):
    """
    Choose numwords randomly from wordlist
    """

    return [rng().choice(wordlist) for i in xrange(numwords)]


def try_input(prompt, validate):
    """
    Suppress stack trace on user cancel and validate input with supplied
    validate callable.
    """

    try:
        answer = raw_input(prompt)
    except (KeyboardInterrupt, EOFError):
        # user cancelled
        print("")
        sys.exit(0)

    # validate input
    return validate(answer)


def generate_xkcdpassword(wordlist,
                          numwords=6,
                          interactive=False,
                          acrostic=False,
                          delimiter=" "):
    """
    Generate an XKCD-style password from the words in wordlist.
    """

    passwd = None

    # generate the worddict if we are looking for acrostics
    if acrostic:
        worddict = wordlist_to_worddict(wordlist)

    # useful if driving the logic from other code
    if not interactive:
        if not acrostic:
            passwd = delimiter.join(choose_words(wordlist, numwords))
        else:
            passwd = delimiter.join(find_acrostic(acrostic, worddict))

        return passwd

    # else, interactive session
    # define input validators
    def n_words_validator(answer):
        """
        Validate custom number of words input
        """

        if isinstance(answer, str) and len(answer) == 0:
            return numwords
        try:
            number = int(answer)
            if number < 1:
                raise ValueError
            return number
        except ValueError:
            sys.stderr.write("Please enter a positive integer\n")
            sys.exit(1)

    def accepted_validator(answer):
        return answer.lower().strip() in ["y", "yes"]

    if not acrostic:
        n_words_prompt = ("Enter number of words (default {0}):"
                          " ".format(numwords))

        numwords = try_input(n_words_prompt, n_words_validator)
    else:
        numwords = len(acrostic)

    # generate passwords until the user accepts
    accepted = False

    while not accepted:
        if not acrostic:
            passwd = delimiter.join(choose_words(wordlist, numwords))
        else:
            passwd = delimiter.join(find_acrostic(acrostic, worddict))
        print("Generated: " + passwd)
        accepted = try_input("Accept? [yN] ", accepted_validator)

    return passwd


def emit_passwords(wordlist, options):
    """ Generate the specified number of passwords and output them. """
    count = options.count
    while count > 0:
        print(generate_xkcdpassword(
            wordlist,
            interactive=options.interactive,
            numwords=options.numwords,
            acrostic=options.acrostic,
            delimiter=options.delimiter))
        count -= 1


class XkcdPassArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for this program. """

    def __init__(self, *args, **kwargs):
        super(XkcdPassArgumentParser, self).__init__(*args, **kwargs)

        self._add_arguments()

    def _add_arguments(self):
        """ Add the arguments needed for this program. """
        self.add_argument(
            "-w", "--wordfile",
            dest="wordfile", default=None, metavar="WORDFILE",
            help=(
                "Specify that the file WORDFILE contains the list"
                " of valid words from which to generate passphrases."))
        self.add_argument(
            "--min",
            dest="min_length", type=int, default=5, metavar="MIN_LENGTH",
            help="Generate passphrases containing at least MIN_LENGTH words.")
        self.add_argument(
            "--max",
            dest="max_length", type=int, default=9, metavar="MAX_LENGTH",
            help="Generate passphrases containing at most MAX_LENGTH words.")
        self.add_argument(
            "-n", "--numwords",
            dest="numwords", type=int, default=6, metavar="NUM_WORDS",
            help="Generate passphrases containing exactly NUM_WORDS words.")
        self.add_argument(
            "-i", "--interactive",
            action="store_true", dest="interactive", default=False,
            help=(
                "Generate and output a passphrase, query the user to"
                " accept it, and loop until one is accepted."))
        self.add_argument(
            "-v", "--valid-chars",
            dest="valid_chars", default=".", metavar="VALID_CHARS",
            help=(
                "Limit passphrases to only include words matching the regex"
                " pattern VALID_CHARS (e.g. '[a-z]')."))
        self.add_argument(
            "-V", "--verbose",
            action="store_true", dest="verbose", default=False,
            help="Report various metrics for given options.")
        self.add_argument(
            "-a", "--acrostic",
            dest="acrostic", default=False,
            help="Generate passphrases with an acrostic matching ACROSTIC.")
        self.add_argument(
            "-c", "--count",
            dest="count", type=int, default=1, metavar="COUNT",
            help="Generate COUNT passphrases.")
        self.add_argument(
            "-d", "--delimiter",
            dest="delimiter", default=" ", metavar="DELIM",
            help="Separate words within a passphrase with DELIM.")
        self.add_argument(
            "--allow-weak-rng",
            action="store_true", dest="allow_weak_rng", default=False,
            help=(
                "Allow fallback to weak RNG if the "
                "system does not support cryptographically secure RNG. "
                "Only use this if you know what you are doing."))


def main(argv=None):
    """ Mainline code for this program. """

    if argv is None:
        argv = sys.argv

    exit_status = 0

    try:
        program_name = os.path.basename(argv[0])
        parser = XkcdPassArgumentParser(prog=program_name)

        options = parser.parse_args(argv[1:])
        validate_options(parser, options)

        my_wordlist = generate_wordlist(
            wordfile=options.wordfile,
            min_length=options.min_length,
            max_length=options.max_length,
            valid_chars=options.valid_chars)

        if options.verbose:
            verbose_reports(
                len(my_wordlist),
                options.numwords,
                options.wordfile)

        emit_passwords(my_wordlist, options)

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


if __name__ == '__main__':
    exit_status = main(sys.argv)
    sys.exit(exit_status)
