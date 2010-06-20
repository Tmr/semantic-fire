# -*- coding: utf-8 -*-
import re
import calendar
import parsedatetime.parsedatetime as pdt 
import parsedatetime.parsedatetime_consts as pdc

class DataFormatter(object):
    data = {}

    def date(self, value):
        c = pdc.Constants()
        p = pdt.Calendar(c)
        return p.parse(value) 

    def timespan(self, value):
        return value
    
    def string(self, value):
        return value
  
    def integer(self, value):
        return int(''.join(re.match(numregexp, value).group().split(',')))

    def formatData(self, value, fmt):
      try:
          formatter = getattr(self, "%s" % str(fmt))
          return formatter(value)
      except AttributeError:
          print "Invalid data format: %s" % str(fmt)


numregexp = re.compile('[\d,]+')
#titleregexp = re.compile('^[a-zA-Z]*$') #string with only a-Z chars
#titleregexp = re.compile('^\D*$') #string that does not contain numbers
titleregexp = re.compile('^[a-zA-Z\sæøåÆØÅ]+$')
timeregexp = re.compile('(kl)*\s*([0-9]{2}):?([0-9]{2})?\s*$')
dateregexp = re.compile('[0-9]{2}\.[0-9]{2}')
dmyregexp = re.compile('[0-9]{2}\.[0-9]{2}\.[0-9]{2}')
dmregexp = re.compile('[0-9]{2}\.[0-9]{2}')
#timeregexp = re.compile('(2[0-3]|1\d|0\d)[:]?[0-5]\d')

