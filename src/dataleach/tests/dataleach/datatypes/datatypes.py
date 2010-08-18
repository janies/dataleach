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

from dataleach.datatypes import *

logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format="%(message)s")


class test_dataTypes(unittest.TestCase):

    def test_word_set_init(self):
        input_set = ["hello", "this one", "that one"]
        list_input = WordSet(input_set)
        set_input = WordSet(set(input_set))
        for element in input_set:
            self.assertTrue(element in set_input)
            self.assertTrue(element in list_input)

    def test_word_set_operations(self):
        input1 = ["hello"]
        input2 = ["bye"]
        set1 = WordSet(input1)
        set2 = WordSet(input2)
        self.assertTrue("hello" in set1)
        self.assertTrue("bye" in set2)

        total_op = set1 | set2
        total_method = set1.union(set2)
        self.assertTrue(total_op == total_method)
        self.assertTrue(total_op != set2)
        self.assertTrue(total_op != set1)

        input3 = ["a", "b", "c"]
        input4 = ["c", "d"]
        total = ["c"]
        set3 = WordSet(input3)
        set4 = WordSet(input4)
        total = WordSet(total)
        total_op = set3 & set4
        total_method = set3.intersection(set4)
        self.assertTrue(total == total_op)
        self.assertTrue(total == total_method)

    def test_configuration_init(self):
        a = Configuration()
        self.assertEqual(a.filter_string, None)
        self.assertEqual(a.search_string, None)

        a = Configuration(FILTER_STRING="f")
        self.assertEqual(a.filter_string, "f")
        self.assertEqual(a.search_string, None)

        a = Configuration(SEARCH_STRING="s")
        self.assertEqual(a.filter_string, None)
        self.assertEqual(a.search_string, "s")

        a = Configuration(SEARCH_STRING="search",
                          FILTER_STRING="filter")
        self.assertEqual(a.filter_string, "filter")
        self.assertEqual(a.search_string, "search")

        a = Configuration(OUTPUT_DIRECTORY="someDirectory")
        self.assertEqual(a.get_output_directory(), "someDirectory")
        a = Configuration(SOURCE_TYPE=WEB_SOURCE)
        self.assertEqual(a.get_source_type(), WEB_SOURCE)
        a = Configuration(SOURCE_TYPE=RSS_SOURCE)
        self.assertEqual(a.get_source_type(), RSS_SOURCE)
        a = Configuration(SOURCE_TYPE=RSYNC_SOURCE)
        self.assertEqual(a.get_source_type(), RSYNC_SOURCE)
        a = Configuration(SOURCE_TYPE="Not Valid")
        self.assertEqual(a.get_source_type(), None)

    def test_format(self):
        a = Configuration()
        self.assertEqual(a.get_format().raw_string,
                         DEFAULT_NAME_FORMAT)
        a = Format("%Y%m%d:%H:%M:%S_done")
        self.assertEqual("20090516:00:01:02_done",
                         a.gen_fmt_string(YEAR="2009", MONTH="05",
                                          DAY="16", HOUR="00", MINUTE="01",
                                          SECOND="02"))
        a = Format("%Y%m%d:%%H:%M:%S_done")
        self.assertEqual("20090516:00:01:02_done",
                         a.gen_fmt_string(YEAR="2009", MONTH="05",
                                          DAY="16", HOUR="00", MINUTE="01",
                                          SECOND="02"))
        a = Format("%Y%m%d:%H:%M:%S_done%X")
        self.assertEqual("20090516:00:01:02_doneX",
                         a.gen_fmt_string(YEAR="2009", MONTH="05",
                                          DAY="16", HOUR="00", MINUTE="01",
                                          SECOND="02"))

