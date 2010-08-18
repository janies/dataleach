# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------

import sys
import logging

from dataleach.process.keeper import Keeper, KeeperReg
from dataleach.process.scrubber import Scrubber, ScrubReg
from dataleach.webgrabber import WebGrabber
from dataleach.datatypes import *

__all__ = (
    "Rsync",
)

logger = logging.getLogger("dataleach.sources.rsync")
class Rsync(object):
    def __init__(self, url, config=None):
        if isinstance(url, str):
            self.url = url
        else:
            self.url = ""
        self.data = ""
        pass

    def retrieve_data(self):
        pass

    def process_data(self, html):
        pass
    
    def generate_filters(self):
        if self.config == None:
            return (None, None)
        if self.config.has_search():
            search = KeeperReg(self.config.search_string)
        else:
            search = None
        if self.config.has_filter():
            scrub = ScrubReg(self.config.filter_string)
        else:
            scrub = None
        return (search, scrub)

    def get_data(self):
        return self.data
