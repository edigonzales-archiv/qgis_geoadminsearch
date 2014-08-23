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

class GasWmtsLayer(QObject):
    def __init__(self, iface, data, fallback = False):
        QObject.__init__(self)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.fallback = fallback
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        
        self.wmtsCapabilitities = self.settings.value("services/wmtscapabilities", "http://api3.geo.admin.ch/rest/services/api/1.0.0/WMTSCapabilities.xml")
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        searchLanguage = self.settings.value("options/language", "de")
        self.userName = self.settings.value("options/username", "")
        self.password = self.settings.value("options/password", "")

        self.layerName = data['layer']
        
        url = self.wmtsCapabilitities

        # It does not work:
        # a) when networkAccess is not 'self'
        # b) without lambda
        self.networkAccess = QNetworkAccessManager()         
        self.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), lambda event, data=data: self.receiveWmtsCapabilities(event, data))
        self.networkAccess.get(QNetworkRequest(QUrl(url)))   
        
    def receiveWmtsCapabilities(self, networkReply, data):
        if not networkReply.error():
            response = networkReply.readAll()
            xml = QXmlStreamReader(response)
            while not xml.atEnd():
                token = xml.readNext()
                if token == QXmlStreamReader.StartDocument:
                    continue
                
                if token == QXmlStreamReader.StartElement:
                    if xml.name() == "Layer":
                        
                        identifier = None
                        format = None
                        time = None
                        tileMatrixSet = None

                        xml.readNext()
                        
                        while not (xml.tokenType() == QXmlStreamReader.EndElement and xml.name() == "Layer"):
                            if xml.tokenType() == QXmlStreamReader.StartElement:
                                
                                if xml.name() == "Identifier" and identifier == None:
                                    my_identifier =  xml.readElementText().strip()
                                    if my_identifier == self.layerName:
                                        identifier = my_identifier
                                
                                if xml.name() == "Format" and format == None:
                                     my_format = xml.readElementText().strip()
                                    
                                if xml.name() == "Dimension" and time == None:
                                    while not (xml.tokenType() == QXmlStreamReader.EndElement and xml.name() == "Dimension"):
                                        if xml.tokenType() == QXmlStreamReader.StartElement:
                                            if xml.name() == "Default":
                                                my_time = xml.readElementText().strip()
                                        xml.readNext()
                                     
                                if xml.name() == "TileMatrixSetLink" and tileMatrixSet == None:
                                    while not (xml.tokenType() == QXmlStreamReader.EndElement and xml.name() == "TileMatrixSetLink"):
                                        if xml.tokenType() == QXmlStreamReader.StartElement:
                                            if xml.name() == "TileMatrixSet":
                                                my_tileMatrixSet = xml.readElementText().strip()
                                        xml.readNext()
                                     
                            xml.readNext()
                        
                        if identifier <> None:
                            format = my_format
                            time = my_time
                            tileMatrixSet = my_tileMatrixSet
                            break

        print "end of WMTSCapabilities.xml"
        print identifier

        if not identifier or not format or not time or not tileMatrixSet: 
            if not self.fallback:
                self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "WMTS layer not found. Will try to add it as WMS layer.",  None), level=QgsMessageBar.WARNING, duration=5)                      
                self.emit(SIGNAL("wmtsLayerNotFound(QVariant, QString)"), data, "WMS")
                return
            else:
                self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Not able to add WMS or WMTS layer.",  None), level=QgsMessageBar.CRITICAL, duration=5)                                      
                return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            headerFields = self.settings.value("options/headerfields")
            headerValues = self.settings.value("options/headervalues")
            referer =""
            if headerFields and headerValues:
                for i in range(len(headerFields)):
                    if headerFields[i] == "Referer":
                        referer = headerValues[i]
                        
            layerName = data['label'].replace('<b>', '').replace('</b>', '')
            
            if referer == "":
                uri = "crs=EPSG:21781&dpiMode=7&featureCount=10&format="+format+"&layers="+identifier+"&styles=&tileDimensions=Time%3D"+time+"&tileMatrixSet="+tileMatrixSet+"&url=" + self.wmtsCapabilitities
            else:
                uri = "crs=EPSG:21781&dpiMode=7&featureCount=10&format="+format+"&layers="+identifier+"&referer="+referer+"&styles=&tileDimensions=Time%3D"+time+"&tileMatrixSet="+tileMatrixSet+"&url=" + self.wmtsCapabilitities
            wmtsLayer = QgsRasterLayer (uri, layerName, "wms", False)      
            self.emit(SIGNAL("layerCreated(QgsMapLayer)"), wmtsLayer)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print str(traceback.format_exc(exc_traceback))
            
            QApplication.restoreOverrideCursor()            
        QApplication.restoreOverrideCursor()      
