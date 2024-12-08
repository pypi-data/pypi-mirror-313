#! /usr/bin/env python3

import unittest

import tablinum


class TestTableHelp(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.help = '''
Try one of these: add arr clear ditto dp dup filter gen group help
label levels make noblanks nospace pivot pop push roll rule sf shuffle
sort tap uniq unwrap unzip wrap xp zip
        '''.strip()

        # textwrap wraps at 70 by default
        self.verbs = '''
Functions for arr: abs all angle any base bool caps chr comb cos cosd
date dir divmod dow epoch exp factors floor format gcd hex hms hr
hypot int lcm len log log10 lower make_date max mexp min minp mins
mlog oct ord perm pi pow randomd reversed round secs sin sind sorted
sqrt str sum tan tand tau time uktaxyear upper
'''.strip()

    def test_help(self):
        self.tab.do("help")
        self.assertEqual(str(self.tab), self.help)

        self.tab.do("help Arr")
        self.assertEqual(str(self.tab), self.verbs)
