import unittest
import subprocess
from xkcdpass import xkcd_password

WORDFILE = 'xkcdpass/static/default.txt'


class XkcdPasswordTests(unittest.TestCase):
    def setUp(self):
        self.wordlist_full = xkcd_password.generate_wordlist(
            wordfile=WORDFILE,
            min_length=5,
            max_length=8,)
        self.wordlist_small = xkcd_password.generate_wordlist(
            wordfile='tests/test_list.txt',
            valid_chars='[a-z]')

    def test_loadwordfile(self):
        self.assertEquals(len(self.wordlist_full), 19493)

    def test_regex(self):
        self.assertNotIn("__$$$__", self.wordlist_small)

    def test_acrostic(self):
        target = ["factual", "amazing", "captain", "exactly"]
        result = xkcd_password.generate_xkcdpassword(
            self.wordlist_small,
            acrostic="face")
        self.assertEquals(result.split(), target)

    def test_commandlineCount(self):
        count = 5
        result = subprocess.check_output(
            ["python", "xkcdpass/xkcd_password.py", "-w", WORDFILE,
             "-c", str(count)])
        self.assertTrue(result.count("\n"), count)

    def test_delim(self):
        tdelim = "_"
        target = tdelim.join(["factual", "amazing", "captain", "exactly"])
        # use an acrostic for simpler target check
        result = xkcd_password.generate_xkcdpassword(
            self.wordlist_small,
            acrostic="face",
            delim=tdelim)
        self.assertEquals(result, target)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(XkcdPasswordTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
