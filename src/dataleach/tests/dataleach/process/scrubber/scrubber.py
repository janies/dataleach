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

import os
from dataleach.process.scrubber import Scrubber, ARTICLES, PREPOSITIONS
from dataleach.process.scrubber import CONJUNCTIONS, ScrubReg, SECURITY_TITLE
from dataleach.process.scrubber import ScrubList


logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format="%(message)s")

INPUT_FILE = "testData/raw/testText.txt"
class test_scrubber(unittest.TestCase):
    def create_string(self):
        file = open(INPUT_FILE, "r")
        s = ""
        for line in file:
            s += line
        file.close()
        return s

    def make_list(self, input):
        line = input.strip()
        line = line.lower()
        line = line.split(" ")
        return line

    def test_sl_init(self):
        for type in (ARTICLES, CONJUNCTIONS, PREPOSITIONS):
            sl = ScrubList(type)
            for word in type:
                self.assertTrue(word in sl.removeList)

    def test_remover(self):
        input = self.create_string()
        inputList = self.make_list(input)
        count = 0
        for t in (ARTICLES, CONJUNCTIONS, PREPOSITIONS):
            sl = Scrubber([t])
            for word in t:
                if word in inputList:
                    count += 1
                    self.assertTrue(word in inputList)
                    self.assertFalse(word in sl.scrub(input))
        self.assertNotEqual(count, 0)

    def test_scrubreg(self):
        input = "abcddd"

        reg1 = "ddd"
        expected1 = "abc "
        output = ScrubReg(reg1).scrub(input)
        self.assertEqual(output, expected1)

        reg2 = "dd"
        expected2 = "abc d"
        output = ScrubReg(reg2).scrub(input)
        self.assertEqual(output, expected2)
        
        reg3 = "d"
        expected3="abc   "
        output = ScrubReg(reg3).scrub(input)
        self.assertEqual(output, expected3)
