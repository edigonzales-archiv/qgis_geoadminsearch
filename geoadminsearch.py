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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from qgis.core import *
from qgis.gui import *

from gassettingsdialog import GasSettingsDialog
from gassuggestcompletion import GasSuggestCompletion
from gaswmslayer import GasWmsLayer
from gaswmtslayer import GasWmtsLayer
from gashtmlpopup import GasHtmlPopup

import json
import sys
import traceback
import collections
import math

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

        # settings dialog
        self.dlg = GasSettingsDialog(self.canvas)
        self.dlg.initGui()
            
        # VertexMarker
        self.marker = None
        
    def initGui(self):
        self.action = QAction(_translate("GeoAdminSearch", "Settings",  None), self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        self.iface.addPluginToMenu(u"&GeoAdmin Search", self.action)
        
        self.toolBar = self.iface.addToolBar(_translate("GeoAdminSearch", "GeoAdmin Search",  None))
        self.toolBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)) 
                
        emptyWidget = QWidget(self.toolBar)
        toolBarLayout = QHBoxLayout(emptyWidget)
        toolBarLayout.setMargin(2)
        
        self.suggest = GasSuggestCompletion(self.iface, emptyWidget)
        self.suggest.setMinimumWidth(600);
        toolBarLayout.addWidget(self.suggest)
        
        self.toolButtonReset = QToolButton(emptyWidget)
        self.toolButtonReset.setIcon(QIcon(':/plugins/geoadminsearch/icons/reset.png'))
        toolBarLayout.addWidget(self.toolButtonReset)
        
        self.comboSearchType = QComboBox(self.toolBar)
        self.comboSearchType.insertItem(0, _translate("GeoAdminSearch", "Locations",  None), "locations")
        self.comboSearchType.addItem(_translate("GeoAdminSearch", "Layers",  None), "layers")
        self.comboSearchType.addItem(_translate("GeoAdminSearch", "Features",  None), "featuresearch")
        
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
        searchType = self.comboSearchType.itemData(self.comboSearchType.currentIndex())
        
        if searchType == "locations":
            self.processLocation(data)
        elif searchType == "layers":
            self.processLayer(data)
        elif searchType == "featuresearch":
            self.processFeatureSearch(data)
        
        self.suggest.preventRequest()                    
        
    def processFeatureSearch(self, data):
        htmlpopup = GasHtmlPopup(self.iface, data)
        htmlpopup.resize(450,300);     
        htmlpopup.show()
        
        self.processLocation(data) # vertex marker
        
    def processLayer(self, data):
        preferredProvider = self.settings.value("options/provider", "WMTS")
        
        if preferredProvider == "WMTS":
            crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()   # hardcoded
            if crs <> "EPSG:21781":
                self.iface.messageBar().pushMessage("Warning",  _translate("GeoAdminSearch", "Only EPSG:21781 tiles are available. ",  None) + str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.WARNING, duration=10)      
                return
                
            myLayer = GasWmtsLayer(self.iface, data)
            QObject.connect(myLayer, SIGNAL("wmtsLayerNotFound(QVariant, QString)"), self.processFallback)
            QObject.connect(myLayer, SIGNAL("layerCreated(QgsMapLayer)"), self.addLayerToCanvas)
    
        elif preferredProvider == "WMS":
            myLayer = GasWmsLayer(self.iface, data)
            QObject.connect(myLayer, SIGNAL("wmsLayerNotFound(QVariant, QString)"), self.processFallback)
            QObject.connect(myLayer, SIGNAL("layerCreated(QgsMapLayer)"), self.addLayerToCanvas)

    def processFallback(self, data, fallbackProvider):
        if fallbackProvider == "WMTS":
            myLayer = GasWmtsLayer(self.iface, data, True)
            QObject.connect(myLayer, SIGNAL("layerCreated(QgsMapLayer)"), self.addLayerToCanvas)
          
        elif fallbackProvider == "WMS":
            myLayer = GasWmsLayer(self.iface, data, True)
            QObject.connect(myLayer, SIGNAL("layerCreated(QgsMapLayer)"), self.addLayerToCanvas)

    def addLayerToCanvas(self, layer):
        if not layer.isValid():                
            self.iface.messageBar().pushMessage("Error",  _translate("GeoAdminSearch", "Layer is not valid.",  None), level=QgsMessageBar.CRITICAL, duration=5)                                                            
            return       
        else:
            root = QgsProject.instance().layerTreeRoot()
            QgsMapLayerRegistry.instance().addMapLayer(layer, False) 
            layerNode = root.addLayer(layer)
            layerNode.setExpanded(False)                     

    def processLocation(self, data):
        try:
            bbox = data['geom_st_box2d']
            coords = bbox[4:-1].split(',')
            
            min = coords[0].split(' ')
            xmin = min[0]
            ymin = min[1]
            
            max = coords[1].split(' ')
            xmax = max[0]        
            ymax = max[1]
            
            # some bbox are really small -> do not make sense (e.g. lfp2)
            # use some tolerance...
            if abs(float(xmax) - float(xmin)) < 1 or abs(float(xmax) - float(xmin)) < 1:
                point = QgsPoint(float(xmin), float(ymin))
                geom = QgsGeometry().fromPoint(point)
            
                # create a marker only for point objects 
                # since we only get the bbox and not the
                # real geometry for polygons
                self.canvas.scene().removeItem(self.marker)  

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

            bbox = geom.boundingBox() 
            self.iface.mapCanvas().setExtent(bbox)
            self.iface.mapCanvas().refresh() 
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print str(traceback.format_exc(exc_traceback))

    def unload(self):
        self.iface.removePluginMenu(u"&GeoAdmin Search", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        self.iface.mainWindow().removeToolBar(self.toolBar)

    def run(self):
            self.dlg.show()
            result = self.dlg.exec_()
            if result == 1:
                pass
