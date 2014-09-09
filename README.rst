xkcdpass
========

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

Python 2.4+ (Python 3.x compatible)



Running ``xkcdpass``
====================

``xkcdpass`` can be called with no arguments::

    $ xkcdpass
    > pinball previous deprive militancy bereaved numeric

which returns a single password, using the default dictionary and default settings. Or you can mix whatever arguments you want::

    $ xkcdpass --count=5 --acrostic='chaos' --delimiter='|' --min=5 --max=6 --valid_chars='[a-z]'
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
* ``--valid_chars='[a-z]'``   using only lower-case letters (via regex).


A concise overview of the available ``xkcdpass`` options can be accessed via::

    xkcdpass --help

    Usage: xkcdpass [options]

    Options:
        -h, --help
                                    show this help message and exit
        -w WORDFILE, --wordfile=WORDFILE
                                    List of valid words for password
        --min=MIN_LENGTH
                                    Minimum length of words to make password
        --max=MAX_LENGTH
                                    Maximum length of words to make password
        -n NUMWORDS, --numwords=NUMWORDS
                                    Number of words to make password
        -i, --interactive
                                    Interactively select a password
        -v VALID_CHARS, --valid_chars=VALID_CHARS
                                    Valid chars, using regexp style (e.g. '[a-z]')
        -V, --verbose
                                    Report various metrics for given options
        -a ACROSTIC, --acrostic=ACROSTIC
                                    Acrostic to constrain word choices
        -c COUNT, --count=COUNT
                                    number of passwords to generate
        -d DELIM, --delimiter=DELIM
                                    separator character between words


A large wordlist is provided (courtesy of `12Dicts <http://wordlist.aspell.net/12dicts/>`_) for convenience, but the generator can be used with any word file of the correct format: a file containing one 'word' per line. The default word file can be found in ``xkcdpass/static/default.txt``.



Advanced Usage
==============

The built-in functionality of ``xkcdpass`` can be extended by importing the module into custom python scripts.
An example of this usage is provided in `example_import.py <https://github.com/redacted/XKCD-password-generator/blob/master/xkcdpass/example_import.py>`_, which randomly capitalises the letters in a generated password. 

A simple use of import:: 

    import xkcdpass.xkcd_password as xp

    ## create a wordlist from the default wordfile
    ## use words between 5 and 8 letters long
    wordfile = xp.locate_wordfile()
    mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8) 

    ## create a password with the acrostic "face"
    print(xp.generate_xkcdpassword(mywords, acrostic="face")) 



License
=======
The BSD License (BSD)
