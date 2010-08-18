# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright © 2010, RedJack, LLC.
# All rights reserved.
#
# Please see the LICENSE.txt file in this distribution for license
# details.
# ----------------------------------------------------------------------

import re
import sys
import logging

from dataleach.datatypes import WordSet

__all__ = (
    "Scrubber",
    "ScrubList",
    "ScrubReg",
    "ARTICLES",
    "PREPOSITIONS",
    "SECURITY_TITLE",
    "CONJUNCTIONS",
)

logger = logging.getLogger("dataleach.process.scrubber")

WORD = r"[a-zA-Z0-9]+"

ARTICLES = WordSet(["a", "an", "the"])

PREPOSITIONS = WordSet(["aboard","about","above","across","after","against","along",
                    "amid","among","anti","around","as","at","before","behind",
                    "below","beneath","beside","besides","between","beyond","but",
                    "by","concerning","considering","despite","down","during",
                    "except","excepting","excluding","following","for","from","in",
                    "inside","into","like","minus","near","of","off","on","onto",
                    "opposite","outside","over","past","per","plus","regarding",
                    "round","save","since","than","through","to","toward","towards",
                    "under","underneath","unlike","until","up","upon","versus","via",
                    "with","within","without"])

COORDINATING_CONJUNCTIONS = WordSet(["and", "but", "or", "nor", "for", "yet", "so"])

SUBORDINATING_CONJUNCTIONS = WordSet(["after", "although", "as", "because", "before",
                                  "how", "if", "once", "since", "than", "that", 
                                  "though", "till", "until", "when", "where",
                                  "whether", "while"])

CORELATIVE_CONJUNCTIONS = WordSet(["both", "and", "not only", "but also", "either",
                               "or", "neither", "nor","whether"])

CONJUNCTIONS = (COORDINATING_CONJUNCTIONS | SUBORDINATING_CONJUNCTIONS | CORELATIVE_CONJUNCTIONS)

SECURITY_TITLE = WordSet(["bugtraq", "security", "vulnerability", "vulnerabilities",
                      "vuln", "re", "internet", "announce", "bulletin", "news"])

class ScrubList(object):
    """
    Helper class representing a collection of L{Scruber} phrases to remove.
    """
    def __init__(self, l):
        if isinstance(l, WordSet):
            self.removeList = l.to_set()
        else:
            logger.warning("Non-WordSet ignored in the constuction of the ScrubList")
            self.removeList = set()

    def remover(self, input):
        """
        Print the supplied text with all of the  L{Scrubber}s from the list
        removed.

        @param input: The text to be searched.
        """
        if isinstance(input, list):
            s = set(input)
        elif isinstance(input, set):
            s = input
        else:
            Error("SrubList remover cannot handle '%s' objects" % type(input))
            return input
        return s - self.removeList
        
class Scrubber(object):
    """
    Class representing a word or phrase to remove from a selction of
    text.
    """
    def __init__(self, sl):
        self.scrubs = []
        if isinstance(sl, WordSet):
            sl = [sl]
        for scrub in sl:
            if not isinstance(scrub, ScrubList):
                scrub = ScrubList(scrub)
            self.scrubs.append(scrub)
    def scrub(self, input):
        """
        Return the text all scrubbed values removed.

        @param input: The text to be searched.
        """
        if isinstance(input, str):
            input = re.findall(WORD, input.lower())
            input = set(input)
        else:
            input = set([])
        for r in self.scrubs:
            input = r.remover(input)
        return input



class ScrubReg(object):
    """
    The regualar expression class.  This is identical to the
    L{Scrubber} class.
    """
    def __init__(self, reg):
        if isinstance(reg, str):
            self.reg = reg
        else:
            self.reg = ""
        logger.debug("Using '%s' as our regular expression for removal" %
                     self.reg)

    def scrub(self, input):
        input = input.lower()
        if isinstance(input, str):
            removeList = re.findall(self.reg, input)
        else:
            removeList = []
        logger.debug("Removing %d strings", len(removeList))
        for r in removeList:
            if len(r) > 25:
                logger.debug("Removing all occurances of '%50s...'" % r[0:49])
            else:
                logger.debug("Removing all occurances of '%s'" % r)
            debugMsg = "Length change %d -> " % len(input)

            input = input.replace(r, " ")

            debugMsg += "%d" % len(input)
            logger.debug(debugMsg)

        return input


def get_file(file):
    output = ""
    input = open(file, "r")
    for l in input:
        output += l
    return output

if __name__ == "__main__":
    sc = Scrubber([ARTICLES, PREPOSITIONS, CONJUNCTIONS, SECURITY_TITLE])
    data = open(sys.argv[1], "r")
    for line in data:
        out = sc.scrub(line)
        tmp = ""
        for word in out:
            tmp += "%s " % word
        print tmp
