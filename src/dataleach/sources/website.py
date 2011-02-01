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
        self.config = config
        self.webData = None
        if self.config is None or not self.config.has_crawl():
            self.crawl = False
        else:
            self.crawl = True
        self.toProcess = [url]
        self.processed = []
        self.gen_url_filters(url)
        self.iterate_pages()

    def gen_url_filters(self, url):
        """
        Generate the set of filters that we can use to get other URLs
        from this domain.
        """
        if url is not None and isinstance(url, str):
            url = url.split(".")
            if len(url) < 2: 
                self.domainUrl = search.keep("[a-zA-Z\-0-9\.]*%s\..%s[a-zA-Z\-0-9\./]*" % 
                                             (url[-2], url[-1]))
            else:
                self.domainUrl = None
        else:
            self.domainUrl = None

    def get_urls(self, data):
        """
        Process the page looking for URLs to traverse
        """
        if self.domainUrl is not None and data is not None:
            data = self.domainUrl.keep(data)
            print data

    def iterate_pages(self):
        """
        This iterates through the list of URLS available for use.
        """
        for url in self.toProcess:
            if url not in self.processed:
                self.processed.append(url)
                if isinstance(url, str):
                    self.url = url
                    html = self.retrieve_data()
                else:
                    self.url = None
                    html = ""
                if self.crawl:
                    self.get_urls(html)
                self.process_data(html)
            self.toProcess.remove(url)

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
        (search, scrub, reverse) = self.generate_filters()
        if reverse == 0:
            if scrub is not None:
                logger.debug("Scrubbing data")
                html = scrub.scrub(html)
            if search is not None:
                logger.debug("Searching data")
                html = search.keep(html)
        else:
            if search is not None:
                logger.debug("Searching data")
                html = search.keep(html)
            if scrub is not None:
                logger.debug("Scrubbing data")
                html = scrub.scrub(html)
        if not self.crawl or self.webData is None:
            self.webData = html
        elif isinstance(self.webData, str):
            self.webData += html
        elif isinstance(self.webData, set):
            self.webData.append(html)
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
        #if len(self.webData) == 1:
        #    return self.webData[0]
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
