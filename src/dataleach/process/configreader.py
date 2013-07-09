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
import os
from ConfigParser import *

from dataleach.datatypes import Configuration
from dataleach.datatypes import *

__all__ = (
    "ConfigReader",
    "ConfigError",
    "SystemConfig",
    "IndividualConfig",
    "VALID_SYSTEM_SECTIONS",
    "VALID_INDIVIDUAL_SECTIONS",
)

logger = logging.getLogger("dataleach.process.configreader")


VALID_SYSTEM_SECTIONS = {
    "INPUT" : ["dir", "extension"],
    "OUTPUT" :["dir","format"],
} #: The collection of valid system configuration options

VALID_INDIVIDUAL_SECTIONS = {
    "DETAILS" : ["name", "type", "address"],
    "PROCESS" : ["filter", "search", "reverse_order", "crawl",
                 "domain_base", "max_page_count", "ip_field",
                 "compression"],
    "IO" : ["output_dir"],
} #: The collection of valid source configuration options


class ConfigError(Exception):
    """
    Error class for configurations.
    """
    def __init__(self, error):
        """
        Define a ConfigError
        """
        self.error = error

    def __str__(self):
        """
        @return: String object
        """
        return "Configuration Error: %s" % \
            self.error

class ConfigReader(object):
    """
    Helper class for representing and parsing configuration files.
    """

    def __init__(self, configFile):
        """
        Declare a ConfigReader

        @param configFile: The name of the file containing the configuration
        """
        self.configParser = SafeConfigParser()
        self.configFile = configFile
        if configFile not in self.configParser.read(self.configFile):
            raise ConfigError, \
                "Could not open '%s'" % self.configFile

    def valid(self, listing):
        """
        Verify that a dictionary only contains valid keys.

        @param listing: The collection of valid listings.
        """
        sections = set(self.configParser.sections())
        listingKeys = set(listing.keys())
        if len(sections - listingKeys) != 0:
            logger.error("%s is not valid (%d invalid)" % (sections,
                                   len(sections -listingKeys)))
            return False
        for section in sections:
            options = set(self.configParser.options(section))
            listOptions = set(listing[section])
            if len(options - listOptions) != 0:
                print "%s -> %s is not valid" % (section, options)
                return False
        return True
            

    def get(self, section, option):
        """
        Return the value corresponding section and option in the
        configuration or none if one does not exist.

        @param section: The section of the configuration.
        @param option: The option of the configuration. 
        """
        if self.configParser.has_section(section):
            if self.configParser.has_option(section, option):
                return self.configParser.get(section,option)
        return None

    def set(self, section, option, value):
        """
        set a configraution value for a specific section and option.

        @param section: The section of the configuration.
        @param option: The option of the configuration.
        @param value: The value to which we set the corresponding
        section and option pair.
        """
        self.configParser.set(section, option, value)

    def get_configFile(self):
        """
        @return: The configuration file currently loaded.
        """
        return self.configFile

    def get_config_list(self):
        """
        @return: A list of configuration options represented in the
        configuration file.
        """
        return self.configList
        

class SystemConfig(object):
    """
    Helper class representing and parsing a system configuration.
    A system configuration is the actual application configuration.
    """
    def __init__(self, configFile):
        """
        Declare a SystemConfig

        @param configFile: The name of the file containing the configuration
        """
        self.config_reader = ConfigReader(configFile)
        if not self.config_reader.valid(VALID_SYSTEM_SECTIONS):
            raise ConfigError, \
                "%s is not a valid System configuration" % configFile
        self.sources = []
        self.process_options()
        self.develop_source_list()

    def process_options(self):
        """
        Process the options read in via the L{ConfigReader}
        """
        self.file_extension = self.config_reader.get("INPUT", "NAME")
        if self.file_extension is None:
            self.file_extension = "conf"
        if self.file_extension[0] == ".":
            self.file_extension = self.file_extension[1:]

        self.in_dir = self.config_reader.get("INPUT", "DIR")
        if self.in_dir is None:
            self.in_dir = os.path.abspath(os.curdir)
        else:
            self.in_dir = os.path.abspath(self.in_dir)
            
        self.out_dir = self.config_reader.get("OUTPUT", "DIR")
        if self.out_dir is None:
            self.out_dir = os.path.abspath(os.curdir)
        else:
            self.out_dir = os.path.abspath(self.out_dir)
        #self.out_format = Format(self.config_reader.get("OUTPUT",
        #                                                "FORMAT"))
        self.out_format = self.config_reader.get("OUTPUT", "FORMAT")


    def develop_source_list(self):
        """
        Get a list of configuration files by walking through the
        directory.
        """
        for root, dirs, files in os.walk(self.in_dir):
            for file in files:
                #print "%s/%s" % (root,file)
                part = file.split(".")
                if len(part) > 0 and \
                        part[-1] == self.file_extension:
                    self.sources.append(IndividualConfig("%s/%s"%(root, file),
                                                         self.out_format))
                    
    def get_in_dir(self):
        """
        Return the input directroy used to obtain the source
        configuration files.
        """
        return self.in_dir

    def set_in_dir(self, file):
        """
        Set the input directory used to obtain the source
        configuration files.

        @param file: The directory we will use for input.
        """
        self.in_dir = file

    def get_out_dir(self):
        """
        @return: The output directory we will use by default.
        """
        return self.out_dir

    def set_out_dir(self, file):
        """
        Set the output directory will use by default.

        @param file: The directory we will use for default output.
        """
        self.out_dir = file

    def get_sources(self):
        """
        @return: The list of sources
        """
        return self.sources

    def get_file_extension(self):
        """
        @return: The file extension we identify as being source
        configuration files.
        """
        return self.file_extension

    def set_file_extension(self, phrase):
        """
        Set the extention we identify as being source
        configuraiton files.

        @param phrase: The extension to use set.
        """
        self.file_extension = phrase

class IndividualConfig(object):
    """
    Helper class representing and parsing srouce configurations.
    """
    def __init__(self, configFile, format=DEFAULT_NAME_FORMAT):
        """
        Declare an IndividualConfig

        @param configFile: the name of the configuration file
        @param format: The name format sting to use
        """
        self.config_name = configFile
        self.config_reader = ConfigReader(configFile)
        self.out_format = format
        if not self.config_reader.valid(VALID_INDIVIDUAL_SECTIONS):
            raise ConfigError, \
                "%s is not a valid Individual Configuration" % configFile
        self.process_options()

    def process_options(self):
        """
        Parse the source configuration file.
        """
        #"DETAILS" : ["name", "type", "address"],
        #"Process" : ["filter", "search"],
        #"IO" : ["output_dir"],
        self.name = self.config_reader.get("DETAILS", "NAME")
        if self.name is None:
            raise ConfigError, \
                "%s does not have a name value" % self.config_name

        self.type = self.config_reader.get("DETAILS", "TYPE")
        if self.type is None:
            raise ConfigError, \
                "%s does not have a type value" % self.type
        if self.type not in (WEB_SOURCE, RSYNC_SOURCE, RSS_SOURCE, JSON_FILE):
            raise ConfigError, \
                "%s is not a supported type" % self.type

        self.address = self.config_reader.get("DETAILS", "ADDRESS")
        if self.address is None:
            raise ConfigError, \
                "%s does not have a address" % self.address

        self.filter = self.config_reader.get("PROCESS", "filter")
        self.search = self.config_reader.get("PROCESS", "search")
        self.order = self.config_reader.get("PROCESS", "reverse_order")
        self.crawl = self.config_reader.get("PROCESS", "crawl")
        self.domainBase = self.config_reader.get("PROCESS", "domain_base")
        self.maxPageCount = self.config_reader.get("PROCESS", "max_page_count")
        self.ip_field = self.config_reader.get("PROCESS", "ip_field")
        self.compressed = self.config_reader.get("PROCESS", "compressed")

        self.output_dir = self.config_reader.get("IO","OUTPUT_DIR")
        if self.output_dir is None:
            raise ConfigError, \
                "%s does not have a output directory" % self.output_dir
        else:
            self.output_dir = os.path.abspath(self.output_dir)
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

    def get_config_name(self):
        """
        @return: The name of the configuration file.
        """
        return self.config_name

    def get_configuration(self):
        """
        @return: A L{Configuration} out of the file representations. 
        """
        return Configuration(FILTER_STRING=self.filter,
                             SEARCH_STRING=self.search,
                             OUTPUT_DIRECTORY=self.output_dir,
                             SOURCE_TYPE=self.type,
                             NAME_FORMAT=self.out_format,
                             REVERSE_ORDER=self.order,
                             CRAWL=self.crawl,
                             DOMAIN_BASE=self.domainBase,
                             MAX_PAGE_COUNT=self.maxPageCount,
                             IP_FIELD=self.ip_field,
                             COMPRESSED=self.compressed)
        
