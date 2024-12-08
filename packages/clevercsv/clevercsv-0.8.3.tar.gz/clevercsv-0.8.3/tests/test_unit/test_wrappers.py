# -*- coding: utf-8 -*-

"""
Unit tests for the wrappers

Author: Gertjan van den Burg

"""

import os
import tempfile
import types
import unittest

from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Union

import pandas as pd

from clevercsv import wrappers
from clevercsv import writer
from clevercsv.dialect import SimpleDialect
from clevercsv.exceptions import NoDetectionResult


class WrappersTestCase(unittest.TestCase):
    def _df_test(
        self, table: List[List[Any]], dialect: SimpleDialect, **kwargs: Any
    ) -> None:
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        tmpid = os.fdopen(tmpfd, "w", encoding=kwargs.get("encoding"))
        w = writer(tmpid, dialect=dialect)
        w.writerows(table)
        tmpid.close()

        exp_df = pd.DataFrame.from_records(table[1:], columns=table[0])
        df = wrappers.read_dataframe(tmpfname)

        try:
            self.assertTrue(df.equals(exp_df))
        finally:
            os.unlink(tmpfname)

    def _write_tmpfile(
        self, table: Iterable[Iterable[Any]], dialect: SimpleDialect
    ) -> str:
        """Write a table to a temporary file using specified dialect"""
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        tmpid = os.fdopen(tmpfd, "w")
        w = writer(tmpid, dialect=dialect)
        w.writerows(table)
        tmpid.close()
        return tmpfname

    def _read_test(
        self, table: Iterable[Iterable[Any]], dialect: SimpleDialect
    ) -> None:
        tmpfname = self._write_tmpfile(table, dialect)
        exp = [list(map(str, r)) for r in table]
        try:
            self.assertEqual(exp, wrappers.read_table(tmpfname))
        finally:
            os.unlink(tmpfname)

    def _stream_test(
        self, table: Iterable[Iterable[str]], dialect: SimpleDialect
    ) -> None:
        tmpfname = self._write_tmpfile(table, dialect)
        exp = [list(map(str, r)) for r in table]
        try:
            out = wrappers.stream_table(tmpfname)
            self.assertTrue(isinstance(out, types.GeneratorType))
            self.assertEqual(exp, list(out))
        finally:
            os.unlink(tmpfname)

    def _read_test_rows(
        self, rows: List[str], expected: List[List[str]]
    ) -> None:
        contents = "\n".join(rows)
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        tmpid = os.fdopen(tmpfd, "w")
        tmpid.write(contents)
        tmpid.close()

        try:
            self.assertEqual(expected, wrappers.read_table(tmpfname))
        finally:
            os.unlink(tmpfname)

    def _stream_test_rows(
        self, rows: Iterable[str], expected: List[List[str]]
    ) -> None:
        contents = "\n".join(rows)
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        tmpid = os.fdopen(tmpfd, "w")
        tmpid.write(contents)
        tmpid.close()

        try:
            out = wrappers.stream_table(tmpfname)
            self.assertTrue(isinstance(out, types.GeneratorType))
            self.assertEqual(expected, list(out))
        finally:
            os.unlink(tmpfname)

    def test_read_dataframe(self) -> None:
        table: List[List[Any]]

        table = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        with self.subTest(name="simple"):
            self._df_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar="", escapechar="\\")
        with self.subTest(name="escaped"):
            self._df_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="quoted"):
            self._df_test(table, dialect)

        table = [['a"A,0"b', "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="double"):
            self._df_test(table, dialect)

        table = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        with self.subTest(name="simple_nchar"):
            self._df_test(table, dialect, num_char=10)

        table = [["Ä", "Ð", "Ç"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        with self.subTest(name="simple_encoding"):
            self._df_test(table, dialect, num_char=10, encoding="latin1")

    def test_read_table(self) -> None:
        table: List[List[Any]]

        table = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        with self.subTest(name="simple"):
            self._read_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar="", escapechar="\\")
        with self.subTest(name="escaped"):
            self._read_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="quoted"):
            self._read_test(table, dialect)

        table = [['a"A,0"b', "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="double"):
            self._read_test(table, dialect)

        rows = ['1,"AA"', '2,"BB"', '3,"CC"']
        exp = [["1", "AA"], ["2", "BB"], ["3", "CC"]]
        with self.subTest(name="rowtest"):
            self._read_test_rows(rows, exp)

        # This raises a NoDetectionResult due to the spacing after the
        # delimiter, which confuses the detection algorithm. Support for
        # detecting 'skipinitialspace' should fix this problem.
        rows = ['1, "AA"', '2, "BB"', '3, "CC"']
        exp = [["1", "AA"], ["2", "BB"], ["3", "CC"]]
        with self.subTest(name="raises2"):
            with self.assertRaises(NoDetectionResult):
                self._read_test_rows(rows, exp)

    def test_stream_table(self) -> None:
        table: List[List[Any]]

        table = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        with self.subTest(name="simple"):
            self._stream_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar="", escapechar="\\")
        with self.subTest(name="escaped"):
            self._stream_test(table, dialect)

        table = [["A,0", "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="quoted"):
            self._stream_test(table, dialect)

        table = [['a"A,0"b', "B", "C"], [1, 2, 3], [4, 5, 6]]
        dialect = SimpleDialect(delimiter=",", quotechar='"', escapechar="")
        with self.subTest(name="double"):
            self._stream_test(table, dialect)

        rows = ['1,"AA"', '2,"BB"', '3,"CC"']
        exp = [["1", "AA"], ["2", "BB"], ["3", "CC"]]
        with self.subTest(name="rowtest"):
            self._stream_test_rows(rows, exp)

        # This raises a NoDetectionResult due to the spacing after the
        # delimiter, which confuses the detection algorithm. Support for
        # detecting 'skipinitialspace' should fix this problem.
        rows = ['1, "AA"', '2, "BB"', '3, "CC"']
        exp = [["1", "AA"], ["2", "BB"], ["3", "CC"]]
        with self.subTest(name="raises2"):
            with self.assertRaises(NoDetectionResult):
                self._stream_test_rows(rows, exp)

    def _write_test_table(
        self, table: Iterable[Iterable[Any]], expected: str, **kwargs: Any
    ) -> None:
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        wrappers.write_table(table, tmpfname, **kwargs)
        read_encoding = kwargs.get("encoding", None)
        with open(tmpfname, "r", newline="", encoding=read_encoding) as fp:
            data = fp.read()

        try:
            self.assertEqual(data, expected)
        finally:
            os.close(tmpfd)
            os.unlink(tmpfname)

    def test_write_table(self) -> None:
        table: List[List[Union[str, int]]] = [
            ["A", "B,C", "D"],
            [1, 2, 3],
            [4, 5, 6],
        ]
        exp = 'A,"B,C",D\r\n1,2,3\r\n4,5,6\r\n'
        with self.subTest(name="default"):
            self._write_test_table(table, exp)

        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        exp = "A;B,C;D\n1;2;3\n4;5;6\n"
        with self.subTest(name="dialect"):
            self._write_test_table(table, exp, dialect=dialect)

        exp = "A;1;4\nB,C;2;5\nD;3;6\n"
        with self.subTest(name="transposed"):
            self._write_test_table(table, exp, dialect=dialect, transpose=True)

        table[2].append(8)
        with self.assertRaises(ValueError):
            self._write_test_table(table, "")

        table = [["Å", "B", "C"], [1, 2, 3], [4, 5, 6]]
        exp = "Å,B,C\r\n1,2,3\r\n4,5,6\r\n"
        with self.subTest(name="encoding_1"):
            # Not specifying an encoding here could potentially fail on
            # Windows, due to open() defaulting to
            # locale.getpreferredencoding() (see gh-27).
            self._write_test_table(table, exp, encoding="utf-8")

        with self.subTest(name="encoding_2"):
            self._write_test_table(table, exp, encoding="cp1252")

    def _write_test_dicts(
        self, items: Iterable[Dict[str, Any]], expected: str, **kwargs: Any
    ) -> None:
        tmpfd, tmpfname = tempfile.mkstemp(prefix="ccsv_", suffix=".csv")
        wrappers.write_dicts(items, tmpfname, **kwargs)
        read_encoding = kwargs.get("encoding", None)
        with open(tmpfname, "r", newline="", encoding=read_encoding) as fp:
            data = fp.read()

        try:
            self.assertEqual(data, expected)
        finally:
            os.close(tmpfd)
            os.unlink(tmpfname)

    def test_write_dicts(self) -> None:
        items = [{"A": 1, "B": 2, "C": 3}, {"A": 4, "B": 5, "C": 6}]
        exp = "A,B,C\r\n1,2,3\r\n4,5,6\r\n"
        with self.subTest(name="default"):
            self._write_test_dicts(items, exp)

        dialect = SimpleDialect(delimiter=";", quotechar="", escapechar="")
        exp = "A;B;C\n1;2;3\n4;5;6\n"
        with self.subTest(name="dialect"):
            self._write_test_dicts(items, exp, dialect=dialect)

        items = [{"Å": 1, "B": 2, "C": 3}, {"Å": 4, "B": 5, "C": 6}]
        exp = "Å,B,C\r\n1,2,3\r\n4,5,6\r\n"
        with self.subTest(name="encoding_1"):
            # Not specifying an encoding here could potentially fail on
            # Windows, due to open() defaulting to
            # locale.getpreferredencoding() (see gh-27).
            self._write_test_dicts(items, exp, encoding="utf-8")

        with self.subTest(name="encoding_2"):
            self._write_test_dicts(items, exp, encoding="cp1252")
