#! /usr/bin/env python3

import unittest

import tablinum


class TestTableSort(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.rain = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
'''.strip()

        self.diary = '''
Monday     0.38  0.52
Tuesday    0.41  0.14
Wednesday  0.91  0.17
Thursday   0.22  0.94
Friday     0.94  0.28
Saturday   0.62  0.02
Sunday     0.34  0.25
'''.strip()

        self.addresses = '''
Mac                IP
00:01:E6:2C:42:1D  192.168.0.12
3C:07:54:3D:3F:82  192.168.0.13
60:C5:47:21:D7:E9  192.168.0.16
2C:4D:54:74:A4:D8  192.168.0.4
50:C7:BF:1C:88:66  192.168.0.3
74:D0:2B:5D:CD:C0  192.168.0.2
'''.strip()

        self.addresses_by_A = '''
Mac                IP
00:01:E6:2C:42:1D  192.168.0.12
2C:4D:54:74:A4:D8  192.168.0.4
3C:07:54:3D:3F:82  192.168.0.13
50:C7:BF:1C:88:66  192.168.0.3
60:C5:47:21:D7:E9  192.168.0.16
74:D0:2B:5D:CD:C0  192.168.0.2
'''.strip()

        self.addresses_by_B = '''
Mac                IP
74:D0:2B:5D:CD:C0  192.168.0.2
50:C7:BF:1C:88:66  192.168.0.3
2C:4D:54:74:A4:D8  192.168.0.4
00:01:E6:2C:42:1D  192.168.0.12
3C:07:54:3D:3F:82  192.168.0.13
60:C5:47:21:D7:E9  192.168.0.16
'''.strip()

    def test_filter(self):
        "Select matching rows"
        self.tab.parse_lines(self.rain.splitlines())
        self.tab.do('sort')  # missing predicate does nothing here
        self.assertEqual(str(self.tab), self.rain)
        self.tab.do('sort j')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
'''.strip()
        self.assertEqual(str(self.tab), expected)
        self.tab.do('sort -len(z)')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
'''.strip()
        self.assertEqual(str(self.tab), expected)
        self.tab.do('sort B')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
'''.strip()
        self.assertEqual(str(self.tab), expected)

        # check broken col spec
        self.tab.do('sort <')
        self.assertEqual(str(self.tab), '?! syntax (<)\n' + expected)

        self.tab.do('sort @z')  # automatic pop and push of header
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('dup 0 uniq')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('uniq ?')
        expected = '''
?! colspec ?
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-01-06     2  0.5  0.0  0.0  6.4  0.0  0.1   1.7    8.7  Damp
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2019-12-30     1  0.0  0.2  0.0  0.0  1.2  0.0   0.0    1.4  Dry
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-02-10     7  5.5  0.0  0.5  6.6  0.0  4.9  15.6   33.1  Monsoon
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-01-13     3  5.3  1.7  9.1  3.0  1.7  0.0   0.0   20.8  Wet
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('uniq z')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('sort 1')
        expected = '''
Date        Week  Mon  Tue  Wed  Thu  Fri  Sat   Sun  Total  Description
------------------------------------------------------------------------
2020-01-20     4  0.0  0.0  0.0  0.0  0.0  0.1   2.3    2.4  Dry
2020-01-27     5  8.4  2.1  0.0  0.5  1.0  0.0   7.1   19.1  Wet
2020-02-03     6  0.1  0.0  0.0  0.0  0.0  1.5  10.6   12.2  Humid
2020-02-17     8  0.2  3.3  1.0  3.8  0.0  0.5   1.0    9.8  Damp
2020-02-24     9  6.1  0.5  0.1  8.6  5.9  7.1   0.2   28.5  Monsoon
'''.strip()
        self.assertEqual(str(self.tab), expected)

        self.tab.do('uniq @z')
        self.assertEqual(str(self.tab), expected)

        self.tab.clear()
        self.tab.parse_lines(self.diary.splitlines())
        self.assertEqual(str(self.tab), self.diary)

        self.tab.do('sort c')
        self.assertEqual(str(self.tab), '''
Saturday   0.62  0.02
Tuesday    0.41  0.14
Wednesday  0.91  0.17
Sunday     0.34  0.25
Friday     0.94  0.28
Monday     0.38  0.52
Thursday   0.22  0.94
'''.strip())

        self.tab.do('sort')
        self.assertEqual(str(self.tab), '''
Monday     0.38  0.52
Tuesday    0.41  0.14
Wednesday  0.91  0.17
Thursday   0.22  0.94
Friday     0.94  0.28
Saturday   0.62  0.02
Sunday     0.34  0.25
'''.strip())

        self.tab.do('sort =a')
        self.assertEqual(str(self.tab), '''
Friday     0.94  0.28
Monday     0.38  0.52
Saturday   0.62  0.02
Sunday     0.34  0.25
Thursday   0.22  0.94
Tuesday    0.41  0.14
Wednesday  0.91  0.17
'''.strip())

    def test_special_sorts(self):
        "Smart sorting"
        self.tab.parse_lines(self.addresses.splitlines())
        self.tab.do('sort')
        self.assertEqual(str(self.tab), self.addresses_by_A)
        self.tab.do('sort b')
        self.assertEqual(str(self.tab), self.addresses_by_B)
