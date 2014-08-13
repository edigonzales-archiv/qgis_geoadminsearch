# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SogisSucheDialog
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
from qgis.core import *
from qgis.gui import *
from ui_sogissuche import Ui_SogisSuche

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class SogisSucheDialog(QDialog, Ui_SogisSuche):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","SogisSuche")

    def initGui(self):
        self.listWidgetSearchTables.clear()
        size = self.settings.beginReadArray("options/searchtables")
        for i in range(size):
            self.settings.setArrayIndex(i)
            item = QListWidgetItem(self.settings.value("type").toString())
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.listWidgetSearchTables.addItem(item)
        self.settings.endArray();
    
    @pyqtSignature("on_btnAddSearchTable_clicked()")    
    def on_btnAddSearchTable_clicked(self):
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.listWidgetSearchTables.addItem(item)
        self.listWidgetSearchTables.setFocus()
        self.listWidgetSearchTables.setCurrentRow(self.listWidgetSearchTables.count() - 1)

    @pyqtSignature("on_btnDeleteSearchTable_clicked()")    
    def on_btnDeleteSearchTable_clicked(self):
        selectedItems = self.listWidgetSearchTables.selectedItems()
        for selectedItem in self.listWidgetSearchTables.selectedItems():
            self.listWidgetSearchTables.takeItem(self.listWidgetSearchTables.row(selectedItem))
    
    
    def accept(self):      
        self.settings.beginWriteArray("options/searchtables");
        for i in range(self.listWidgetSearchTables.count()):
            self.settings.setArrayIndex(i);
            self.settings.setValue("type", self.listWidgetSearchTables.item(i).text());
        self.settings.endArray();        
        
        self.close()
    
