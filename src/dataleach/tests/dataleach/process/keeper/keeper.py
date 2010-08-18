# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------


import unittest
import logging
import sys

from dataleach.process.keeper import Keeper, KeeperList, KeeperReg
from dataleach.datatypes import WordSet

SEARCH_SET = WordSet(["this is something", "this is nothing", "hello all",
                     "newline between this and this"])

INPUT_SET = ("""\nHello All,
So this is what I am working with.  A letter that does not say
much but does exist.  We have a newline between this\nand this.
This is something, and then again this is nothing.""")

logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format="%(message)s")



class test_scrubber(unittest.TestCase):

    def make_list(self, input):
        line = input.strip()
        line = line.lower()
        line = line.split(" ")
        return line

    def test_kl(self):
        k = KeeperList(SEARCH_SET)
        for element in k.keeperList:
            self.assertTrue(element in SEARCH_SET)
        for element in SEARCH_SET:
            self.assertTrue(element in k.keeperList)

    def test_kl_keep(self):
        k = KeeperList(SEARCH_SET)
        output = k.keep(INPUT_SET)
        self.assertEqual(len(output), 1)
        self.assertTrue('this is nothing' in output)

    def test_k(self):
        k = Keeper(SEARCH_SET)
        output = k.keep(INPUT_SET)
        for element in SEARCH_SET:
            self.assertTrue(element in output)

    def test_not_in(self):
        k = Keeper(WordSet(["Foo"]))
        output = k.keep(INPUT_SET)
        self.assertEqual(len(output), 0)

    def test_keeperreg(self):
        input = "ababab"

        reg1 = "a"
        expected1 = ["a", "a", "a"]
        output = KeeperReg(reg1).keep(input)
        self.assertEqual(expected1, output)

        reg2 = "b"
        expected2 = ["b", "b", "b"]
        output = KeeperReg(reg2).keep(input)
        self.assertEqual(expected2, output)

        reg3 = "[ab]+"
        expected3 = ["ababab"]
        output = KeeperReg(reg3).keep(input)
        self.assertEqual(expected3, output)
