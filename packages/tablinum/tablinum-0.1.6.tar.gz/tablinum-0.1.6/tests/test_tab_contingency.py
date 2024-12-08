#! /usr/bin/env python3

import unittest
import tablinum


class TestTableContingency(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.simple = '''
Category  Type A  Type B
------------------------
First         34      21
Second        58      72
'''.strip()

    def test_tapping(self):
        self.tab.parse_lines(self.simple.splitlines())
        self.tab.do("tap")   # default is noop
        self.assertEqual(str(self.tab), self.simple)

        self.tab.do("tap +1000")
        self.assertEqual(str(self.tab), '''
Category  Type A  Type B
------------------------
First       1034    1021
Second      1058    1072
'''.strip())

        self.tab.do("tap log(x)")
        self.assertEqual(str(self.tab), '''
Category         Type A         Type B
--------------------------------------
First     6.94119005507  6.92853781816
Second    6.96413561242  6.97728134163
'''.strip())

    def test_other_variables(self):
        self.tab.parse_lines(self.simple.splitlines())
        self.assertEqual(str(self.tab), self.simple)

        self.tab.do("tap /total")
        self.assertEqual(str(self.tab), '''
Category          Type A          Type B
----------------------------------------
First     0.183783783784  0.113513513514
Second    0.313513513514  0.389189189189
'''.strip())

    def test_only_variables(self):   # with no x values, the headings should not change!
        self.tab.parse_lines(self.simple.splitlines())
        self.assertEqual(str(self.tab), self.simple)

        self.tab.do("tap row_total*col_total/total dp 2")
        self.assertEqual(str(self.tab), '''
Category  Type A  Type B
------------------------
First      27.35   27.65
Second     64.65   65.35
'''.strip())
