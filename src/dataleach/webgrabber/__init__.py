# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------


import logging
import sys
import urllib2

__all__ = (
    "WebGrabber",
)

logger = logging.getLogger("dataleach.webgrabber")

class WebGrabber(object):
    """
    Class for retrieving a webpage.
    """
    def __init__(self, url):
        if isinstance(url, str):
            self.url = url
        else:
            self.url = None
        self.data = ""
        self.failed = False

    def get_page(self):
        """
        Retrieve the webpage.
        """
        #logger.info("Attempting to get web page from '%s'" % self.url)
        try:
            if self.url is not None:
                page = urllib2.urlopen(self.url)
            else:
                page = ""
            self.data = ""
            for line in page:
                self.data += line
        except Exception as inst:
            logger.warning("Failed to retrieve info (%s)" % inst)
            self.failed = True

    def get_data(self):
        """
        @return: The data retrieved from a web page as a string.
        """
        return self.data

    def done(self):
        """
        called when a webpage conpletes processing.

        @return: True
        """
        return not self.failed

    def __eq__(self, other):
        """
        Is the webpage equal to other.

        @param other: The WebGrabber to be compared to this instance.

        @return: True if other is equal to this instance
        """
        if isinstance(other, WebGrabber):
            if self.url == other.url and self.data == other.data:
                return True
        return False

    def __ne__(self, other):
        """
        Is the webpage not equal to other.

        @param other: The WebGrabber to be compared to this instance.

        @return: True if other is not equal to this instance
        """
        return not self.__eq__(other)

def main():
    if len(sys.argv) != 2:
        print("Must supply a URL")
    w = WebGrabber(sys.argv[1])
    sys.stdout.write("Grabbing data from '%s' ... " % sys.argv[1])
    w.get_page()
    if w.done():
        print "Done"
        print w.get_data()
    else:
        print "Fail"
if __name__ == "__main__":
    main()
