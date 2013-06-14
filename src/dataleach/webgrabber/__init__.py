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
import requests

__all__ = (
    "WebGrabber",
)

logger = logging.getLogger("dataleach.webgrabber")

TEXT = "text"

class WebGrabber(object):
    """
    Class for retrieving a webpage.
    """
    def __init__(self, url, user=None, password=None):
        if isinstance(url, str):
            self.url = url
        else:
            self.url = None
        self.data = ""
        self.content_type = TEXT
        self.user = user
        self.password = password
        self.failed = False

    def get_page(self):
        """
        Retrieve the webpage.
        """
        #logger.info("Attempting to get web page from '%s'" % self.url)
        try:
            if self.url is not None:
                params = {}
                if self.user and self.password:
                    params["auth"] =(self.user, self.password)
                response = requests.get(self.url, **params)
                self.data = response.text
                self.content_type = response.headers["content_type"]
                self.failed = not response.status_code < 300
            else:
                self.data = ""
                self.content_type = TEXT
        except Exception as inst:
            logger.warning("Failed to retrieve info (%s)" % inst)
            self.failed = True

    def get_content_type(self):
        """
        @return: The content type returned by the request
        """
        return self.content_type

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
