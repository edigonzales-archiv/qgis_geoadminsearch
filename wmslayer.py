 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from PyQt4.QtNetwork import QNetworkReply
from qgis.core import *
from qgis.gui import *

from layernotfoundexception import LayerNotFoundException

import json
import sys
import traceback
import collections

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class WmsLayer(QObject):
    def __init__(self, iface, data):
        QObject.__init__(self)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.MAPSERVER_URL = "https://api3.geo.admin.ch/rest/services/api/MapServer"
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        searchLanguage = self.settings.value("options/language", "de")
        
        layerName = data['layer']
        
        url = self.MAPSERVER_URL + "?searchText="
        url += layerName.strip()
        url += "&lang=" + searchLanguage
        
        print url

        # It does not work:
        # a) when networkAccess is not 'self'
        # b) without lambda
        self.networkAccess = QNetworkAccessManager()         
        self.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), lambda event, data=data: self.receiveLayerMetadata(event, data))
#        networkAccess.finished.connect(self.receiveLayerMetadata)        
        self.networkAccess.get(QNetworkRequest(QUrl(url)))   

    def receiveLayerMetadata(self, networkReply, data):
        print "foo"
        layerName = data['layer']

        bytes = networkReply.readAll()
        response = str(bytes)
        
        try:
            json_response = json.loads(unicode(response), object_pairs_hook=collections.OrderedDict) 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Failed to load json response. ",  None) + str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)      
            return
     
#        try:
        attrs = json_response['layers'][0]['attributes']
        wmsUrlResource = attrs['wmsUrlResource']
        wmsUrl = wmsUrlResource.split('?')[0]
#        except:
#            self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "WMS layer not found. Will try to add it as WMTS layer.",  None), level=QgsMessageBar.WARNING, duration=5)  
#            raise LayerNotFoundException
#            if self.attempts == 0:
#                self.processWMTSLayer(data)
#                self.attempts += 1
#            return

        



    def test(self):
        raise LayerNotFoundException
