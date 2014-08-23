# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from qgis.core import *
from qgis.gui import *

import json
import sys
import traceback
import collections

from collections import OrderedDict

from gascapabilities import GasCapabilities

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class GasSuggestCompletion(QLineEdit, QWidget):
    def __init__(self, iface, parent):
        QLineEdit.__init__(self, parent)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        self.settings = QSettings("CatAIS","GeoAdminSearch")
        
        self.origins = {'zipcode': _translate("GeoAdminSearch", "Zipcode",  None), 'gg25': _translate("GeoAdminSearch", "Administrative boundary",  None), 
            'district': _translate("GeoAdminSearch", "District",  None), 'kantone': _translate("GeoAdminSearch", "Canton",  None),
            'sn25': _translate("GeoAdminSearch", "Named location",  None), 'address': _translate("GeoAdminSearch", "Address",  None),
            'parcel': _translate("GeoAdminSearch", "Parcel",  None), 'layer': _translate("GeoAdminSearch", "Layer",  None), 
            'feature': _translate("GeoAdminSearch", "Feature",  None)}
            
        self.geoadminLayers = []
        
        self.popup = QTreeWidget()
        self.popup.setWindowFlags(Qt.Popup);
        self.popup.setFocusPolicy(Qt.NoFocus);
        self.popup.setFocusProxy(parent);
        self.popup.setMouseTracking(True);
        
        self.popup.setColumnCount(4);
        self.popup.hideColumn(3)
        self.popup.setUniformRowHeights(True);
        self.popup.setRootIsDecorated(False);
        self.popup.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.popup.setSelectionBehavior(QTreeWidget.SelectRows)
        self.popup.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.popup.header().hide()
        
        self.popup.installEventFilter(self)
                
        self.connect(self.popup, SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.doneCompletion) # for mouse event
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True);
        self.timer.setInterval(500);
        self.connect(self.timer, SIGNAL("timeout()"), self.autoSuggest);
        self.connect(self, SIGNAL("textEdited(QString)"), self.timer.start)
        
        self.networkManager = QNetworkAccessManager(self)
        self.connect(self.networkManager, SIGNAL("finished(QNetworkReply*)"), self.handleNetworkData)
        
        # connect to layer added signal
#        self.connect(self.canvas, SIGNAL("layersChanged()"), self.updateLayerList)
#        self.connect(QgsMapLayerRegistry.instance(), SIGNAL("layersAdded(QVariant)"), self.updateLayerList)
        QgsMapLayerRegistry.instance().layerWasAdded["QgsMapLayer*"].connect(self.updateAddLayerList)
        QgsMapLayerRegistry.instance().layerRemoved["QString"].connect(self.updateRemoveLayerList)

    def updateAddLayerList(self, mapLayer):
        if mapLayer.type() == QgsMapLayer.RasterLayer:
            if mapLayer.providerType() == "wms":
                layerSource = mapLayer.source()
                params = layerSource.split('&')
                wmsUrl = ""
                layers = []                
                for param in params:
                    if param[0:3] == "url":
                        wmsUrl = param[4:].strip()
                    if param[0:6] == "layers":
                        layers.append(param[7:].strip())

                if wmsUrl.find('swisstopo.admin.ch') > 0 or wmsUrl.find('geo.admin.ch') > 0:
                    for layer in layers:
                        
                        if GasCapabilities.isSearchable(layer):
                            self.geoadminLayers.append(layer)

    def updateRemoveLayerList(self, id):
        self.geoadminLayers = []
        layers = self.iface.mapCanvas().layers()
        for layer in layers:    
            self.updateAddLayerList(layer)
                
    def eventFilter(self, obj, ev):
        try:
            if obj != self.popup:
                return False
    
            if ev.type() ==  QEvent.MouseButtonPress:
                self.setFocus()
                self.popup.hide()
                pass
     
            if ev.type() == QEvent.KeyPress:
                consumed = False
                key = int(ev.key())
                
                if key == Qt.Key_Enter or key == Qt.Key_Return:
                    self.doneCompletion()
                    consumed = True
                elif key == Qt.Key_Escape:
                    self.setFocus()
                    self.popup.hide()
                    consumed = True
                elif key == Qt.Key_Up or key == Qt.Key_Down or key == Qt.Key_Home or key == Qt.Key_End or key == Qt.Key_PageUp or key == Qt.Key_PageDown:
                    pass
                else:
                    self.setFocus()
                    self.event(ev)
                    self.popup.hide()
                    pass
                    
                return consumed
            return False
        except:
            # underlying C++ ..... ???
            return False

    def showCompletion(self, displaytext, layername, origin, data):        
        if len(displaytext) == 0:
            return False
        
        pal = self.palette()
        color  = pal.color(QPalette.Disabled, QPalette.WindowText)
        
        self.popup.setUpdatesEnabled(False)
        self.popup.clear()
                
        for  i in range(len(displaytext)):
            item = QTreeWidgetItem(self.popup)
            item.setText(0, displaytext[i])
            try:
                item.setText(1, layername[i])
                item.setTextColor(1, color)
            except:
                pass
            item.setText(2, origin[i])
            item.setTextAlignment(2, Qt.AlignRight)
            item.setTextColor(2, color)
            item.setData(3, Qt.UserRole, data[i])
            
        self.popup.setCurrentItem(self.popup.topLevelItem(0))
        self.popup.resizeColumnToContents(0)
        self.popup.resizeColumnToContents(1)
        self.popup.adjustSize()
        self.popup.setUpdatesEnabled(True)
        
        h = self.popup.sizeHintForRow(0) * min(7, len(displaytext) + 3)
        self.popup.resize(self.width(), h)
        
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.show()
        self.setFocus()

    def doneCompletion(self):
        self.timer.stop()
        self.popup.hide()
        self.setFocus()
        item = self.popup.currentItem()
        if item:
            self.setText(item.text(0))
            QMetaObject.invokeMethod(self, "returnPressed")
            self.emit(SIGNAL("searchEnterered(QString, QVariant)"),  unicode(item.text(0)), item.data(3, Qt.UserRole))
        
    def autoSuggest(self):
        # search type, language and search url
        searchServer = self.settings.value("services/searchserver", "https://api3.geo.admin.ch/rest/services/api/SearchServer")        
        searchType = self.settings.value("searchtype", "locations")
        searchLanguage = self.settings.value("options/language", "de")

        if searchType == "layers":
            suggestUrl = searchServer + "?lang=" + searchLanguage + "&type=" + searchType + "&searchText="
        elif searchType == "locations":
            suggestUrl = searchServer + "?type=" + searchType + "&searchText="         
        elif searchType == "featuresearch":
            featureLayerNames = ','.join(self.geoadminLayers)            
            suggestUrl = searchServer + "?features=" + featureLayerNames + "&type=" + searchType + "&searchText=" 
    
        # http headers
        headerFields = self.settings.value("options/headerfields")
        headerValues = self.settings.value("options/headervalues")
        headers = []
        if headerFields and headerValues:
            for i in range(len(headerFields)):
                headers.append([headerFields[i], headerValues[i]])
    
        # complete search url 
        # try to get the prefix/origins for location search
        searchString = self.text()
        listSearchString = searchString.split(' ')

        originPrefix = ""
        if listSearchString[0] in self.origins.keys():
            originPrefix += listSearchString[0]
            searchString = ' '.join(listSearchString[1:])
        
        url = str(suggestUrl) + searchString
        if originPrefix <> "":
            url += "&origins=" + originPrefix.strip()

        request = QNetworkRequest(QUrl(url))
        for header in headers:
            request.setRawHeader(header[0], header[1])
        self.networkManager.get(request)
        
    def preventRequest(self):
        self.timer.stop()
        
    def handleNetworkData(self, networkReply):    
        searchType = self.settings.value("searchtype", "locations")
        
        url = networkReply.url()
        if not networkReply.error():
            displaytext = []
            layername = []
            type =  []
            data = []
            
            response = networkReply.readAll()
    
            try:
                my_response = unicode(response)
                json_response = json.loads(my_response, object_pairs_hook=collections.OrderedDict) 
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                QMessageBox.critical(None, "GeoAdminSearch", "Failed to load json response" + str(traceback.format_exc(exc_traceback)))                                    
                return
                       
            for result in json_response['results']:
                attrs = result['attrs']

                if searchType == 'locations':
                    # ignore results without 'geom_st_box2d' key
                    try:
                        bbox = attrs['geom_st_box2d']
                        label = attrs['label']
                        label = label.replace('<b>', '').replace('</b>', '')
                        displaytext.append(label)
                        
                        origin = attrs['origin']
                        origin = self.origins[origin]
                        type.append(origin)
                        
                        data.append(attrs)
                    except:
                        pass
                        
                elif  searchType == 'layers':
                    label = attrs['label']
                    label = label.replace('<b>', '').replace('</b>', '')                    
                    displaytext.append(label)

                    layer = attrs['layer']
                    layername.append(layer)

                    origin = self.origins['layer']
                    type.append(origin)

                    data.append(attrs)
                    
                elif searchType == 'featuresearch':
                    label = attrs['label']
                    label = label.replace('<b>', '').replace('</b>', '')                    
                    displaytext.append(label)

                    layer = attrs['layer']
                    layername.append(layer)

                    origin = self.origins['feature']
                    type.append(origin)

                    data.append(attrs)

            self.showCompletion(displaytext, layername, type, data)
        networkReply.deleteLater()

