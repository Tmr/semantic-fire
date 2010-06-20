# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, Mats Skillingstad <mats.gls@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
from lxml import etree
from lxml import html
import yaml
from urldata import YamlUrlData
from dataexporter import RdfDataExporter
from dataformatter import DataFormatter
import itertools

class Parser():
    def extractSemantics(self, htm):
        root = html.fromstring(htm)
        print self.urldata
        if self.urldata.has_key('databags'):
            for databag in self.urldata['databags']:
                self.databagExtractor(databag, root)                      
        if self.urldata.has_key('dataitems'):
            for dataitem in self.urldata['dataitems']:
                self.dataitemExtractor(dataitem, root)
        self.rdfex.printTriples()
        

    def dataitemExtractor(self, params, root):
        print params['xpath']
        value = root.xpath(params['xpath'])[0]
        if not isinstance(value, str):
            value = root.xpath(params['xpath'])[0].text_content().strip()
        else:
            value = value.strip()
        self.rdfex.addTriple(self.urldata['url'], params['predicate'], value)


    def databagExtractor(self, params, root):
        table = []
        compositeLeafNode = '' #the row node is a composite string of all nodes in the row, split by a regex
                         
        #print(etree.tostring(root, pretty_print=True))
        #print params['xpath']
        nodeList = root.xpath(params['xpath'])[0]
        if params.has_key('skip_end_rows'):
            num_rows = len(nodeList) - int(params['skip_end_rows'])
        else:
            num_rows = len(nodeList)

        def dataGetter(root, filterfunc):
            if params.has_key('p-list'):
                data = ['' if child.text is None else child.text.strip() 
                        for child in root.iter() if filterfunc]
                data.extend([child.tail.strip() for child in root.iter() 
                             if child.tail is not None and filterfunc])
                return data
            else:
                if params.has_key('subject'):
                    subject = root.xpath(params['subject'])[0]
                else:
                    subject = self.urldata['url']
                for p in params['p-xpaths']:                    
                    o = ''
                    #print root.xpath(p['xpath'])
                    try:
                        value = root.xpath(p['xpath'])
                        if len(value) > 0:
                          o = value[0].text_content().strip()
                    except:
                        value = root.xpath(p['xpath'])
                        if len(value) > 0:
                          o = value[0].strip()
                    self.rdfex.addTriple(subject, p['predicate'], o)
                return None

        def includeHref(data, root):
            data.extend([child.attrib.get('href') for child in root.iter() 
                                                     if child.attrib.has_key('href')])
            return data

        def groupByDatacontainer(params, root):
            if params.has_key('datacontainer_attrib'):                        
              print params['datacontainer_attrib'].split(':')
            else:
              groupedNodes = [child.iter() for child in root.iter() 
                              if child.tag == params['group_by_datacontainer']]
              data = []
              for node in groupedNodes:
                  d = [child.text.strip() for child in node 
                       if child.text is not None and not child.text.isspace()]
                  if len(d) > 1: #grouped by data container
                      data.append(d)
                  elif len(d) == 0: #missing value
                      data.append(None)
                  else: #not grouped by data container
                      data.append(d[0])
            return data

        filterFuncs = {1:lambda x: x == x, 2:lambda x: len(x) == 0}

        #Set default values if not specified in the yaml file
        if not params.has_key('start_row'): 
            params['start_row'] = 0
        if not params.has_key('parser_type'): 
            params['parser_type'] = 1

        #Go through each row and get all the stuff
        for i in xrange(params['start_row'],num_rows): 
            tpl = {}
            myNode = nodeList[i]
            if myNode.tag == params['row_separator']:
                if [n for n in myNode.iter()] is None:
                    continue
                root = myNode             
                if params.has_key('group_by_datacontainer'):
                    data = groupByDatacontainer(params, root)
                else:
                    filterFunc = filterFuncs[params['parser_type']]
                    data = dataGetter(root, filterFunc)
                    if params.has_key('include_href'): includeHref(data, root)

                if params.has_key('include-href'):
                    data.append(myNode.attrib.get('href'))
                
                #print data
                if params.has_key('p-list'):
                    #Create a tuple containing all the data in the databag
                    if len(data) == len(params['p-list']):
                        for i, predicate in enumerate(params['p-list']):
                            if predicate != '':
                                tpl[predicate] = data[i]
                                #tpl[predicate] = self.df.formatData(data[i],'')

                    #print tpl
                    if len(tpl) > 0:
                        table.append(tpl)

        #for t in table: print t
        #Convert the tuples to triples
        if params.has_key('p-list'):
            self.rdfex.export(self.urldata['url'], params, table)


    #Add external data to the tuple and append the tuple to the table
    def addTuple(self, tpl, table, params): 
        #tpl['e'] = params['e']
        table.append(tpl)
        return table

    def usage(self):
        print "Usage: python semanticfire.py myfile.yaml id (if needed)"
        sys.exit()

    def run(self, argv):
        if len(argv) < 1:
          usage()

        ud = YamlUrlData()
        self.urldata = ud.getURLData(argv[0])
        self.df = DataFormatter()
        self.rdfex = RdfDataExporter()

        #Check the require_id parameter
        if self.urldata.has_key('require_id'):
            if self.urldata['require_id']:
                if len(argv) != 2:
                    print "This URL requires an id"
                    sys.exit()
                else:
                    self.urldata['url'] = self.urldata['url']+argv[1]

        #Check the javascript parameter
        if self.urldata.has_key('javascript') and self.urldata['javascript']:
            #from webkitdownloader import WebkitDownloader
            #dl = WebkitDownloader(parser.extractSemantics)
            from jsdownloader import GeckoDownloader
            dl = GeckoDownloader(parser.extractSemantics)
        else:
            from downloader import Urllib2Downloader
            dl = Urllib2Downloader(parser.extractSemantics)

        print self.urldata['url']
        dl.download(self.urldata['url'])

parser = Parser()
parser.run(sys.argv[1:])


