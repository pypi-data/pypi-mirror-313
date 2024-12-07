#! /usr/bin/env python3

import unittest

import tablinum


class TestTableWrangler(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()

    def test_pivot(self):
        self.asbo = '''
Exposure category     Lung cancer  No lung cancer
-------------------------------------------------
Asbestos exposure               6              51
No asbestos exposure           52             941
'''.strip()
        self.longer = '''
Exposure category     Name            Value
-------------------------------------------
Asbestos exposure     Lung cancer         6
Asbestos exposure     No lung cancer     51
No asbestos exposure  Lung cancer        52
No asbestos exposure  No lung cancer    941
'''.strip()
        self.for_camels = '''
ExposureCategory    Name          Value
---------------------------------------
AsbestosExposure    LungCancer        6
AsbestosExposure    NoLungCancer     51
NoAsbestosExposure  LungCancer       52
NoAsbestosExposure  NoLungCancer    941
'''.strip()
        self.for_pirates = '''
Exposure.category     Lung.cancer  No.lung.cancer
-------------------------------------------------
Asbestos.exposure               6              51
No.asbestos.exposure           52             941
'''.strip()

        self.tab.parse_lines(self.asbo.splitlines())
        self.assertEqual(str(self.tab), self.asbo)

        self.tab.do("pivot")  # no argument is nop
        self.assertEqual(str(self.tab), self.asbo)

        self.tab.do("pivot long")
        self.assertEqual(str(self.tab), self.longer)

        self.tab.do("nospace")
        self.assertEqual(str(self.tab), self.for_camels)

        self.tab.parse_lines(self.asbo.splitlines())
        self.assertEqual(str(self.tab), self.asbo)

        self.tab.do("nospace .")
        self.assertEqual(str(self.tab), self.for_pirates)

    def test_pivot_wide(self):
        sales = '''
Region  Quarter  Sales
----------------------
East    Q1        1200
East    Q2        1100
East    Q3        1500
East    Q4        2200
West    Q1        2200
West    Q2        2500
West    Q3        1990
West    Q4        2600
'''.strip()
        counter = '''
Region  Q1  Q2  Q3  Q4
----------------------
East     1   1   1   1
West     1   1   1   1
'''.strip()
        gotter = '''
Region    Q1    Q2    Q3    Q4
------------------------------
East    True  True  True  True
West    True  True  True  True
'''.strip()
        summer = '''
Region    Q1    Q2    Q3    Q4
------------------------------
East    1200  1100  1500  2200
West    2200  2500  1990  2600
'''.strip()

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot wide")
        self.assertEqual(str(self.tab), summer)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot sum")
        self.assertEqual(str(self.tab), summer)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot mean")
        self.assertEqual(str(self.tab), summer)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot alpha")
        self.assertEqual(str(self.tab), summer)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot omega")
        self.assertEqual(str(self.tab), summer)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot count")
        self.assertEqual(str(self.tab), counter)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot any")
        self.assertEqual(str(self.tab), gotter)

        self.tab.parse_lines(sales.splitlines())
        self.tab.do("pivot undefined")
        self.assertEqual(str(self.tab), sales)

    def test_pivot_long(self):
        "Now try going the other way..."

        rain = '''
Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat   Sun
------------------------------------------------------
2019-12-30     1  0.0  0.2   0.0  0.0  1.2   0.0   0.0
2020-01-06     2  0.5  0.0   0.0  6.4  0.0   0.1   1.7
2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0   0.0
2020-01-20     4  0.0  0.0   0.0  0.0  0.0   0.1   2.3
2020-01-27     5  8.4  2.1   0.0  0.5  1.0   0.0   7.1
2020-02-03     6  0.1  0.0   0.0  0.0  0.0   1.5  10.6
2020-02-10     7  5.5  0.0   0.5  6.6  0.0   4.9  15.6
2020-02-17     8  0.2  3.3   1.0  3.8  0.0   0.5   1.0
2020-02-24     9  6.1  0.5   0.1  8.6  5.9   7.1   0.2
2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4   0.0
2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0   0.0
2020-03-16    12  3.6  1.3   0.0  0.0  0.0   0.5   0.0
2020-03-23    13  0.0  0.0   0.0  0.0  0.0   0.0   0.0
2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0   0.0
'''.strip()
        longrain = '''
Monday      Week  Name  Value
-----------------------------
2019-12-30     1  Mon     0.0
2019-12-30     1  Tue     0.2
2019-12-30     1  Wed     0.0
2019-12-30     1  Thu     0.0
2019-12-30     1  Fri     1.2
2019-12-30     1  Sat     0.0
2019-12-30     1  Sun     0.0
2020-01-06     2  Mon     0.5
2020-01-06     2  Tue     0.0
2020-01-06     2  Wed     0.0
2020-01-06     2  Thu     6.4
2020-01-06     2  Fri     0.0
2020-01-06     2  Sat     0.1
2020-01-06     2  Sun     1.7
2020-01-13     3  Mon     5.3
2020-01-13     3  Tue     1.7
2020-01-13     3  Wed     9.1
2020-01-13     3  Thu     3.0
2020-01-13     3  Fri     1.7
2020-01-13     3  Sat     0.0
2020-01-13     3  Sun     0.0
2020-01-20     4  Mon     0.0
2020-01-20     4  Tue     0.0
2020-01-20     4  Wed     0.0
2020-01-20     4  Thu     0.0
2020-01-20     4  Fri     0.0
2020-01-20     4  Sat     0.1
2020-01-20     4  Sun     2.3
2020-01-27     5  Mon     8.4
2020-01-27     5  Tue     2.1
2020-01-27     5  Wed     0.0
2020-01-27     5  Thu     0.5
2020-01-27     5  Fri     1.0
2020-01-27     5  Sat     0.0
2020-01-27     5  Sun     7.1
2020-02-03     6  Mon     0.1
2020-02-03     6  Tue     0.0
2020-02-03     6  Wed     0.0
2020-02-03     6  Thu     0.0
2020-02-03     6  Fri     0.0
2020-02-03     6  Sat     1.5
2020-02-03     6  Sun    10.6
2020-02-10     7  Mon     5.5
2020-02-10     7  Tue     0.0
2020-02-10     7  Wed     0.5
2020-02-10     7  Thu     6.6
2020-02-10     7  Fri     0.0
2020-02-10     7  Sat     4.9
2020-02-10     7  Sun    15.6
2020-02-17     8  Mon     0.2
2020-02-17     8  Tue     3.3
2020-02-17     8  Wed     1.0
2020-02-17     8  Thu     3.8
2020-02-17     8  Fri     0.0
2020-02-17     8  Sat     0.5
2020-02-17     8  Sun     1.0
2020-02-24     9  Mon     6.1
2020-02-24     9  Tue     0.5
2020-02-24     9  Wed     0.1
2020-02-24     9  Thu     8.6
2020-02-24     9  Fri     5.9
2020-02-24     9  Sat     7.1
2020-02-24     9  Sun     0.2
2020-03-02    10  Mon     0.0
2020-03-02    10  Tue     0.0
2020-03-02    10  Wed     4.3
2020-03-02    10  Thu     0.0
2020-03-02    10  Fri     3.0
2020-03-02    10  Sat    12.4
2020-03-02    10  Sun     0.0
2020-03-09    11  Mon     0.0
2020-03-09    11  Tue     4.3
2020-03-09    11  Wed     6.3
2020-03-09    11  Thu     1.3
2020-03-09    11  Fri     1.0
2020-03-09    11  Sat     1.0
2020-03-09    11  Sun     0.0
2020-03-16    12  Mon     3.6
2020-03-16    12  Tue     1.3
2020-03-16    12  Wed     0.0
2020-03-16    12  Thu     0.0
2020-03-16    12  Fri     0.0
2020-03-16    12  Sat     0.5
2020-03-16    12  Sun     0.0
2020-03-23    13  Mon     0.0
2020-03-23    13  Tue     0.0
2020-03-23    13  Wed     0.0
2020-03-23    13  Thu     0.0
2020-03-23    13  Fri     0.0
2020-03-23    13  Sat     0.0
2020-03-23    13  Sun     0.0
2020-03-30    14  Mon     0.1
2020-03-30    14  Tue     0.1
2020-03-30    14  Wed    10.9
2020-03-30    14  Thu     0.0
2020-03-30    14  Fri     0.0
2020-03-30    14  Sat     0.0
2020-03-30    14  Sun     0.0
'''.strip()

        self.tab.parse_lines(rain.splitlines())
        self.assertEqual(str(self.tab), rain)

        self.tab.do("pivot long2")
        self.assertEqual(str(self.tab), longrain)

        self.tab.parse_lines(rain.splitlines())
        self.tab.do("pivot longb")
        self.assertEqual(str(self.tab), longrain)

        self.tab.parse_lines(rain.splitlines())
        self.tab.do("pivot longm")  # out of bounds == nop
        self.assertEqual(str(self.tab), rain)
