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
import datetime

from dataleach.sources.rssreader import RSSReader, KeyNotFoundException

TEST_DATA_DIR = "testData/xmlFeeds"
EMPTY_FILE = "testData/bad/bad.rss"
TEST_FILE_LIST = os.listdir(TEST_DATA_DIR)
NUM_ENTRIES = {"bugtraq":15, "cert":15, "dailydave":15, "darknet":10, 
               "dataloss":15, "firewallwizard":15, "fulldisclosure":15, 
               "funsec":15, "honeypots":15, "idsfocus":5, "infosec":15, 
               "mssec":15, "opensource":15, "packetstorm":10, 
               "pentesting":15, "sansrisk":125, "securitybasics":15, 
               "securityfocus":21, "stormcenter":10, "webapp":15}

def print_entries(r):
    d = r.get_entries()
    count = 0
    for title in d.keys():
        print "%d) %s - %s" % (count, title, d[title])
        count += 1

class test_rssreader(unittest.TestCase):
    def test_rss_get(self):
        for file in TEST_FILE_LIST:
            file = "%s/%s" % (TEST_DATA_DIR, file) 
            r = RSSReader(file)
            self.assertEqual(len(r.feed["entries"]), r.get_num_entries())
            self.assertEqual(r.url, file)
            d = r.get_entries()
            for entry in r.feed["entries"]:
                rawKey = entry["title"]
                self.assertTrue(d.has_key(rawKey))
                self.assertTrue(entry["link"] in d[rawKey])
            self.assertTrue(r.has_entries())
            r.feed["entries"] = {}
            self.assertFalse(r.has_entries())
            del r.feed["entries"]
            self.assertFalse(r.has_entries())

    def test_empty_data(self):
        r = RSSReader(EMPTY_FILE)
        self.assertFalse(r.has_entries())
        errCount = 0
        try:
            r.get_entries()
        except Exception as ans:
            errCount += 1
            self.assertTrue(isinstance(ans, KeyNotFoundException))
        r.feed["entries"] =[]
        try:
            r.get_entries()
        except Exception as ans:
            errCount += 1
            self.assertTrue(isinstance(ans, KeyNotFoundException))
        r.feed["entries"].append({})
        try:
            r.get_entries()
        except Exception as ans:
            errCount += 1
            self.assertTrue(isinstance(ans, KeyNotFoundException))
        r.feed["entries"][0]["title"]="hi"
        try:
            r.get_entries()
        except Exception as ans:
            errCount += 1
            self.assertTrue(isinstance(ans, KeyNotFoundException))
        r.feed["entries"][0]["link"]="hi2"
        try:
            r.get_entries()
        except Exception as ans:
            errCount += 1
            self.assertTrue(isinstance(ans, KeyNotFoundException))
        self.assertEqual(errCount, 4)
        #print_entries(r)

    def test_get_date(self):
        today = datetime.datetime.today()
        for file in TEST_FILE_LIST:
            file = "%s/%s" % (TEST_DATA_DIR, file)
            r = RSSReader(file)
            readDate = r.get_date()
            self.assertEqual(today.year, readDate.year)
            self.assertEqual(today.month, readDate.month)
            self.assertEqual(today.day, readDate.day)

    def test_feed(self):
        for file in TEST_FILE_LIST:
            file  = "%s/%s" % (TEST_DATA_DIR, file)
            r = RSSReader(file)
            self.assertEqual(r.get_url(), file)

    def test_num_entries(self):
        for file in TEST_FILE_LIST:
            f = "%s/%s" % (TEST_DATA_DIR, file)
            r = RSSReader(f)
            self.assertEqual(NUM_ENTRIES[file], r.get_num_entries())
            
