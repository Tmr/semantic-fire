# -*- coding: utf-8 -*-
from __future__ import with_statement
import time
import sys
import yaml

import pprint

class YamlUrlData(object):
    def getURLData(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f)
        return data



