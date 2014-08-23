 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from qgis.core import *
from qgis.gui import *

import json
import sys
import traceback
import collections

from ui_htmlpopup import Ui_HtmlPopup

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class GasHtmlPopup(QDialog, Ui_HtmlPopup):
    def __init__(self, iface, data):
        QDialog.__init__(self, iface.mapCanvas())
        self.setupUi(self)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        lang = self.settings.value("options/language", "de")
        mapServer = self.settings.value("services/mapserver", "https://api3.geo.admin.ch/rest/services/api/MapServer")

        layerBodId = data['layer']
        featureId = data['featureId']
        self.setWindowTitle(str(featureId))
        
        url = mapServer +"/" + layerBodId + "/" + featureId + "/htmlPopup"
        url += "?lang=" + lang
        print url
    
        self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.load(QUrl(url))      
        
        settings = self.webView.settings()        
        css = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/geoadminsearch/htmlpopup.css'))
        settings.setUserStyleSheetUrl(QUrl.fromLocalFile(css))
        
        self.connect(self.webView, SIGNAL("linkClicked(QUrl)"), self.linkClickedSlot)
        
    def linkClickedSlot(self, url):
        QDesktopServices.openUrl(url)


 
        
