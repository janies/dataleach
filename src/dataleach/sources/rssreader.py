# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------

__all__ = (
    "RSSReader",
    "KeyNotFoundExcpetion",
)

import logging
import datetime
import feedparser
import sys
import re

from dataleach.sources.website import *
from dataleach.datatypes import *

logger = logging.getLogger("dataleach.sources.rssreader")
class KeyNotFoundException(Exception):
    """
    Exception for handling if an XML key is not found.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class RSSReader(object):
    """
    Class representing an rss feed.
    """
    def __init__(self, url, config=None):
        """
        Define an RSSReader.
        """
        self.config = config
        self.url = url
        try:
            self.feed = feedparser.parse(self.url)
        except Exception as inst:
            logger.warning("Exception: %s" % inst)
        self.date = datetime.datetime.today()


    def get_date(self):
        """
        @return: The date the data was retrieved.
        """
        return self.date

    def get_highest_level_keys(self):
        """
        @return: The highest level of the fields.
        """
        return self.feed.keys()

    def get(self, keys):
        """
        An internal method used for locating specific objects 
        within the feed.  It assumes the key list to contain 
        the path to the object of interest.

        @param keys: A list of the keys along the path to the 
        object of interst. Note, if the keylist goes through a 
        list object, the index is used as the key.

        @return: The object or raise an exception if the path is invalid.
        """
        if isinstance(keys, list):
            cur = self.feed
            for key in keys:
                if isinstance(cur, dict) and key in cur.keys():
                    cur = cur[key]
                elif isinstance(cur, list) and isinstance(key,int):
                    cur = cur[key]
                else:
                    raise KeyNotFoundException("'%s' is not a valid key %s" %
                                               (key, type(cur)))
            return cur
        else:
            return self.feed[keys]

    def get_feed(self):
        """
        @return: The raw feed obtained by feedparser.
        I{This should not be used by the user, except for debugging.}
        """
        return self.feed

    def get_url(self):
        """
        @return: The URL from which we are feeding
        """
        return self.url

    def get_num_entries(self):
        """
        @return: The number of entries obtained.
        """
        if self.has_entries():
            return len(self.get(["entries"]))
        return 0

    def has_entries(self):
        return self.feed.has_key("entries") and len(self.feed["entries"]) > 0

    def get_entries(self):
        """
        This assumes a top level 'entries' entity, which can be expected for 
        RSS news feeds.  This method will return a dictionary keyed by the
        title of each story provided.  Since reply messages tend to share
        title, we use a list to represent the links.
        """
        d = {}
        count = 0
        if not self.has_entries():
            raise KeyNotFoundException("No entries found")
        for entry in self.get(["entries"]):
            if not entry.has_key("title"):
                raise KeyNotFoundException("No title found")
            if not entry.has_key("link"):
                raise KeyNotFoundException(
                      "No Link associated with entry '%s'" %
                                           entry["title"])
            if d.has_key(entry["title"]):
                d[entry["title"]].append(str(entry["link"]))
            else:
                d[entry["title"]] = [str(entry["link"])]
        return d
 
    def __str__(self):
        """
        @return: String representing the RSSReader.
        """
        def recurs_str(cur, tabs, keylist):
            line = ""
            if isinstance(cur, list):
                if len(cur) > 0:
                    row = cur[0]
                    line += "%s(list)\n" % tabs
                    line += recurs_str(row, "%s  " % tabs, keylist) 
                return line
            if isinstance(cur, dict) or isinstance(cur, 
                                                   feedparser.FeedParserDict):
                for key in cur.keys():
                    line += "%sKEY: %s\n" % (tabs, key)
                    l = keylist
                    l.append(key)
                    line += recurs_str(cur[key], "%s  " % tabs, l)
            return line
        line = self.url
        line += recurs_str(self.feed, "", [])
        return line
 
    def output_file(self, name):
        """
        Generate a text output file.

        @param name: The base name of the file to be created.
        """
        entries = self.get_entries()
        count = 0
        for t in entries.keys():
            for url in entries[t]:
                 print url
                 site = WebSite(url, self.config)
                 output = "%s.%03d" % (name, count)
                 site.output_file(output)
                 count += 1

FEEDLIST = ["http://www.malwaredomainlist.com/hostslist/mdl.xml"] #["http://seclists.org/rss/dataloss.rss"]
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    #print "hi"
    title = open("testData/raw/title.txt", "w")
    for feed in FEEDLIST: 
        print feed
        r = RSSReader(feed)
        r.output_file("tmp/data")
        #entries = r.get_entries()
        #for t in entries.keys():
        #    print "\t%s" % t
        #    print "\t\t%s" % entries[t]
        #    config = Configuration(FILTER_STRING='<.*?>|<!--|-->|\&nbsp;|')
        #    site = WebSite(str(entries[t][0]), config)
        #    page = site.get_data().replace("\n", " ").replace("_", "")
        #    print "-----\n%s\n----" % (page)
        #    #print "diff: %s" % (site.webData == site.bk)
    #title.close()
