#! /usr/bin/env python3

import unittest

import tablinum


class TestTableLevels(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.covid = '''
Country         Region   Deaths  Death rate  Total Cases
--------------------------------------------------------
Argentina       America   51965         117      2107365
Belgium         Europe    22077         192       771511
Brazil          America  254942         122     10551259
Canada          America   21990          59       871694
Chile           America   20572         110       824625
Colombia        America   59766         120      2251690
Czech Republic  Europe    20339         191      1235480
Ecuador         America   15811          92       286155
France          Europe    85582         132      3686813
Germany         Europe    70152          84      2450306
Hungary         Europe    14974         154       428599
India           Asia     157157          12     11112241
Indonesia       Asia      36166          14      1334634
Iran            Asia      60073          73      1631169
Italy           Europe    97699         161      2925265
Mexico          America  185715         147      2086938
Netherlands     Europe    15566          91      1088886
Peru            America   46494         145      1329805
Poland          Europe    43769         115      1706986
Portugal        Europe    16317         159       804562
Romania         Europe    20350         104       801994
Russia          Asia      84700          58      4198400
South Africa    Africa    49993          86      1513393
Spain           Europe    69142         148      3188553
Turkey          Asia      28569          35      2701588
UK              Europe   122849         183      4176554
Ukraine         Europe    27472          62      1399813
US              Europe   510900         156     28494973
'''.strip()

        self.levels = '''
# Country: All distinct.
# Region: Europe 14, America 8, Asia 5, Africa 1
# Death rate: Min: 12  Q25: 81.25  Median: 116.0  Mean: 111.5  Q75: 149.50  Max: 192
'''.strip()

    def test_levels(self):
        "show messages about column contents"
        self.tab.parse_lines(self.covid.splitlines())
        self.assertEqual(str(self.tab), self.covid)

        self.tab.do('levels')  # missing predicate does nothing
        self.assertEqual(str(self.tab), self.covid)

        self.tab.do('levels .')  # broken predicate gives error
        self.assertEqual(str(self.tab), '?! colspec .\n' + self.covid)

        self.tab.do('levels ABD')
        self.assertEqual(str(self.tab), self.levels + '\n' + self.covid)

        self.tab.do('levels c')
        self.assertEqual(str(self.tab), '# c: All distinct.\n' + self.covid)
