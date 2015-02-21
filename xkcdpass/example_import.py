import xkcdpass.xkcd_password as xp
import random


def random_capitalisation(s, chance):
    new_str = []
    for i, c in enumerate(s):
        new_str.append(c.upper() if random.random() < chance else c)
    return "".join(new_str)


words = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=words, min_length=5, max_length=8)
raw_password = xp.generate_xkcdpassword(mywords)

for i in range(5):
    print(random_capitalisation(raw_password, i/10.0))
