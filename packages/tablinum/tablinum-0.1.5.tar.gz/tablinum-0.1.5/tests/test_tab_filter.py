#! /usr/bin/env python3

import unittest

import tablinum


class TestTableFilter(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.rain = '''
Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
-------------------------------------------------------------
2019-12-30     1  0.0  0.2   0.0  0.0  1.2   0.0   0.0    1.4
2020-01-06     2  0.5  0.0   0.0  6.4  0.0   0.1   1.7    8.7
2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
2020-01-20     4  0.0  0.0   0.0  0.0  0.0   0.1   2.3    2.4
2020-01-27     5  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1
2020-02-03     6  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
2020-02-10     7  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
2020-02-17     8  0.2  3.3   1.0  3.8  0.0   0.5   1.0    9.8
2020-02-24     9  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5
2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
2020-03-16    12  3.6  1.3   0.0  0.0  0.0   0.5   0.0    5.4
2020-03-23    13  0.0  0.0   0.0  0.0  0.0   0.0   0.0    0.0
2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1
'''.strip()

    def test_filter(self):
        "Select matching rows"
        self.tab.parse_lines(self.rain.splitlines())

        self.tab.do('filter')  # missing predicate does nothing
        self.assertEqual(str(self.tab), self.rain)

        self.tab.do('filter True')  # True predicate does nothing
        self.assertEqual(str(self.tab), self.rain)

        self.tab.do('filter b=>4')  # Syntax error make message
        self.assertEqual(str(self.tab), '?! syntax b=>4\n' + self.rain)

        self.tab.do('filter j > 10.0')
        expected = '''
Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
-------------------------------------------------------------
2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
2020-01-27     5  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1
2020-02-03     6  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
2020-02-10     7  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
2020-02-24     9  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5
2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('filter @c=0')
        expected = '''
Monday      Week  Mon  Tue  Wed  Thu  Fri   Sat  Sun  Total
-----------------------------------------------------------
2020-03-02    10  0.0  0.0  4.3  0.0  3.0  12.4  0.0   19.7
2020-03-09    11  0.0  4.3  6.3  1.3  1.0   1.0  0.0   13.9
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('filter i=Sun')  # treats unknown name as string...
        expected = '''
Monday  Week  Mon  Tue  Wed  Thu  Fri  Sat  Sun  Total
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('filter False')
        self.assertEqual(str(self.tab), "")
