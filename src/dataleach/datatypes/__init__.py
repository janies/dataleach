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
    "CRAWL",
    "DOMAIN_BASE",
    "MAX_PAGE_COUNT",
    "DEFAULT_NAME_FORMAT",
    "JSON_FILE",
)

# List of possible configuration variables

FILTER_STRING = "FILTER_STRING" #: Filter string configuration variable name
SEARCH_STRING = "SEARCH_STRING" #: Search String configuration variable name
OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY" #: Output directory configuration variable name
SOURCE_TYPE = "SOURCE_TYPE"     #: Source type configuration variable name
WEB_SOURCE = "WEB_SOURCE"       #: Web Source configuration variable name
RSYNC_SOURCE = "RSYNC_SOURCE"   #: RSYNC Source configuration variable name
JSON_FILE = "JSON_FILE"         #: Json file configuration variable name
RSS_SOURCE = "RSS_SOURCE"       #: RSS Source configuration variable name
NAME_FORMAT = "NAME_FORMAT"     #: Name Format configuration variable name
REVERSE_ORDER = "REVERSE_ORDER" #: Reverse order configuration variable name
CRAWL = "CRAWL"                 #: Crawl configuration variable name
DOMAIN_BASE = "DOMAIN_BASE"     #: Domain base configuration variable name
MAX_PAGE_COUNT = "MAX_PAGE_COUNT" #: Max page count configuration variable name
IP_FIELD = "IP_FIELD"
COMPRESSED = "COMPRESSED"

# With no options the format that will be used for output files
DEFAULT_NAME_FORMAT = "%Y%m%d.%H" #: format of output file names


CONFIGURATION_VAR_LIST = set(["FILTER_STRING", "SEARCH_STRING",
                              "OUTPUT_DIRECTORY", "SOURCE_TYPE",
                              "NAME_FORMAT", "REVERSE_ORDER",
                              "CRAWL", "DOMAIN_BASE",
                              "MAX_PAGE_COUNT", IP_FIELD, COMPRESSED]) #: The list of possible configuration variables
FORMAT_STRING_SUB = {"YEAR": "%Y", "MONTH": "%m", "DAY": "%d",
                     "HOUR": "%H", "MINUTE": "%M", "SECOND": "%S"} #: String format varaiables

SOURCE_TYPES = (WEB_SOURCE, RSYNC_SOURCE, RSS_SOURCE, JSON_FILE) #: The collection of avaiblae sources

logger = logging.getLogger("dataleach.datatypes")

class WordSet(object):
    """
    Helper class defining a set of words for filtering and searhing.
    It is a wrapper class for Python Sets.  We wanted these sets to be
    explicitly marked as such.
    """

    def __init__(self, l):
        """
        Declare instance of WordSet.

        @param l: List or Set of strings. 
        """
        if isinstance(l, list):
            self.val = set(l)
        elif isinstance(l, set):
            self.val = l
        else:
            self.val = None

    def __eq__(self, other):
        """
        Equals operation.

        @param other: L{dataleach.WordSet} for comparison.

        @return: True if other equals this instance, False otehrwise.
        """
        if isinstance(other, WordSet):
            return self.val == other.val
        if isinstance(other, set):
            return self.val == other
        return False

    def __ne__(self, other):
        """
        Not equals operation

        @param other: L{dataleach.WordSet} for comparison.

        @return: True if other is not equals this instance, False otherwise.
        """
	return not self.__eq__(other)

    def __in__(self, val):
        """
        In operation

        @param val: String to be checked.

        @return: True if val is in the instance, False otherwise.
        """
	return val in self.val

    def to_set(self):
        """
        @return: The set of String values
        """
        return self.val

    def __iter__(self):
        """
        @return: Iterator of String values
        """
        return self.val.__iter__()

    def intersection(self, other):
        """
        Intersection operation

        @param other: L{dataleach.WordSet} to be checked.

        @return: L{dataleach.WordSet} intersecting other with this instance
        """
        return self.__and__(other)

    def __and__(self, other):
        """
        And operation

        @param other: List or Set to be ANDed.

        @return: L{dataleach.WordSet} ANDing other with this instance
        """
        tmp = self
        if isinstance(other, set) or isinstance(other, list):
            tmp.val = self.val & other
        elif isinstance(other, WordSet):
            tmp.val = self.val & other.val
        return tmp

    def union(self, other):
        """
        Union operation

        @param other: L{dataleach.WordSet} to be ORed.

        @return: L{dataleach.WordSet} unioning the other with this instance.
        """
        return self.__or__(other)

    def __or__(self, other):
        """
        Or operation

        @param other: L{dataleach.WordSet} to be ORed.

        @return: L{dataleach.WordSet} ORing the other with this instance.
        """
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
        """
        Declare and instance of a configuration

        @param kargs: The arg list
        """
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

        if kargs.has_key(MAX_PAGE_COUNT) and \
           kargs[MAX_PAGE_COUNT] is not None:
            val = kargs[MAX_PAGE_COUNT]
            self.max_page_count = int(val)
        else:
            self.max_page_count = 1

        if kargs.has_key(IP_FIELD):
            self.ip_field = kargs[IP_FIELD]
        if kargs.has_key(COMPRESSED):
            self.compressed = kargs[COMPRESSED]

    def get_ip_field(self):
        return self.ip_field

    def is_compressed(self):
        return self.compressed

    def has_domainbase(self):
        """
        @return: True if there is a defined domainbase
        """
        if self.domain_base is None:
            return False
        return True
    def get_domainbase(self):
        """
        @return: The domain base value
        """
        return self.domain_base

    def has_search(self):
        """
        @return: True if there is a search string.
        """
        if self.search_string is None:
            return False
        return True

    def has_crawl(self):
        """
        @return: The value of crawl
        """
        return self.crawl

    def has_filter(self):
        """
        @return: True if there is a fiter string.
        """
        if self.filter_string is None:
            return False
        return True

    def get_reverse(self):
        """
        @return: The value of reverse
        """
        return self.reverse

    def get_output_directory(self):
        """
        @return: The output directory.
        """
        return self.output_directory

    def get_source_type(self):
        """
        @return: The source type
        """
        return self.source_type

    def get_format(self):
        """
        @return: The format string
        """
        return self.name_format

    def get_max_page_count(self):
        """
        @return: The Max page count
        """
        return self.max_page_count

    def __eq__(self, other):
        """
        Equals operation

        @param other: L{dataleach.Configuration} to be used.

        @return: True if other equals this instance, False otherwise
        """
        if isinstance(other, Configuration) and \
              self.source_type == other.source_type and \
              self.output_directory == other.output_directory and \
              self.filter_string == other.filter_string and \
              self.search_string == other.search_string and \
              self.domain_base == other.domain_base and \
              self.crawl == other.crawl and \
              self.max_page_count == other.max_page_count:
            return True
        return False

    def __ne__(self):
        """
        Not equals operation
        """
        return not self.__eq__()


class Format(object):
    """
    Helper class for formating file names.
    """
    def __init__(self, s):
        """
        Declare a Format instance

        @param s: String to be used.
        """
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
        """
        @return: The format string
        """
        return self.fmt_string
