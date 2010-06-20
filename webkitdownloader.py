#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://blog.motane.lu/2009/07/07/downloading-a-pages-content-with-python-and-webkit/ 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import signal
 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebPage

class WebkitDownloader(QWebPage): 
    def __init__(self, callback):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.callback = callback

    def _callback(self,listener):
        html = str(self.mainFrame().toHtml())
        self.callback(html)

    def download(self, url):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.connect(self, SIGNAL('loadFinished(bool)'), self._callback)
        self.mainFrame().load(QUrl(url))
      	sys.exit(self.app.exec_())
