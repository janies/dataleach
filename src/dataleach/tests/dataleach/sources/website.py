# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------


import sys
import os
import logging
import unittest

from dataleach.datatypes import *
from dataleach.sources.website import WebSite

#logging.basicConfig(level=logging.ERROR, stream=sys.stderr,
#                    format="%(message)s")

WEB_SITE = ("<html>Hello World <a href=\"www.google.com/help\")> g </a>" +
            "<a    href =   www.google.com/mail?name=\" \"> a </a>" +
            "<a  href = https://mail.google.com/ > mail </a>" +
            "</html>")
WEB_DATA = ("<html>Hello World. There is no place like " +
            "<a href=\"192.168.1.1\">127.0.0.1</a>.</html>")
NO_HTML =" hello world. there is no place like  127.0.0.1 . " 

class test_websites(unittest.TestCase):
    def test_empty(self):
        w = WebSite(None)
        self.assertEqual(len(w.get_data()), 0)

    def test_get_google(self):
        w = WebSite("http://www.google.com")
        self.assertNotEqual(len(w.get_data()), 0)

    def test_remove_html(self):
        config = Configuration(FILTER_STRING="<.*?>")
        w = WebSite(None, config)
        w.process_data(WEB_DATA)
        self.assertEqual(NO_HTML, w.get_data())

    def test_find_ips(self):
        config = Configuration(SEARCH_STRING=
                               "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
        w = WebSite(None, config)
        w.process_data(WEB_DATA)
        self.assertEqual(len(w.get_data()), 2)
        self.assertTrue("127.0.0.1" in w.get_data())
        self.assertTrue("192.168.1.1" in w.get_data())

    def test_find_plain_text_ip(self):
        config = Configuration(SEARCH_STRING=
                              "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",
                              FILTER_STRING = "<.*?>")
        w = WebSite(None, config)
        w.process_data(WEB_DATA)
        self.assertEqual(len(w.get_data()), 1)
        self.assertTrue("127.0.0.1" in w.get_data())

    def test_crawl_enable(self):
        config = Configuration(CRAWL=1, DOMAIN_BASE="")
        w = WebSite(None, None)
        self.assertFalse(w.crawl)
        w = WebSite(None, config)
        self.assertTrue(w.crawl)
        config = Configuration(CRAWL=0)
        w = WebSite(None, config)
        self.assertFalse(w.crawl)

    def test_find_urls(self):
        sites = ["www.google.com/help",
                 "www.google.com/mail",
                 "mail.google.com"]
        w = WebSite(None, None)
        w.domainBase = "google.com"
        w.get_urls(WEB_SITE)
        for site in sites:
            self.assertTrue(site in w.toProcess)
        self.assertTrue(w is not None)
