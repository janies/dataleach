import json
import sys
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
            self.ip_field = self.config.get_ip_field().split(",")
            self.compressed = self.config.is_compressed()
        else:
            self.ip_field = "ip"
        self.url = url

    def output_file(self, file_name):
        try:
            self.output = open(file_name, "w")
        except:
            traceback.print_exc()
            logger.error("Unable to write to output file '%s'" % file_name)
            sys.exit()
        r = requests.get(self.url)
        r = r.json()
        for rec in r:
            self.recurse_record(rec, self.ip_field)
        self.output.close()

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
