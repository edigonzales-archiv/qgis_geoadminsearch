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
                
        self.dlg = SettingsDialog(self.canvas)
        self.dlg.initGui()
        
#        # Create Rubberband
#        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), True)
#        self.rubberBand.setColor(QColor(255, 0, 0))
#        self.rubberBand.setWidth(4)
#        
#        # VertexMarker
#        self.marker = None

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
        
    def searchTypeChanged(self, idx):
        searchType = self.comboSearchType.itemData(idx)
        self.settings.setValue("searchtype", searchType)

    def processResult(self, item, data):
        print data
        # wie unterscheidet man am einfachsten was es ist? layer, feature, location? dict bei locations versch. keys zum gleichen value, z.B. address -> location, parcel -> location etc.
        # -> processLocation
        # -> process Layer...
#        GEOM_URL = "http://www.sogis1.so.ch/wsgi/getSearchGeom.wsgi?searchtable=%1&displaytext=%2"
#        url = QString(GEOM_URL).arg(searchTable).arg(item)
##        print unicode(url)
#    
#        self.networkAccess = QNetworkAccessManager()         
#        QObject.connect(self.networkAccess, SIGNAL("finished(QNetworkReply*)"), self.receiveGeometry)
#        self.networkAccess.get(QNetworkRequest(QUrl(url))) 
       
    def receiveGeometry(self, networkReply): 
        bytes = networkReply.readAll()
        wkt = QString(bytes)
        print wkt
        
        geom = QgsGeometry.fromWkt(wkt)
        
        # Rubberband or Vertexmarker
        wkbType = geom.wkbType()
        if wkbType == 1 or wkbType == 5 or wkbType == 8 or wkbType == 11:
            self.rubberBand.reset(True) # reset rubberband
            
            # Geht das nicht eleganter? Schon bei den CadTools ein Geknorze...
            self.iface.mapCanvas().scene().removeItem(self.marker)  
            self.marker = None

            self.marker = QgsVertexMarker(self.iface.mapCanvas())
            self.marker.setIconType(3)
            self.marker.setColor(QColor(255,0,0))
            self.marker.setIconSize(20)
            self.marker.setPenWidth (3)
            
            if wkbType == 1 or wkbType == 8: # (Multi)Point(25D)
                self.marker.setCenter(geom.asPoint())
            else:
                self.marker.setCenter(geom.asMultiPoint())
                
        else:
            self.iface.mapCanvas().scene().removeItem(self.marker)  
            self.marker = None
            
            if wkbType == 3 or wkbType == 6 or wkbType == 10 or wkbType == 13:
                isPolygon = True # (Multi)Polygon(25D)
            else:
                isPolygon = False
            
            # Eventuell in Settings wählbar, ob man immer neues will?
            self.rubberBand.reset(isPolygon)
            self.rubberBand.addGeometry(geom, None)
        
        # Zoom to extent
        bbox = geom.boundingBox() # Wie zoomt QGIS zum Punkt?
        bbox.scale(1.2)
        
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh() 
        
        # Stop timer
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
