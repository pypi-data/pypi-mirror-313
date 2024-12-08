# -*- coding: utf-8 -*-

"""
Unit tests for the potential dialect selection.

Author: Gertjan van den Burg

"""

import unittest

from clevercsv.potential_dialects import filter_urls
from clevercsv.potential_dialects import get_delimiters
from clevercsv.potential_dialects import get_quotechars
from clevercsv.potential_dialects import masked_by_quotechar


class PotentialDialectTestCase(unittest.TestCase):
    def test_masked_by_quotechar(self) -> None:
        self.assertTrue(masked_by_quotechar('A"B&C"A', '"', "", "&"))
        self.assertFalse(masked_by_quotechar('A"B&C"A&A', '"', "", "&"))
        self.assertFalse(masked_by_quotechar('A|"B&C"A', '"', "|", "&"))
        self.assertFalse(masked_by_quotechar('A"B"C', '"', "", ""))

    def test_filter_urls(self) -> None:
        data = "A,B\nwww.google.com,10\nhttps://gertjanvandenburg.com,25\n"
        exp = "A,B\nU,10\nU,25\n"
        self.assertEqual(exp, filter_urls(data))

    def test_get_quotechars(self) -> None:
        data = "A,B,'A',B\"D\"E"
        exp = set(['"', "'", ""])
        out = get_quotechars(data)
        self.assertEqual(out, exp)

    def test_get_delimiters(self) -> None:
        data = "A,B|CD,E;F\tD123£123€10.,0"
        exp = set([",", "|", ";", "\t", "€", "£", ""])
        out = get_delimiters(data, "UTF-8")
        self.assertEqual(out, exp)


if __name__ == "__main__":
    unittest.main()
