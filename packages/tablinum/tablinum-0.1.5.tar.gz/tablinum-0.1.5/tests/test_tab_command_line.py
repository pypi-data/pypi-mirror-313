#! /usr/bin/env python3

import subprocess
import unittest


class TestTableScript(unittest.TestCase):

    def test_me(self):
        '''Run the filter script'''
        cmd = 'tablinum_filter gen 16 wrap 4'.split()
        cp = subprocess.run(cmd, stdout=subprocess.PIPE)
        self.assertEqual(cp.returncode, 0)
        self.assertEqual(cp.stdout.decode('utf-8'), '''
1  5   9  13
2  6  10  14
3  7  11  15
4  8  12  16
'''.lstrip())

        cmd = 'tablinum_filter --file tests/test-input.txt 1 dp 003 rule 1 rule add'.split()
        cp = subprocess.run(cmd, stdout=subprocess.PIPE)
        self.assertEqual(cp.returncode, 0)
        self.assertEqual(cp.stdout.decode('utf-8'), '''
# Don't change this file!
x      Price      Val
---------------------
A        180   14.420
B        869  171.700
C        448  144.342
D        821   20.500
E        790   80.900
F        219   42.500
G        582   61.650
---------------------
Total   3909  536.012
'''.lstrip())
