# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SogisSuche
                                 A QGIS plugin
 Sogis Suche Plugin
                              -------------------
        begin                : 2014-03-09
        copyright            : (C) 2014 by Stefan Ziegler / Amt für Geoinformation
        email                : stefan.ziegler@bd.so.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from qgis.core import *
from qgis.gui import *

from settingsdialog import SettingsDialog
from suggestcompletion import SuggestCompletion

import json
import sys
import traceback
import collections

import resources_rc

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class GeoAdminSearch:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        self.searchType = self.settings.value("searchtype", "locations")
        
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/geoadminsearch"

        localePath = ""
        locale = QSettings().value("locale/userLocale")[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/geoadminsearch_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
                
        # URLs
        self.WMTS_URL = "http://api3.geo.admin.ch/rest/services/ech/1.0.0/WMTSCapabilities.xml"
        self.MAPSERVER_URL = "https://api3.geo.admin.ch/rest/services/api/MapServer"
        
        # settings dialog
        self.dlg = SettingsDialog(self.canvas)
        self.dlg.initGui()
        
        # origins mapping dictionary
        self.originsMap = {'zipcode':'locations', 'gg25':'locations', 'district':'locations', 'kantone':'locations', 'sn25':'locations', 'address':'locations', 'parcel':'locations', 'layer':'layers'}
    
        # VertexMarker
        self.marker = None
        
        # number of attempts
        self.attempts = 0

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(_translate("GeoAdminSearch", "Settings",  None), self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
#        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&GeoAdmin Search", self.action)
        
        # Create own toolbar
        self.toolBar = self.iface.addToolBar(_translate("GeoAdminSearch", "GeoAdmin Search",  None))
        self.toolBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)) 
                
        emptyWidget = QWidget(self.toolBar)
        toolBarLayout = QHBoxLayout(emptyWidget)
        toolBarLayout.setMargin(2)
        
        self.suggest = SuggestCompletion(emptyWidget)
        self.suggest.setMinimumWidth(600);
        toolBarLayout.addWidget(self.suggest)
        

        self.toolButtonReset = QToolButton(emptyWidget)
        self.toolButtonReset.setIcon(QIcon(':/plugins/geoadminsearch/icons/reset.png'))
        toolBarLayout.addWidget(self.toolButtonReset)
        
        self.comboSearchType = QComboBox(self.toolBar)
        self.comboSearchType.insertItem(0, _translate("GeoAdminSearch", "Locations",  None), "locations")
        
        self.comboSearchType.addItem(_translate("GeoAdminSearch", "Layers",  None), "layers")
        idx = self.comboSearchType.findData(self.searchType)
        self.comboSearchType.setCurrentIndex(idx)
        QObject.connect(self.comboSearchType, SIGNAL("currentIndexChanged(int)"), self.searchTypeChanged)        
        toolBarLayout.addWidget(self.comboSearchType)
        
        emptyWidget.setLayout(toolBarLayout)
        self.toolBar.addWidget(emptyWidget)

        QObject.connect(self.toolButtonReset, SIGNAL("clicked()"), self.resetSuggest)
        QObject.connect(self.suggest, SIGNAL("searchEnterered(QString, QVariant)"), self.processResult)
        
    def resetSuggest(self):
        self.suggest.clear()
        
        self.iface.mapCanvas().scene().removeItem(self.marker)  
        self.marker = None
        
    def searchTypeChanged(self, idx):
        searchType = self.comboSearchType.itemData(idx)
        self.settings.setValue("searchtype", searchType)
        self.resetSuggest()

    def processResult(self, item, data):                
        self.attempts = 0
        
        searchType = self.comboSearchType.itemData(self.comboSearchType.currentIndex())
        
        if searchType == "locations":
            self.processLocation(item, data)
        elif searchType == "layers":
            self.processLayer(item, data)
        
        self.resetSuggest()
            
        self.suggest.preventRequest()                    
        
    def processLayer(self, item, data):
        print "processLayer"
        preferredProvider = self.settings.value("options/provider", "WMTS")
        
        if preferredProvider == "WMTS":
            
            # hardcoded
            crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if crs <> "EPSG:21781":
                self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "Only EPSG:21781 tiles are available. ",  None) + str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.WARNING, duration=10)      
                return
            print "wmts layer"
            self.processWMTSLayer(data)
        elif preferredProvider == "WMS":
            print "wms layer"
            self.processWMSLayer(data)

    def processWMSLayer(self, data):    
        searchLanguage = self.settings.value("options/language", "de")
        
        layerName = data['layer']
        
        url = self.MAPSERVER_URL + "?searchText="
        url += layerName.strip()
        url += "&lang=" + searchLanguage

        self.networkAccess = QNetworkAccessManager()         
        QObject.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), lambda event, layerData=data: self.receiveLayerMetadata(event, layerData))
        self.networkAccess.get(QNetworkRequest(QUrl(url)))   

    def receiveLayerMetadata(self, networkReply, data):
        layerName = data['layer']

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
            self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "WMS layer not found. Will try to add it as WMTS layer.",  None), level=QgsMessageBar.WARNING, duration=5)      
            if self.attempts == 0:
                self.processWMTSLayer(data)
                self.attempts += 1
            return

        # this is unstable (sometimes)?! QGIS? WMS-Server?
        auth = False
        userName = ""
        password = ""
        if wmsUrl.find('httpauth') > 0:
            auth = True
            userName = self.settings.value("options/username", "")
            password = self.settings.value("options/password", "")
            
            if userName == "" or password == "":
                self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "WMS server needs authentification. Please set username and password.",  None), level=QgsMessageBar.CRITICAL, duration=5)      
                return
            
        layer = json_response['layers'][0]['layerBodId']
        layerName = json_response['layers'][0]['fullName']
 
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.addWMSLayer(layer, layerName, wmsUrl, userName, password, auth)
        except:
            QApplication.restoreOverrideCursor()            
        QApplication.restoreOverrideCursor()      

    def addWMSLayer(self, layer, layerName, wmsUrl, userName, password, auth):

        # what happens with a crs which is unknown by the server?
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()

        uri = "IgnoreGetMapUrl=1&crs="+str(crs)+"&layers="+layer+"&styles=&format=image/png&url="+wmsUrl
        
        if auth == True:
            uri += "&username="+userName+"&password="+password
    
        wmsLayer = QgsRasterLayer (uri, layerName, "wms", False) 
        
        if not wmsLayer.isValid():                
            self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Layer is not valid.",  None), level=QgsMessageBar.CRITICAL, duration=5)                                                            
            return       
        else:
            root = QgsProject.instance().layerTreeRoot()
            QgsMapLayerRegistry.instance().addMapLayer(wmsLayer, False) 
            wmsLayerNode = root.addLayer(wmsLayer)
            wmsLayerNode.setExpanded(False)                     

    def processWMTSLayer(self, data):        
        url = self.WMTS_URL

        self.networkAccess = QNetworkAccessManager()         
        QObject.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), lambda event, layerData=data: self.receiveWMTSCapabilities(event, layerData))
        self.networkAccess.get(QNetworkRequest(QUrl(url)))   

    # Problem: Identifier muss vor allem anderen kommen... 
    # Geht das auch besser?
    # Alles in Dictionary und dann auslesen, zB.
    def receiveWMTSCapabilities(self, networkReply, data):
        layerName = data['layer']

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
                                    if my_identifier == layerName:
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
       
        if not identifier or not format or not time or not tileMatrixSet: 
            self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "WMTS layer not found. Will try to add it as WMS layer.",  None), level=QgsMessageBar.WARNING, duration=5)      
            
            if self.attempts == 0:
                self.processWMSLayer(data)
                self.attempts += 1
            return
                
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.addWMTSLayer(identifier, format, time, tileMatrixSet, data)
        except:
            QApplication.restoreOverrideCursor()            
        QApplication.restoreOverrideCursor()      

    # EPSG:21781 only!
    def addWMTSLayer(self, identifier, format, time, tileMatrixSet, data):
        headerFields = self.settings.value("options/headerfields")
        headerValues = self.settings.value("options/headervalues")
        referer =""
        if headerFields and headerValues:
            for i in range(len(headerFields)):
                if headerFields[i] == "Referer":
                    referer = headerValues[i]
                    
        layerName = data['label'].replace('<b>', '').replace('</b>', '')
        
        uri = "crs=EPSG:21781&dpiMode=7&featureCount=10&format="+format+"&layers="+identifier+"&referer="+referer+"&styles=&tileDimensions=Time%3D"+time+"&tileMatrixSet="+tileMatrixSet+"&url=" + self.WMTS_URL
        wmtsLayer = QgsRasterLayer (uri, layerName, "wms", False)      

        if not wmtsLayer.isValid():                
            self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "WMTS layer is not valid.",  None), level=QgsMessageBar.CRITICAL, duration=5)                                                            
            return       
        else:
                root = QgsProject.instance().layerTreeRoot()
                QgsMapLayerRegistry.instance().addMapLayer(wmtsLayer, False) 
                wmsLayerNode = root.addLayer(wmtsLayer)
                wmsLayerNode.setExpanded(False)                     
        
    def processLocation(self, item, data):
        bbox = data['geom_st_box2d']
        coords = bbox[4:-1].split(',')
        
        min = coords[0].split(' ')
        xmin = min[0]
        ymin = min[1]
        
        max = coords[1].split(' ')
        xmax = max[0]        
        ymax = max[1]
        
        if xmin == xmax or ymin == ymax:
            point = QgsPoint(float(xmin), float(ymin))
            geom = QgsGeometry().fromPoint(point)
            
            # create a marker only for point objects 
            # since we only get the bbox and not the
            # real geometry for polygons
            self.canvas.scene().removeItem(self.marker)  
            self.marker = None

            self.marker = QgsVertexMarker(self.iface.mapCanvas())
            self.marker.setIconType(3)
            self.marker.setColor(QColor(255,0,0))
            self.marker.setIconSize(20)
            self.marker.setPenWidth (3)
            self.marker.setCenter(geom.asPoint())
            
        else:
            rect = QgsRectangle(float(xmin), float(ymin), float(xmax), float(ymax))
            rect.scale(1.2)
            geom = QgsGeometry().fromRect(rect)

        # pan/zoom to result
        bbox = geom.boundingBox() 
        
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh() 
        
        # stop timer
        self.suggest.preventRequest()
        
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Sogis Suche", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        # Remove own toolbar
        self.iface.mainWindow().removeToolBar(self.toolBar)

    def run(self):
            self.dlg.show()
            result = self.dlg.exec_()
            if result == 1:
                pass
