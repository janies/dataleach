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
import getopt
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


class DataLeach(object):
    """
    The class defining the data leach system.
    """
    def __init__(self, args):
        """
        Declare a DataLeach.
        """
        self.configFile = None
        self.parse_options()
        if self.configFile is None:
            usage("Must specify a configuration file")
        try:
            self.config = SystemConfig(self.configFile)
        except Exception as inst:
            usage("Unable to open file '%s'\n%s" %
                  (self.configFile, inst))
        self.process_sources(self.config)

    def parse_options(self):
        """
        Parser for command line arguments provided.
        """
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       "hc:",
                                       ["help", "config="])
        except getopt.GetoptError, err:
            usage(str(err))
        for o,a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-c", "--config"):
                self.configFile = a
            else:
                usage("'%s' is not a recognized option" % o)

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

def usage(error=None):
    """
    Print the system usage to the screen and exit.

    @param error: If an error is provided, it will be printed.
    """
    if error is not None:
        l = "%s\n" % error
    else:
        l =""
    l += "usage: %s " % sys.argv[0]
    l += "[-h | --help] [-c | --config=FILE]\n\n"
    l += "--help No Arg.  Print the usage output and exit\n"
    l += "--config Req Arg.  Use the configuration file to\n"
    l += "         configure the system"
    logger.warning(l)
    sys.exit(0)

def main():
    args = sys.argv
    logging.basicConfig(format="%(message)s", level=logging.WARNING)
    process = DataLeach(args)


if __name__ == "__main__":
    main()
