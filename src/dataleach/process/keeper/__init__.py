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
    "Keeper",
    "KeeperList",
    "KeeperReg",
)

logger = logging.getLogger("dataleach.process.keeper")

WORD = r"[a-zA-Z0-9\.]+" #: Regex string representing a word.

class KeeperList(object):
    """
    Helper class representing a collection of keeper phrases to keep.
    """
    def __init__(self, l):
        """
        Define instance of a KeeperList

        @param l: A L{dataleach.datatypes.WordSet}.
        """
        if isinstance(l, WordSet):
            self.keeperList = l.to_set()
        else:
            logger.warning("Non-WordSet ignored in the constuction of the KeeperList")
            self.keeperList = set()

    def keep(self, input):
        """
        Print a set of words that match a L{Keeper} from the list
        from the input file.

        @param input: The text to be searched.
        """
        output = set()
        for val in self.keeperList:
            if input.rfind(val) > -1:
                output.add("%s" % val)
        return output

    def __str__(self):
        """
        @return: A string of the KeeperList
        """
        l = ""
        for word in self.keeperList:
            l += "  \"%s\"\n" % (word)
        return l
        
class Keeper(object):
    """
    Class representing a word or phrase to keep from a selction of
    text.
    """
    def __init__(self, sl):
        """
        Define a Kepper.

        @param sl: A L{dataleach.datatypes.WordSet}
        """
        self.scrubs = []
        if isinstance(sl, WordSet):
            sl = [sl]
        for scrub in sl:
            if not isinstance(scrub, KeeperList):
                scrub = KeeperList(scrub)
            self.scrubs.append(scrub)

    def keep(self, input):
        """
        Return a set of values that match the keeper.

        @param input: The text to be searched.
        """
        if isinstance(input, str):
            input = re.findall(WORD, input.lower())
        else:
            input = []
        l = ""
        for word in input:
            l = "%s %s" % (l, word)
        output = set()
        for r in self.scrubs:
            output = output | r.keep(l)
        return output

    def __str__(self):
        """
        @return: A string representing the Keeper
        """
        l = ""
        count = 0
        for r in self.scrubs:
            l += "%d)\n%s\n" % (count, r)
            count += 1
        return l


class KeeperReg(object):
    """
    The regualar expression class.  This is identical to the
    L{Keeper} class.
    """
    def __init__(self, reg):
        """
        Define a KepperReg.

        @param reg: A string representing the regular expression.
        """
        if isinstance(reg, str):
            logger.debug("Using reg ex: %s" % reg)
            self.reg = reg
        else:
            self.reg = ""

    def keep(self, input):
        """
        Return a set of values that match the KeeperReg.

        @param input: The text to be searched.
        """
        if isinstance(input, str) or isinstance(input, unicode):
            logger.debug("Am processing the string")
            keepList = re.findall(self.reg, input.lower())
        else:
            keepList = []
        return keepList

def main():
    k = Keeper(WordSet(["hello all"]))
    output = k.keep("hello.... all //.hello \nall")
    print output
if __name__ == "__main__":
    main()
