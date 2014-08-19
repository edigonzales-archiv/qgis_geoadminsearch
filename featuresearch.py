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

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class FeatureSearch(QObject):
    def __init__(self, iface, data):
        QObject.__init__(self)
        
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.HTMLPOPUP_URL = "https://api3.geo.admin.ch/rest/services/api/MapServer/"
                
        layerBodId = data['layer']
        featureId = data['featureId']
        
        url = self.HTMLPOPUP_URL + layerBodId + "/" + featureId + "/htmlPopup"
        
        print url
        
        # FeatureSearch -> HtmlPopupDialog mit webView. Analog veriso checkliste.
        
        
