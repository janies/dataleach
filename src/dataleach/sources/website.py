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

from dataleach.process.keeper import Keeper, KeeperReg
from dataleach.process.scrubber import Scrubber, ScrubReg
from dataleach.webgrabber import WebGrabber
from dataleach.datatypes import *

__all__ = (
    "WebSite",
)

logger = logging.getLogger("dataleach.sources.website")
class WebSite(object):
    """
    Class representing a website.
    """
    def __init__(self, url, config=None):
        self.webData = None
        if isinstance(url, str):
            self.url = url
            html = self.retrieve_data()
        else:
            self.url = None
            html = ""
        self.config = config
        self.process_data(html)

    def retrieve_data(self):
        """
        Retrieve the data from the website.
        """
        w = WebGrabber(self.url)
        w.get_page()
        if w.done():
            return w.get_data()
        else:
            logger.warning("Using empty string as WebSite data")
            return ""

    def process_data(self, html):
        """
        Do the web grab from the website and all the filtering
        and searching.
        """
        #print html[:100]
        self.webData = html
	self.bk = html
        (search, scrub, reverse) = self.generate_filters()
        if reverse == 0:
            if scrub is not None:
                logger.debug("Scrubbing data")
                self.webData = scrub.scrub(self.webData)
            if search is not None:
                logger.debug("Searching data")
                self.webData = search.keep(self.webData)
        else:
            if search is not None:
                logger.debug("Searching data")
                self.webData = search.keep(self.webData)
            if scrub is not None:
                logger.debug("Scrubbing data")
                self.webData = scrub.scrub(self.webData)
        
        #print "-------"
        #print self.webData[:100]
    
    def generate_filters(self):
        """
        Generate the list of filters from the configutation.
        """
        if self.config == None:
            return (None, None, 0)
        if self.config.has_search():
            search = KeeperReg(self.config.search_string)
        else:
            search = None
        if self.config.has_filter():
            scrub = ScrubReg(self.config.filter_string)
        else:
            scrub = None
        return (search, scrub, self.config.get_reverse())

    def get_data(self):
        """
        return the data from the web page
        """
        return self.webData

    def output_file(self, name):
        """
        generate the output file with the user specified name.

        @param name: The file name to be used
        """
        if os.path.exists(name):
            count = 1
            tmp = "%s_%d" % (name, count)
            while os.path.exists(tmp):
                count += 1
                tmp = "%s_%d" % (name,count)
            logger.warning(("unable to use '%s' as an output " +
                            "using '%s' instead.") % (name, tmp)) 
            name = tmp
        output = open(name, "w")
        #print self.get_data()
        if isinstance(self.get_data(), list):
            for l in self.get_data():
                output.write("%s\n" % l)
        else:
            output.write(str(self.get_data()))
        output.close()


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
                        format="%(message)s")
    config = Configuration(FILTER_STRING=r"<.*?>")
    a = WebSite("http://www.google.com", config)
    print "______________________________"
    print a.get_data()
    print "______________________________"

if __name__ == "__main__":
    main()
