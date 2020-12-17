xkcdpass
========

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/redacted/XKCD-password-generator
   :target: https://gitter.im/redacted/XKCD-password-generator?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

A flexible and scriptable password generator which generates strong passphrases, inspired by `XKCD 936 <http://xkcd.com/936/>`_::

    $ xkcdpass
    > correct horse battery staple

.. image:: http://imgs.xkcd.com/comics/password_strength.png



Install
=======

``xkcdpass`` can be easily installed using pip::

    pip install xkcdpass

or manually::

    python setup.py install



Source
~~~~~~
The latest development version can be found on github: https://github.com/redacted/XKCD-password-generator

Contributions welcome and gratefully appreciated!



Requirements
============

Python 2 (version 2.7 or later), or Python 3 (version 3.4 or later). Running module unit tests on Python 2 requires ``mock`` to be installed.



Running ``xkcdpass``
====================

``xkcdpass`` can be called with no arguments::

    $ xkcdpass
    > pinball previous deprive militancy bereaved numeric

which returns a single password, using the default dictionary and default settings. Or you can mix whatever arguments you want::

    $ xkcdpass --count=5 --acrostic='chaos' --delimiter='|' --min=5 --max=6 --valid-chars='[a-z]'
    > collar|highly|asset|ovoid|sultan
    > caper|hangup|addle|oboist|scroll
    > couple|honcho|abbot|obtain|simple
    > cutler|hotly|aortae|outset|stool
    > cradle|helot|axial|ordure|shale

which returns

* ``--count=5``   5 passwords to choose from
* ``--acrostic='chaos'``   the first letters of which spell 'chaos'
* ``--delimiter='|'``   joined using '|'
* ``--min=5 --max=6``  with words between 5 and 6 characters long
* ``--valid-chars='[a-z]'``   using only lower-case letters (via regex).


A concise overview of the available ``xkcdpass`` options can be accessed via::

    xkcdpass --help

    Usage: xkcdpass [options]

    Options:
        -h, --help
                                    show this help message and exit
        -w WORDFILE, --wordfile=WORDFILE
                                    Specify that the file WORDFILE contains the list of
                                    valid words from which to generate passphrases.
                                    Provided wordfiles: eff-long (default), eff-short,
                                    eff-special, legacy, spa-mich (Spanish), fin-kotus (Finnish)
                                    ita-wiki (Italian), ger-anlx (German), nor-nb (Norwegian),
                                    fr-freelang (French), pt-ipublicis / pt-l33t-ipublicis (Portuguese)
        --min=MIN_LENGTH
                                    Minimum length of words to make password
        --max=MAX_LENGTH
                                    Maximum length of words to make password
        -n NUMWORDS, --numwords=NUMWORDS
                                    Number of words to make password
        -i, --interactive
                                    Interactively select a password
        -v VALID_CHARS, --valid-chars=VALID_CHARS
                                    Valid chars, using regexp style (e.g. '[a-z]')
        -V, --verbose
                                    Report various metrics for given options, including word list entropy
        -a ACROSTIC, --acrostic=ACROSTIC
                                    Acrostic to constrain word choices
        -c COUNT, --count=COUNT
                                    number of passwords to generate
        -d DELIM, --delimiter=DELIM
                                    separator character between words
        -s SEP, --separator SEP
                                    Separate generated passphrases with SEP.
        -C CASE, --case CASE  
                                    Choose the method for setting the case of each word in
                                    the passphrase. Choices: ['alternating', 'upper',
                                    'lower', 'random', 'capitalize'] (default: 'lower').
        --allow-weak-rng     
                                     Allow fallback to weak RNG if the system does not
                                    support cryptographically secure RNG. Only use this if
                                    you know what you are doing.


Word lists
==========

Several word lists are provided with the package. The default, `eff-long`, was specifically designed by the EFF for `passphrase generation  <https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases>`_ and is licensed under `CC BY 3.0 <https://creativecommons.org/licenses/by/3.0/us/>`_. As it was originally intended for use with Diceware ensure that the number of words in your passphrase is at least six when using it. Two shorter variants of that list, `eff-short` and `eff-special`, are also included. Please refer to the EFF documentation linked above for more information.

The original word list from `xkcdpass` versions earlier than 1.10.0 is also provided as a convenience, and is available under `legacy`. This word list is derived mechanically from `12Dicts <http://wordlist.aspell.net/12dicts/>`_ by Alan Beale. It is the understanding of the author of ``xkcdpass`` that purely mechanical transformation does not imbue copyright in the resulting work. The documentation for the 12Dicts project at
http://wordlist.aspell.net/12dicts/ contains the following dedication:

..

    The 12dicts lists were compiled by Alan Beale. I explicitly release them to the public domain, but request acknowledgment of their use.

Note that the generator can be used with any word file of the correct format: a file containing one 'word' per line.  

Additional languages
~~~~~~~~~~~~~~~~~~~~

- Spanish: a modifed version of archive.umich.edu in the `/linguistics` directory. It includes ~80k words. Less than 5 char. and latin-like words were deleted using regex. This list is public domain, see `here <http://www.umich.edu/~archive/linguistics/00readme.txt>`_.
- Finnish: a modified version of the Institute for the Languages of Finland `XML word list <http://kaino.kotus.fi/sanat/nykysuomi/>`_. Profanities and expressions containing spaces were removed using regex. The resulting list contains ~93k words. The list is published under GNU LGPL, EUPL 1.1 and CC-BY 3.0 licenses.
- Italian: generated from dumps of the Italian-language Wikipedia, which is released under the Creative Commons Attribution-Share-Alike 3.0 licence.
- German: based on `this GPL v3 list <https://github.com/dassencio/langcmp/blob/master/wordlists/top10000de.txt>`_. Single and double character words have been removed.
- Norwegian: a modified version of `Norsk Ordbank in Norwegian Bokmål 2005 <https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5&lang=en>`_, 2018-06-28 update, which is released under the `CC-BY 4.0 license <https://creativecommons.org/licenses/by/4.0/>`_. Regex has been used to alter the list for cleanup and removal of words with impractical characters. The resulting list contains ~137k words.
- French: One cleaned version of `this list <https://packetstormsecurity.com/files/download/32007/french.gz>`_ (public domain), and one filtered to remove potentially offensive words.
- Portuguese: Converted variant of the LibreOffice / Firefox poturguese dictionary (from `this link <https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Portuguese%20(European).dic>`_. GPL and BSD licenced.

Additional language word lists are always welcome!

Using xkcdpass as an imported module
====================================

The built-in functionality of ``xkcdpass`` can be extended by importing the module into python scripts. An example of this usage is provided in `example_import.py <https://github.com/redacted/XKCD-password-generator/blob/master/examples/example_import.py>`_, which randomly capitalises the letters in a generated password. `example_json.py` demonstrates integration of xkcdpass into a Django project, generating password suggestions as JSON to be consumed by a Javascript front-end.

A simple use of import::

    from xkcdpass import xkcd_password as xp

    # create a wordlist from the default wordfile
    # use words between 5 and 8 letters long
    wordfile = xp.locate_wordfile()
    mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)

    # create a password with the acrostic "face"
    print(xp.generate_xkcdpassword(mywords, acrostic="face"))

When used as an imported module, `generate_wordlist()` takes the following args (defaults shown)::

    wordfile=None,
    min_length=5,
    max_length=9,
    valid_chars='.'

While `generate_xkcdpassword()` takes::

    wordlist,
    numwords=6,
    interactive=False,
    acrostic=False,
    delimiter=" "


Insecure random number generators
=================================
`xkcdpass` uses crytographically strong random number generators where possible (provided by `random.SystemRandom()` on most modern operating systems). From version 1.7.0 falling back to an insecure RNG must be explicitly enabled, either by using a new command line variable before running the script::

    xkcdpass --allow-weak-rng

or setting the appropriate environment variable::

    export XKCDPASS_ALLOW_WEAKRNG=1


Changelog
=========
- **1.17.4** Improvements to French dictionary
- **1.17.3** Updated license and supported versions
- **1.17.2** Compatibility fix for 2.x/3.x 
- **1.17.1** Fix issue with README and unicode encoding
- **1.17.0** Add French, Norwegian, and Portuguese dictionaries. Bugfixes and improvements to tests (WIP).
- **1.16.5** Adds title case option for `--case`
- **1.16.4** Improve unit tests, fixes broken test on python 2
- **1.16.3** Correct links for German worldist, updated docs to include the list
- **1.16.2** Fix exception on UTF8 open with python 2.x
- **1.16.1** Fix encoding issue on Windows
- **1.16.0** Case of words in passphrase can now be set using `--case`
- **1.15.1** Added more information about supported languages
- **1.15.0** Added `--separator` argument, German wordlist (GPL 3.0, thanks to @anlx-sw)
- **1.14.3** Refactor password generator, fixes for hardcoded python version in test
- **1.14.2** Improve unit test discovery, remove deprecation warnings
- **1.14.1** Fix wordlist order in `locate_wordfile`
- **1.14.0** Added Finnish and Italian language support (thanks to Jussi Tiira and Lorenzo Mureu respectively)
- **1.13.0** Added Spanish language wordfile (thanks to Javier Meija)


License
=======
This is free software: you may copy, modify, and/or distribute this work under the terms of the BSD 3-Clause license.
See the file ``LICENSE.BSD`` for details.
