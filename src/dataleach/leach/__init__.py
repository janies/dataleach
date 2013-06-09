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
import os
import optparse
import datetime

from dataleach.datatypes import *
from dataleach.process.configreader import *
from dataleach.sources.rssreader import RSSReader
from dataleach.sources.rsync import Rsync
from dataleach.sources.website import WebSite
from dataleach.process.keeper import Keeper, KeeperList, KeeperReg
from dataleach.process.scrubber import *


__all__ = (
    "LeachSystem",
)

logger = logging.getLogger("datalaeach.leach")
CONFIG = "CONFIG"
DESCRIPTION = """This script uses a configuration file to extract infomration
from a collection of web sources."""


class DataLeach(object):
    """
    The class defining the data leach system.
    """
    def __init__(self, args):
        """
        Declare a DataLeach.
        """
        self.config_file = None
        self.parse_options()
        if self.config_file is None:
            logger.error("Must specify a configuration file")
            sys.exit(0)
        try:
            self.config = SystemConfig(self.config_file)
        except Exception as inst:
            logger.error("Unable to open file '%s'\n%s" %
                  (self.config_file, inst))
            sys.exit(0)
        self.process_sources(self.config)

    def parse_options(self):
        """
        Parser for command line arguments provided.
        """
        parser = optparse.OptionParser(description="")
        parser.add_option("-c", "--config", dest=CONFIG,
                          help="Configuration file to use")
        options, args = parser.parse_args()
        self.config_file = options.CONFIG 

    def process_sources(self, config):
        """
        Take a system configuration and process the options.

        @param config: a system configuration.
        """
        sources = config.get_sources()
        if (not isinstance(sources, list)) or \
                len(sources) == 0:
            logger.warning("No Individual configurations found at %s '%s'" %
                   (type, config.get_in_dir()))
            sys.exit(2)
        for source in sources:
            logger.warning("Processing: %s" % (source.get_config_name()))
            self.process_source(source.address, source.get_configuration())

    def process_source(self, url, config):
        """
        Process an individual source.  This runs the fetching of a 
        data source, determines which class should represent the output,
        and selects where the output goes.

        @param url: The string URL of the configuration.
        @param config: The configuration of the system.
        """
        type = config.get_source_type()
        today = datetime.datetime.today()
        file = config.get_format().gen_fmt_string(YEAR="%4d"%today.year,
                                                  MONTH="%02d"%today.month,
                                                  DAY="%02d"%today.day,
                                                  HOUR="%02d"%today.hour,
                                                  MINUTE="%02d"%today.minute,
                                                  SECOND="%02d"%today.second)
        file = "%s/%s" % (config.get_output_directory(), file)
	try:
            if type == WEB_SOURCE:
                source = WebSite(url, config)
                source.output_file(file)
            elif type == RSS_SOURCE:
                source = RSSReader(url, config) 
                source.output_file(file)
            elif type == RSYNC_SOURCE:
                source = Rsync(url, config)
        except Exception as inst:
            os.system("touch %s" % file)
            logger.warning("No Data found at '%s'" % url) 

def main():
    args = sys.argv
    logging.basicConfig(format="%(message)s", level=logging.WARNING)
    process = DataLeach(args)


if __name__ == "__main__":
    main()
