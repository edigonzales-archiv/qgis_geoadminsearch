 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from PyQt4.QtNetwork import QNetworkReply
from qgis.core import *
from qgis.gui import *

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

class GasWmsLayer(QObject):
    def __init__(self, iface, data, fallback = False):
        QObject.__init__(self)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.fallback = fallback
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")

        mapServer = self.settings.value("services/mapserver", "https://api3.geo.admin.ch/rest/services/api/MapServer")
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        searchLanguage = self.settings.value("options/language", "de")
        self.userName = self.settings.value("options/username", "")
        self.password = self.settings.value("options/password", "")

        self.layerName = data['layer']
        
        url = mapServer + "?searchText="
        url += self.layerName.strip()
        url += "&lang=" + searchLanguage

        # It does not work:
        # a) when networkAccess is not 'self'
        # b) without lambda
        self.networkAccess = QNetworkAccessManager()         
        self.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), lambda event, data=data: self.receiveLayerMetadata(event, data))
        self.networkAccess.get(QNetworkRequest(QUrl(url)))   

    def receiveLayerMetadata(self, networkReply, data):
        bytes = networkReply.readAll()
        response = str(bytes)
                
        try:
            json_response = json.loads(unicode(response), object_pairs_hook=collections.OrderedDict) 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Failed to load json response. ",  None) + str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)      
            return
            
        try:
            attrs = json_response['layers'][0]['attributes']
            wmsUrlResource = attrs['wmsUrlResource']
            wmsUrl = wmsUrlResource.split('?')[0]
        except:
            if not self.fallback:
                self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "WMS layer not found. Will try to add it as WMTS layer.",  None), level=QgsMessageBar.WARNING, duration=5)                      
                self.emit(SIGNAL("wmsLayerNotFound(QVariant, QString)"), data, "WMTS")
                return
            else:
                self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Not able to add WMS or WMTS layer.",  None), level=QgsMessageBar.CRITICAL, duration=5)                                      
                return
            
        # this is unstable (sometimes)?! QGIS? WMS-Server?
        auth = False
        if wmsUrl.find('httpauth') > 0:
            auth = True
            if self.userName == "" or self.password == "":
                self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "WMS server needs authentification. Please set username and password.",  None), level=QgsMessageBar.CRITICAL, duration=5)      
                return
            
        layer = json_response['layers'][0]['layerBodId']
        fullLayerName = json_response['layers'][0]['fullName']
 
 
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:            
            crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            uri = "IgnoreGetMapUrl=1&crs="+str(crs)+"&layers="+layer+"&styles=&format=image/png&url="+wmsUrl
            
            if auth:
                uri += "&username="+self.userName+"&password="+self.password

            wmsLayer = QgsRasterLayer(uri, fullLayerName, "wms", False) 
            self.emit(SIGNAL("layerCreated(QgsMapLayer)"), wmsLayer)
            
        except:
            QApplication.restoreOverrideCursor()            
        QApplication.restoreOverrideCursor()      
