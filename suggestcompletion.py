# -*- coding: utf-8 -*-

# Import the PyQt and the QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from qgis.core import *
from qgis.gui import *

import json
import sys
import traceback


class SuggestCompletion(QLineEdit, QWidget):
    
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)

        self.settings = QSettings("CatAIS","SogisSuche")
        
#        self.SUGGEST_URL = "http://google.com/complete/search?output=toolbar&q=%1"
#        self.SUGGEST_URL = "http://www.sogis1.so.ch/wsgi/search.wsgi?searchtables=&query=%1"
        self.SUGGEST_URL = "http://www.sogis1.so.ch/wsgi/search.wsgi?query=%1&searchtables=%2"

        self.popup = QTreeWidget()
        self.popup.setWindowFlags(Qt.Popup);
        self.popup.setFocusPolicy(Qt.NoFocus);
        self.popup.setFocusProxy(parent);
        self.popup.setMouseTracking(True);
        
        self.popup.setColumnCount(3);
        self.popup.hideColumn(2)
        self.popup.setUniformRowHeights(True);
        self.popup.setRootIsDecorated(False);
        self.popup.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.popup.setSelectionBehavior(QTreeWidget.SelectRows)
        self.popup.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.popup.header().hide()
        
        self.popup.installEventFilter(self)
                
        # for the MousePressEvent
        self.connect(self.popup, SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.doneCompletion)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True);
        self.timer.setInterval(500);
        self.connect(self.timer, SIGNAL("timeout()"), self.autoSuggest);
        self.connect(self, SIGNAL("textEdited(QString)"), self.timer.start)
        # kann man das ähnlich wie im weblient machen? falls gbnr zu beginn dann nur grundstücke suchen etc? -> timer wieder stoppen und was es noch braucht?!
        
        self.networkManager = QNetworkAccessManager(self)
        self.connect(self.networkManager, SIGNAL("finished(QNetworkReply*)"), self.handleNetworkData)
        
    def eventFilter(self, obj, ev):
        try:
            if obj != self.popup:
                print "obj != self.popup"
                return False
    
            if ev.type() == QEvent.KeyPress:
                consumed = False
                key = int(ev.key())
                print "QEvent.KeyPress"
                
                if key == Qt.Key_Enter or key == Qt.Key_Return:
                    print "Key_Enter/Key_Return"
                    self.doneCompletion()
                    consumed = True
                elif key == Qt.Key_Escape:
                    print "Key_Escape"
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
            print "underlying..."
            return False

    def showCompletion(self, choices, hits, searchTables):        
        if len(choices) == 0:
            return False
        
        pal = self.palette()
        color  = pal.color(QPalette.Disabled, QPalette.WindowText)
        
        self.popup.setUpdatesEnabled(False)
        self.popup.clear()
                
        for  i in range(len(choices)):
            item = QTreeWidgetItem(self.popup)
            item.setText(0, choices[i])
            item.setText(1, hits[i])
            item.setTextAlignment(1, Qt.AlignRight)
            item.setTextColor(1, color)
            item.setText(2, searchTables[i])
            
        self.popup.setCurrentItem(self.popup.topLevelItem(0))
        self.popup.resizeColumnToContents(0)
        self.popup.resizeColumnToContents(1)
        self.popup.adjustSize()
        self.popup.setUpdatesEnabled(True)
        
        h = self.popup.sizeHintForRow(0) * min(7, len(choices) + 3)
#        print "width"
#        print self.width()
        self.popup.resize(self.width(), h)
        
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
#        self.popup.setFocus()
        self.popup.show()
        self.setFocus()

    def doneCompletion(self):
        print "doneCompletion"        
        self.timer.stop()
        self.popup.hide()
        self.setFocus()
        item = self.popup.currentItem()
        if item:
            self.setText(item.text(0))
#            print unicode(self.text())
#            print item.text(1)
#            print item.text(2)
            QMetaObject.invokeMethod(self, "returnPressed")
            self.emit(SIGNAL("searchEnterered(QString, QString)"),  unicode(item.text(0)), item.text(2))
        
    def autoSuggest(self):
        # get additional search tables
        searchTables = ""
        size = self.settings.beginReadArray("options/searchtables")
        for i in range(size):
            self.settings.setArrayIndex(i)
            searchTables += self.settings.value("type").toString() + ","
            searchTables = searchTables[:-1]
        self.settings.endArray();
    
        str = self.text()
        url = QString(self.SUGGEST_URL).arg(str).arg(searchTables)
#        print url
        self.networkManager.get(QNetworkRequest(QUrl(url)))
        
    def preventRequest(self):
        self.timer.stop()
        
    def handleNetworkData(self, networkReply):
        url = networkReply.url()
        if not networkReply.error():
            # TODO: Rename lists
            choices = []
            hits = []
            searchTables = []
            
            response = networkReply.readAll()
                        
            # Wie siehts mit dem sortieren aus? Ist das jetzt Kraut und Rüben oder bleibt das so wie
            # es im String ist?
            # Gemäss Internet ist es wirklich unordered...
            # scheint aber hier momentan geordnet zu sein.
            try:
                my_response = unicode(response)
                json_response = json.loads(my_response) 
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                QMessageBox.critical(None, "SogisSuche", "Failed to load json reponse" + str(traceback.format_exc(exc_traceback)))                                    
                return
            
            for result in json_response['results']:
#                print result['displaytext']
                searchtable = result['searchtable']
                
#                print searchtable
                
                # Die "Titel"-Texte (z.B. Gemeinde, Flurnamen, etc.) haben keinen Searchtable.
                if not searchtable:
                    result_type = result['displaytext'] # z.B. Gemeinde. Bedingt aber dass diese IMMER vor den Resultaten mit dem Typ kommen.
                    continue
                
                displaytext = result['displaytext']
                choices.append(unicode(result['displaytext']))
                hits.append(unicode(result_type))
                searchTables.append(searchtable)
            
            self.showCompletion(choices, hits, searchTables)
        networkReply.deleteLater()
        
    def foo(self):
        print "foobar"
        
