#! /usr/bin/env python3

import unittest

import tablinum


class TestTableRoller(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()

    def test_rolling(self):
        "Roll up and down"
        rain = '''
2019-12-30  1  0.0  0.2
2020-01-06  2  0.5  0.0
2020-01-13  3  5.3  1.7
2020-01-20  4  0.0  0.0
'''.strip()
        rolled = '''
2020-01-20  4  0.0  0.0
2019-12-30  1  0.0  0.2
2020-01-06  2  0.5  0.0
2020-01-13  3  5.3  1.7
'''.strip()
        rolled_b_down = '''
2019-12-30  4  0.0  0.2
2020-01-06  1  0.5  0.0
2020-01-13  2  5.3  1.7
2020-01-20  3  0.0  0.0
'''.strip()
        rolled_bc_up = '''
2019-12-30  2  0.5  0.2
2020-01-06  3  5.3  0.0
2020-01-13  4  0.0  1.7
2020-01-20  1  0.0  0.0
'''.strip()
        self.tab.parse_lines(rain.splitlines())
        self.assertEqual(str(self.tab), rain)

        self.tab.do('roll')  # missing predicate rolls whole table
        self.assertEqual(str(self.tab), rolled)

        self.tab.parse_lines(rain.splitlines())
        self.tab.do('roll b')  # down...
        self.assertEqual(str(self.tab), rolled_b_down)

        self.tab.parse_lines(rain.splitlines())
        self.tab.do('roll BC')  # up
        self.assertEqual(str(self.tab), rolled_bc_up)

        self.tab.parse_lines(rain.splitlines())
        self.tab.do('roll ?')  # error
        self.assertEqual(str(self.tab), '?! colspec ?\n' + rain)

        rain_header = '''
Date        N  Mon  Tue
2019-12-30  1  0.0  0.2
2020-01-06  2  0.5  0.0
2020-01-13  3  5.3  1.7
2020-01-20  4  0.0  0.0
'''.strip()
        rain_header_rolled = '''
Date        N  Mon  Tue
2020-01-20  4  0.0  0.0
2019-12-30  1  0.0  0.2
2020-01-06  2  0.5  0.0
2020-01-13  3  5.3  1.7
'''.strip()

        self.tab.parse_lines(rain_header.splitlines())
        self.assertEqual(str(self.tab), rain_header)

        self.tab.do('roll @')  # missing predicate rolls whole table but not header
        self.assertEqual(str(self.tab), rain_header_rolled)
