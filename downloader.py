import urllib2

class Urllib2Downloader(object):
    def __init__(self, callback):
        self.callback = callback

    def download(self, url):
        response = urllib2.urlopen(url)
        html = response.read()     
        self.callback(html)


