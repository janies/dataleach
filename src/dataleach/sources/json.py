import ijson
import sys
import os
import logging
import requests
import traceback
from dataleach.webgrabber import WebGrabber


__all__ = (
    "JsonFile",
)

logger = logging.getLogger("json_file")

class JsonFile(object):
    def __init__(self, url, config=None):
        self.config = config
        if config is not None:
            self.tmp_file = self.config.get_tmp_file()
            self.ip_field = self.config.get_ip_field().split(",")
            if self.tmp_file:
                self.ip_field = 'item.' + \
                    '.item.'.join(self.ip_field)

            self.compressed = self.config.is_compressed()
        else:
            self.ip_field = "ip"
        self.url = url

    def _produce_output(self):
        if not self.tmp_file:
            print "working with requests"
            r = requests.get(self.url)
            for rec in r.json():
                self.recurse_record(rec, self.ip_field)
        else:
            print "working with wget"
            os.system("wget %s -O %s > /dev/null" % (self.url, self.tmp_file))
            self.open_file = open(self.tmp_file)
            print "opened the file"
            for prefix, event, value in ijson.parse(self.open_file):
                if self.ip_field == prefix:
                    self.output.write(value + "\n")
            

    def output_file(self, file_name):
        try:
            self.output = open(file_name, "w")
        except:
            traceback.print_exc()
            logger.error("Unable to write to output file '%s'" % file_name)
            sys.exit()
        r = self._produce_output()
        logger.info("About to process")

        self.output.close()
        self._perform_close()

    def _perform_close(self):
        if self.tmp_file:
            self.open_file.close()
            os.system("rm %s" % self.tmp_file)

    def recurse_record(self, rec, fields):
        cur = rec
        place = 0
        for field in fields:
            if isinstance(cur, list):
                for val in cur:
                    self.recurse_record(val, fields[place:])
                return
            else:
                cur = cur[field]
                place += 1
        self.output.write(cur + "\n")
