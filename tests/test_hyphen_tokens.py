import unittest

from ru_normalizr import normalize
from ru_normalizr.numerals import simple_tokenize


class RuNormalizrHyphenTokenTests(unittest.TestCase):
    def test_tokenizer_keeps_letter_digit_hyphenated_tokens_whole(self):
        self.assertEqual(simple_tokenize("COVID-19"), ["COVID-19"])
        self.assertEqual(simple_tokenize("Т-34"), ["Т-34"])
        self.assertEqual(simple_tokenize("52-G"), ["52-G"])
        self.assertEqual(simple_tokenize("80-A"), ["80-A"])

    def test_tokenizer_still_splits_numeric_suffix_forms(self):
        self.assertEqual(simple_tokenize("1980-е"), ["1980", "-", "е"])
        self.assertEqual(simple_tokenize("5-й"), ["5", "-", "й"])

    def test_normalize_preserves_hyphen_in_letter_digit_compounds(self):
        self.assertEqual(normalize("COVID-19"), "ковид-девятнадцать")
        self.assertEqual(normalize("Т-34"), "Т-тридцать четыре")
        self.assertEqual(normalize("B52G"), "би пятьдесят два-джи")
        self.assertEqual(normalize("Z80A"), "зи восемьдесят-э")


if __name__ == "__main__":
    unittest.main()
