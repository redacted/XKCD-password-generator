import re
import subprocess
import sys
import unittest

from xkcdpass import xkcd_password

WORDFILE = 'xkcdpass/static/legacy'


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
        self.assertEqual(len(self.wordlist_full), 29611)

    def test_regex(self):
        self.assertNotIn("__$$$__", self.wordlist_small)

    def test_acrostic(self):
        word = "face"
        result = xkcd_password.generate_xkcdpassword(
            self.wordlist_small,
            acrostic=word)
        self.assertEqual("".join(map(lambda x: x[0], result.split())), word)

    def test_commandlineCount(self):
        count = 6
        result = subprocess.check_output([
            sys.executable, "xkcdpass/xkcd_password.py",
            "-w", WORDFILE,
            "-c", str(count),
        ])
        self.assertTrue(result.count(b"\n"), count)

    def test_delim(self):
        tdelim = "_"
        result = xkcd_password.generate_xkcdpassword(
            self.wordlist_small,
            delimiter=tdelim)
        self.assertIsNotNone(re.match('([a-z]+(_|$))+', result))

    def test_separator(self):
        count = 3
        result = subprocess.check_output(
            ["python", "xkcdpass/xkcd_password.py",
             "--count", str(count),
             "--delimiter", "|",
             "--separator", " "])
        self.assertEqual(result.count(b" "), 3)

    def test_separator_no_end(self):
        "Pipe output to other program. e.g. `xkcdpass -c 1 -s "" | xsel -b`"
        count = 1
        result = subprocess.check_output(
            ["python", "xkcdpass/xkcd_password.py",
             "--count", str(count),
             "--separator", ""])
        self.assertEqual(result.find(b"\n"), -1)

    def test_set_case(self):
        words = "this is only a test".lower().split()
        words_before = set(words)

        results = {}

        results["lower"] = xkcd_password.set_case(words, method="lower")
        results["upper"] = xkcd_password.set_case(words, method="upper")
        results["alternating"] = xkcd_password.set_case(words, method="alternating")
        results["random"] = xkcd_password.set_case(words, method="random", testing=True)

        words_after = set([word.lower() for group in list(results.values()) for word in group])

        # Test that no words have been fundamentally mutated by any of the methods
        self.assertTrue(words_before == words_after)

        # Test that the words have been uppered or lowered respectively.
        self.assertTrue(all([word.islower() for word in results["lower"]]))
        self.assertTrue(all([word.isupper() for word in results["upper"]]))

        # Test that the words have been correctly uppered randomly.
        expected_random_result_1 = ['THIS', 'IS', 'ONLY', 'a', 'test']
        expected_random_result_2 = ['THIS', 'IS', 'a', 'test', 'ALSO']

        words_extra = "this is a test also".lower().split()
        observed_random_result_1 = results["random"]
        observed_random_result_2 = xkcd_password.set_case(
            words_extra, 
            method="random",
            testing=True
        )

        self.assertTrue(expected_random_result_1 == observed_random_result_1)
        self.assertTrue(expected_random_result_2 == observed_random_result_2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(XkcdPasswordTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
