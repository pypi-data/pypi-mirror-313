#! /usr/bin/env python3

import unittest

import tablinum


class TestTableTextManipulation(unittest.TestCase):

    def setUp(self):
        self.tab = tablinum.Table()
        self.words = '''
Crosby crines hobbies sola @ 141  <---- 32
Juno aril horn culicid | 744  <---- 28
Krishna parched debouch moutan ! 489  <---- 36
Lille gowd medius tanrec * 886  <---- 30
Malvern wired melanin emesis % 264  <---- 34
Sulus package longan nuzzers [ 489  <---- 34
'''.strip()
        self.tableau = '''
Crosby   crines   hobbies  sola     @  141  <----  32
Juno     aril     horn     culicid  |  744  <----  28
Krishna  parched  debouch  moutan   !  489  <----  36
Lille    gowd     medius   tanrec   *  886  <----  30
Malvern  wired    melanin  emesis   %  264  <----  34
Sulus    package  longan   nuzzers  [  489  <----  34
'''.strip()

    def test_functions(self):
        self.tab.parse_lines(self.tableau.splitlines())
        self.tab.do("arr abcd")
        self.assertEqual(str(self.tab), '''
Crosby   crines   hobbies  sola
Juno     aril     horn     culicid
Krishna  parched  debouch  moutan
Lille    gowd     medius   tanrec
Malvern  wired    melanin  emesis
Sulus    package  longan   nuzzers
'''.strip())
        self.tab.do("arr (upper(a))bcd)")
        self.assertEqual(str(self.tab), '''
CROSBY   crines   hobbies  sola
JUNO     aril     horn     culicid
KRISHNA  parched  debouch  moutan
LILLE    gowd     medius   tanrec
MALVERN  wired    melanin  emesis
SULUS    package  longan   nuzzers
'''.strip())
        self.tab.do("arr (caps(a)+' '+caps(b))cd")
        self.assertEqual(str(self.tab), '''
Crosby Crines    hobbies  sola
Juno Aril        horn     culicid
Krishna Parched  debouch  moutan
Lille Gowd       medius   tanrec
Malvern Wired    melanin  emesis
Sulus Package    longan   nuzzers
'''.strip())
        self.tab.do("arr (lower(a))")
        self.assertEqual(str(self.tab), '''
crosby crines
juno aril
krishna parched
lille gowd
malvern wired
sulus package
'''.strip())
