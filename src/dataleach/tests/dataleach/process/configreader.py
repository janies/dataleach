# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------

import unittest
import os
from dataleach.process.configreader import *
from dataleach.datatypes import *

CONFIG_FILE = "testData/config/testConfig.conf"
SYS_CONFIG_FILE = "testData/config/sys.conf"
BAD_INDIV_FILE = "testData/config/badindividual.conf"
GOOD_CONFIG = "testData/config/goodwebsite.conf"


class test_config_error(unittest.TestCase):

    def test_config_reader(self):
        try:
            a = ConfigReader(CONFIG_FILE)
        except Exception as inst:
            print inst
        self.assertEqual(a.get("a", "val1"), "a1")
        self.assertEqual(a.get("a", "val2"), "a2")
        self.assertEqual(a.get("b", "val1"), "b1")
        self.assertEqual(a.get("b", "val2"), "b2")


    def test_valid(self):
        sections = {
            "a" : ["val1", "val2"],
            "b" : ["val1", "val2"],
            }
        a = ConfigReader(CONFIG_FILE)
        self.assertTrue(a.valid(sections))

    def test_invalid(self):
        sections = {
            "a" : ["val1", "val2"],
            "b" : ["val1"],
            }
        a = ConfigReader(CONFIG_FILE)
        self.assertFalse(a.valid(sections))
        sections = {
            "a" : ["val1", "val2"],
            }
        self.assertFalse(a.valid(sections))
    def test_config_reader_bad_file_name(self):
        try:
            a = ConfigReader("file")
        except Exception as inst:
            self.assertTrue(isinstance(inst, ConfigError))

    def test_config_system_bad_file_name(self):
        try:
            a = SystemConfig("file")
        except Exception as inst:
            self.assertTrue(isinstance(inst, ConfigError))

    def test_individual_bad_file_name(self):
        try:
            a = IndividualConfig("file")
            fail
        except Exception as inst:
            self.assertTrue(isinstance(inst, ConfigError))

    def test_good_config(self):
        a = None
        c = None
        try:
            a = IndividualConfig(GOOD_CONFIG)
            c = a.get_configuration()
            self.assertTrue(c.has_crawl())
            self.assertEqual(c.get_domainbase(), "google.com")
            self.assertEqual(c.get_max_page_count(), 50)

        except Exception as inst:
            print inst
            self.fail()
    def test_options(self):
        inDir = (os.path.abspath(os.curdir) + "/" +
                 "testData/config/indiv")
        outDir = (os.path.abspath(os.curdir) + "/" +
                  "testData")
        a = SystemConfig(SYS_CONFIG_FILE)
        self.assertEqual(inDir, a.get_in_dir())
        self.assertEqual(outDir, a.get_out_dir())

    def test_sources(self):
        base = (os.path.abspath(os.curdir) + "/" +
                 "testData/config/indiv/")
        configs = [base + "source1/source1.conf",
                   base + "source2/source2.conf",
                   base + "source3/source3.conf"]
        a = SystemConfig(SYS_CONFIG_FILE)
        l = []
        for inst in a.get_sources():
            l.append(inst.get_config_name())
        self.assertEqual(l, configs)


    def test_individual_options(self):
        base = os.path.abspath(os.curdir) + "/" 
        file = base + "testData/config/indiv/source1/source1.conf"
        a = IndividualConfig(file)
        self.assertEqual(a.config_name, file)
        self.assertEqual(a.name, "source1")
        self.assertEqual(a.type, "WEB_SOURCE")
        self.assertEqual(a.address, "http://www.google.com")
        self.assertEqual(a.search, '([0-9]{1,3}\.{3})[0-9]{1,3}')
        self.assertEqual(a.filter, '<?.*>')
        self.assertEqual(a.output_dir, base + "output/source1")

    def test_bad_individual(self):
        try:
            a = IndividualConfig(BAD_INDIV_FILE)
        except Exception as inst:
            self.assertTrue(isinstance(inst, ConfigError))

    def test_configuration(self):
        base = os.path.abspath(os.curdir) + "/" 
        file = base + "testData/config/indiv/source1/source1.conf"
        a = IndividualConfig(file)
        valid = Configuration(SEARCH_STRING='([0-9]{1,3}\.{3})[0-9]{1,3}',
                              FILTER_STRING='<?.*>' ,
                              OUTPUT_DIRECTORY=base+"output/source1",
                              SOURCE_TYPE=WEB_SOURCE)
        self.assertEqual(valid, a.get_configuration())
