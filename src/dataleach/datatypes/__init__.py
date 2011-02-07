# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------

import logging

__all__ = (
    "WordSet",
    "Configuration",
    "Format",
    "CONFIGURATION_VAR_LIST",
    "FILTER_STRING",
    "SEARCH_STRING",
    "OUTPUT_DIRECTORY",
    "SOURCE_TYPE",
    "WEB_SOURCE",
    "RSYNC_SOURCE",
    "RSS_SOURCE",
    "NAME_FORMAT",
    "REVERSE_ORDER",
    "DEFAULT_NAME_FORMAT",
)

# List of possible configuration variables
FILTER_STRING = "FILTER_STRING"
SEARCH_STRING = "SEARCH_STRING"
OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
SOURCE_TYPE = "SOURCE_TYPE"
WEB_SOURCE = "WEB_SOURCE"
RSYNC_SOURCE = "RSYNC_SOURCE"
RSS_SOURCE = "RSS_SOURCE"
NAME_FORMAT = "NAME_FORMAT"
REVERSE_ORDER = "REVERSE_ORDER"
CRAWL = "CRAWL"
DOMAIN_BASE="DOMAIN_BASE"

# With no options the format that weill be used for output files
DEFAULT_NAME_FORMAT = "%Y%m%d.%H"

# The list of possible configuration variables
CONFIGURATION_VAR_LIST = set(["FILTER_STRING", "SEARCH_STRING",
                              "OUTPUT_DIRECTORY", "SOURCE_TYPE",
                              "NAME_FORMAT", "REVERSE_ORDER",
                              "CRAWL", "DOMAIN_BASE"])

# String format variables
FORMAT_STRING_SUB = {"YEAR": "%Y", "MONTH": "%m", "DAY": "%d",
                     "HOUR": "%H", "MINUTE": "%M", "SECOND": "%S"}

SOURCE_TYPES = (WEB_SOURCE, RSYNC_SOURCE, RSS_SOURCE)

logger = logging.getLogger("dataleach.datatypes")

class WordSet(object):
    """
    Helper class defining a set of works for filtering and searhing.
    It is a wrapper class for Python Sets.  We wanted these sets to be
    explicitly marked as such.
    """

    def __init__(self, l):
        if isinstance(l, list):
            self.val = set(l)
        elif isinstance(l, set):
            self.val = l
        else:
            self.val = None

    def __eq__(self, other):
        if isinstance(other, WordSet):
            return self.val == other.val
        if isinstance(other, set):
            return self.val == other
        return False

    def __ne__(self, other):
	return not self.__eq__(other)

    def __in__(self, val):
	return val in self.val

    def to_set(self):
        return self.val

    def __iter__(self):
        return self.val.__iter__()

    def intersection(self, other):
        return self.__and__(other)

    def __and__(self, other):
        tmp = self
        if isinstance(other, set) or isinstance(other, list):
            tmp.val = self.val & other
        elif isinstance(other, WordSet):
            tmp.val = self.val & other.val
        return tmp

    def union(self, other):
        return self.__or__(other)

    def __or__(self, other):
        tmp = WordSet([])
        if isinstance(other, set) or isinstance(other, list):
            tmp.val = self.val | other
        elif isinstance(other, WordSet):
            tmp.val = self.val | other.val
	#self.__or__(args)
        return tmp 



class Configuration(object):
    """
    Helper class defining the overall configuration of a data source.
    """

    def __init__(self, **kargs):
        keys = set(kargs.keys())
        # check that the configuration options are valid
        if (len(CONFIGURATION_VAR_LIST) !=
            len(CONFIGURATION_VAR_LIST | keys)):
            wrong = keys - CONFIGURATION_VAR_LIST
            output = ""
            for element in wrong:
                output = "%s, %s" % (output, element)
                logger.error("Configuration has unsupported options %s"
                             % output)        

        # If there is a filter string use it, otherwise don't.
        if kargs.has_key(FILTER_STRING):
            val = kargs[FILTER_STRING]
            self.filter_string = val
        else:
            self.filter_string = None

        # If ther is a search string use it, otherwise don't.
        if kargs.has_key(SEARCH_STRING):
            val = kargs[SEARCH_STRING]
            self.search_string = val
        else:
            self.search_string = None

        # If there is an ordering use it, otherwise don't.
        if kargs.has_key(REVERSE_ORDER) and \
                kargs[REVERSE_ORDER] is not None:
            val = kargs[REVERSE_ORDER]
            try:
                self.reverse = int(val)
            except ValueError as ve:
                print ve
                self.reverse = 0 
        else:
            self.reverse = 0

        # If we need to crawl, do it.
        if kargs.has_key(CRAWL) and \
            kargs[CRAWL] is not None:
            val = kargs[CRAWL]
            if int(val) == 1:
                self.crawl = True
            else:
                self.crawl = False
        else:
            self.crawl = False

        # If we have a domain base we track it.
        if kargs.has_key(DOMAIN_BASE) and \
            kargs[DOMAIN_BASE] is not None:
            val = kargs[DOMAIN_BASE]
            self.domain_base = val
        else:
            self.domain_base = None

        # If there is an output directory, use it, otherwise
        # leave it blank.
        if kargs.has_key(OUTPUT_DIRECTORY):
            val = kargs[OUTPUT_DIRECTORY]
            self.output_directory = val
        else:
            self.output_directory = ""

        # Check our processing is capable of supporting the
        # source type.
        if (kargs.has_key(SOURCE_TYPE) and 
            kargs[SOURCE_TYPE] in SOURCE_TYPES):
            val = kargs[SOURCE_TYPE]
            self.source_type = val
        else:
            self.source_type = None

        # If there is a modification to the format, use it.
        if kargs.has_key(NAME_FORMAT):
            val = kargs[NAME_FORMAT]
            self.name_format = Format(val)
        else:
            self.name_format = Format(None)

    def has_domainbase(self):
        """
        Return true if there is a defined domainbase
        """
        if self.domain_base is None:
            return False
        return True

    def has_search(self):
        """
        Return True if there is a search string.
        """
        if self.search_string is None:
            return False
        return True

    def has_crawl(self):
        """
        Return the value of crawl
        """
        return self.crawl

    def has_filter(self):
        """
        Return Truc if there is a fiter string.
        """
        if self.filter_string is None:
            return False
        return True

    def get_domainbase(self):
        return self.domain_base

    def get_reverse(self):
        """
        Return the value of reverse
        """
        return self.reverse

    def get_output_directory(self):
        """
        Return the output directory.
        """
        return self.output_directory

    def get_source_type(self):
        """
        Return the source type
        """
        return self.source_type

    def get_format(self):
        """
        Return the format string
        """
        return self.name_format

    def __eq__(self, other):
        if isinstance(other, Configuration) and \
              self.source_type == other.source_type and \
              self.output_directory == other.output_directory and \
              self.filter_string == other.filter_string and \
              self.search_string == other.search_string:
            return True
        return False

    def __ne__(self):
        return not self.__eq__()


class Format(object):
    """
    Helper class for formating file names.
    """
    def __init__(self, s):
        if s is None:
            s = DEFAULT_NAME_FORMAT
        self.raw_string = s
        self.fmt_string = self.gen_fmt_string()

    def gen_fmt_string(self, **kargs):
        """
        Return a well formed string with variables replaced.

        @param kargs: The set of all variable values.
        """

        tmp = self.raw_string
        keys = kargs.keys()
        for key in keys:
            if key in FORMAT_STRING_SUB.keys():
                tmp = tmp.replace(FORMAT_STRING_SUB[key], kargs[key])
        tmp = tmp.replace("%", "")
        return tmp

    def get_string(self):
        return self.fmt_string
