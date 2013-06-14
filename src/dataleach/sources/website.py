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
import re
import urlparse

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
        """
        Define a WebSite.
        """
        self.config = config
        self.webData = None
        self.crawl = False
        self.domainBase = None
        self.max_page_count = 1
        if config is not None:
            self.crawl = self.config.has_crawl()
            self.domainBase = self.config.get_domainbase()
            self.max_page_count = self.config.get_max_page_count()
        self.get_hrefs = KeeperReg("href\s*=\s*[^ <>]*[a-zA-Z0-9]")
        self.toProcess = [url]
        self.max_page_count -= 1
        self.processed = []
        self.iterate_pages()

    def get_next(self):
        """
        @return: The next URL in the list.
        """
        if len(self.toProcess) > 0:
            out = self.toProcess.pop()
            self.processed.append(out)
            return out
        return None

    def get_urls(self, data):
        """
        Process the page looking for URLs to traverse

        @param data: The raw webpage text.
        """
        if self.get_hrefs is not None and data is not None:
            for url in self.get_hrefs.keep(data):
                # This is removing junk from the string.  It needs to be
                # cleaner.
                #print "Start: %s" % url
                url = url.replace("href", "")
                url = url.replace("=", "")
                url = url.replace("\"", "")
                url = url.replace('\\','')
                url = url.strip()
                parsed = urlparse.urlparse(url)
                url = ("http" if len(parsed.scheme) == 0 else parsed.scheme)  + \
                    "://" + parsed.netloc + parsed.path
                if url not in self.toProcess and \
                   url not in self.processed and \
                   self.max_page_count > 0:
                    if self.domainBase is not None:
                        if url.rfind(self.domainBase) != -1 and \
                           url.rfind("@%s" % self.domainBase) == -1:
                            self.toProcess.append(url)
                            self.max_page_count -= 1
                    else:
                        self.toProcess.append(url)
                        self.max_page_count -= 1
                    

    def iterate_pages(self):
        """
        Iterate through the list of URLS available for use.
        """
        url = self.get_next()
        logger.debug("iterating over %s" % url)
        while url is not None:
            logger.debug("toProcess: %s" % self.toProcess)
            logger.debug("Processed: %s" % self.processed)
            logger.debug("processing: %s" % url)
            #self.processed.append(url)
            if isinstance(url, str):
                logger.debug("url is a string")
                self.url = url
                html = self.retrieve_data()
            else:
                self.url = None
                html = ""
            if self.crawl:
                self.get_urls(html)
            self.process_data(html)
            url = self.get_next()

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
        print html[:100]
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
            self.webData += "\n\n####\n\n" + html
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
        @return: The data from the web page
        """
        #if len(self.webData) == 1:
        #    return self.webData[0]
        if self.webData is None:
            return ""
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
    #logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
    #                    format="%(message)s")
    config = Configuration(CRAWL=1, 
                           DOMAIN_BASE=sys.argv[2],
                           MAX_PAGE_COUNT=10)
    a = WebSite(sys.argv[1], config)
    print "______________________________"
    print a.get_data()
    print "______________________________"
    print "Processed"
    count = 0
    for url in a.processed:
        count += 1
        print "%d) %s" % (count, url)
    print "To Process"
    count = 0
    for url in a.toProcess:
        count += 1
        print "%d) %s" % (count, url)
    print a.max_page_count

if __name__ == "__main__":
    main()
