#!/usr/bin/env python
# encoding: utf-8

__LICENSE__ = """
Copyright (c) 2011, Steven Tobin.
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

import random
import os
import sys

def generate_wordlist(wordfile="", min_length=5, max_length=9):
    """
    generate a word list from either a kwarg word_file, or a system default
    """

    if not wordfile:
        if "darwin" in sys.platform:
            ## OS X
            wordfile = "/usr/share/dict/words"
        elif "linux" in sys.platform:
            ## Linux
            wordfile = "/usr/dict/words"
        else:
            # if we get here wordfile is not set, the try...except block below
            # will catch it
            print "No default word file found, please supply custom list"

    wordfile = os.path.expanduser(wordfile) # just to be sure

    words = []

    try:
        with open(wordfile) as wlf:
            for line in wlf:
                if min_length <= len(line.strip()) <= max_length:
                    words.append(line.strip())
    except:
            print "Word list not loaded"
            raise SystemExit
    return words

def generate_xkcdpassword(wordlist, n_words=4, interactive=False):
    """
    generate an XKCD-style password from the words in wordlist
    """

    # useful if driving the logic from other code
    if not interactive:
        try:
            # random.SystemRandom() should be cryptographically secure
            return " ".join(random.SystemRandom().sample(wordlist, n_words))
        except NotImplementedError:
            print 'System does not support random number generator or Python version < 2.4.'      

    # else, interactive session 
    custom_n_words = raw_input("Enter number of words (default 4): ")
    if custom_n_words: n_words = int(custom_n_words)
            
    accepted = "n"

    while accepted.lower() not in [ "y", "yes" ]:
        try:
            passwd = " ".join(random.SystemRandom().sample(wordlist, n_words))
        except NotImplementedError:
            print 'System does not support random number generator or Python version < 2.4.'
        print "Generated: ", passwd
        accepted = raw_input("Accept? [yN] ")     

    return passwd

if __name__ == '__main__':

    custom_wordfile = "~/local/share/dict/common"

    my_wordlist = generate_wordlist(custom_wordfile) 
    print generate_xkcdpassword(my_wordlist, interactive=True)



