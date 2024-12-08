#! /usr/bin/env python3

import unittest

import tablinum


class TestTableGrouper(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.rain = '''
Month          Monday      Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
----------------------------------------------------------------------
December 2019  2019-12-30  0.0  0.2   0.0  0.0  1.2   0.0   0.0    1.4
January 2020   2020-01-06  0.5  0.0   0.0  6.4  0.0   0.1   1.7    8.7
January 2020   2020-01-13  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
January 2020   2020-01-20  0.0  0.0   0.0  0.0  0.0   0.1   2.3    2.4
January 2020   2020-01-27  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1
February 2020  2020-02-03  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
February 2020  2020-02-10  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
February 2020  2020-02-17  0.2  3.3   1.0  3.8  0.0   0.5   1.0    9.8
February 2020  2020-02-24  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5
March 2020     2020-03-02  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
March 2020     2020-03-09  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
March 2020     2020-03-16  3.6  1.3   0.0  0.0  0.0   0.5   0.0    5.4
March 2020     2020-03-23  0.0  0.0   0.0  0.0  0.0   0.0   0.0    0.0
March 2020     2020-03-30  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1
'''.strip()

        self.grouped = '''
Month          Monday      Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
----------------------------------------------------------------------
December 2019  2019-12-30  0.0  0.2   0.0  0.0  1.2   0.0   0.0    1.4

January 2020   2020-01-06  0.5  0.0   0.0  6.4  0.0   0.1   1.7    8.7
January 2020   2020-01-13  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
January 2020   2020-01-20  0.0  0.0   0.0  0.0  0.0   0.1   2.3    2.4
January 2020   2020-01-27  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1

February 2020  2020-02-03  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
February 2020  2020-02-10  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
February 2020  2020-02-17  0.2  3.3   1.0  3.8  0.0   0.5   1.0    9.8
February 2020  2020-02-24  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5

March 2020     2020-03-02  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
March 2020     2020-03-09  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
March 2020     2020-03-16  3.6  1.3   0.0  0.0  0.0   0.5   0.0    5.4
March 2020     2020-03-23  0.0  0.0   0.0  0.0  0.0   0.0   0.0    0.0
March 2020     2020-03-30  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1
'''.strip()

    def test_grouping(self):
        "Select matching rows"
        self.tab.parse_lines(self.rain.splitlines())
        self.assertEqual(str(self.tab), self.rain)

        self.tab.do('group')  # missing predicate assumes a
        self.assertEqual(str(self.tab), self.grouped)

        self.tab.do('group a')  # repeat is harmless
        self.assertEqual(str(self.tab), self.grouped)

        self.tab.do('noblanks')
        self.assertEqual(str(self.tab), self.rain)

        self.tab.do('group a')
        self.assertEqual(str(self.tab), self.grouped)

        self.tab.do('noblanks')
        self.assertEqual(str(self.tab), self.rain)

        self.tab.do('group ?')
        self.assertEqual(str(self.tab), '?! colspec ?\n' + self.rain)
