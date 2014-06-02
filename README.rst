| A simple command line script that generates XKCD-style multiword
passwords/passphrases.
| Inspired by http://xkcd.com/936/

|XKCD password strength|

For more memorable words, we provide a word list
(``static/default.txt``), reproduced with permission from
http://wordlist.sourceforge.net/

A simple example of how the script may be used via ``import`` is also
provided.

**Requirements:** Python 2.4+ (Python 3 compatible)

| **Usage:**
| xkcdpass [options]

-  ``-w WORDFILE, --wordfile=WORDFILE`` List of valid words for password

-  ``--min=MIN_LENGTH`` Minimum length of words to make password

-  ``--max=MAX_LENGTH`` Maximum length of words to make password

-  ``-n NUMWORDS, --numwords=NUMWORDS`` Number of words to make password

-  ``-i, --interactive`` Interactively select a password

-  ``-v VALID_CHARS, --valid_chars=VALID_CHARS`` Valid chars, using
   regexp style (e.g. '[a-z]')

-  ``-V, --verbose`` Report various metrics for given options

-  ``-a ACROSTIC, --acrostic=ACROSTIC`` Constrain word choices to those
   starting with the letters in a given word

-  ``-c COUNT, --count=COUNT`` Number of passwords to generate

-  ``-d DELIMITER, --delimiter=DELIMITER`` separator character between
   words

Licensed under the BSD license.

.. |XKCD password strength| image:: http://imgs.xkcd.com/comics/password_strength.png
