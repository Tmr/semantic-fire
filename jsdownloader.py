#http://blog.tomeuvizoso.net/2009/01/embedding-mozilla.html
import hulahop
import os
hulahop.startup(os.path.expanduser('~/.hulahop_profile'))
from hulahop.webview import WebView
import xpcom
import gobject
from xpcom.components import interfaces
import gtk

class ProgressListener(gobject.GObject):
    _com_interfaces_ = interfaces.nsIWebProgressListener
    __gsignals__ = {'finished':(gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,([]))}

    def onStateChange(self, webProgress, request, stateFlags, status):
        if not (stateFlags & interfaces.nsIWebProgressListener.STATE_IS_NETWORK and \
                stateFlags & interfaces.nsIWebProgressListener.STATE_STOP):
            return
        self.emit('finished')

class GeckoDownloader(object):
    def __init__(self, callback):
        self.callback = callback
        self.w = gtk.Window()
        self.w.show()
        self.w.hide()

    def _callback(self,listener):
        html = self.v.dom_window.document.documentElement.innerHTML
        self.callback(html)
        gtk.main_quit()

    def download(self, url):
        self.v = WebView()
        self.w.add(self.v)
        self.v.show()
        self.v.load_uri(url)

        listener = ProgressListener()
        wrapped_listener = xpcom.server.WrapObject(listener, interfaces.nsIWebProgressListener)
        self.v.web_progress.addProgressListener(wrapped_listener, interfaces.nsIWebProgress.NOTIFY_STATE_ALL)

        listener.connect('finished', self._callback)

        gtk.main()
