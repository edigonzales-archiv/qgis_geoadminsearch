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
from ui_settings import Ui_Settings

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class SettingsDialog(QDialog, Ui_Settings):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.settings = QSettings("CatAIS","GeoAdminSearch")
        
    def initGui(self):
        self.comboBoxLanguage.insertItem(self.comboBoxLanguage.count(),  _translate("GeoAdminSearch", "German", None), "de")
        self.comboBoxLanguage.insertItem(self.comboBoxLanguage.count(),  _translate("GeoAdminSearch", "Français", None), "fr")
        self.comboBoxLanguage.insertItem(self.comboBoxLanguage.count(),  _translate("GeoAdminSearch", "Italian", None), "it")
        self.comboBoxLanguage.insertItem(self.comboBoxLanguage.count(),  _translate("GeoAdminSearch", "Rhaeto-Romanic ", None), "rm")
        self.comboBoxLanguage.insertItem(self.comboBoxLanguage.count(),  _translate("GeoAdminSearch", "English", None), "en")
        
        lang = self.settings.value("options/language", "de")
        idx = self.comboBoxLanguage.findData(lang)
        self.comboBoxLanguage.setCurrentIndex(idx)

        QWidget.setTabOrder(self.lineEditUserName, self.lineEditPassword)
                
        userName = self.settings.value("options/username")
        password = self.settings.value("options/password")
        self.lineEditUserName.setText(userName) 
        self.lineEditPassword.setText(password) 

        self.treeWidgetHeaders.clear()
        headerFields = self.settings.value("options/headerfields")
        headerValues = self.settings.value("options/headervalues")
        
        if headerFields and headerValues:
            for i in range(len(headerFields)):
                header = [headerFields[i], headerValues[i]]
                item = QTreeWidgetItem(header)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.treeWidgetHeaders.addTopLevelItem(item)

    @pyqtSignature("on_btnAddHeader_clicked()")    
    def on_btnAddHeader_clicked(self):
        item = QTreeWidgetItem(self.treeWidgetHeaders)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.treeWidgetHeaders.setFocus()
        self.treeWidgetHeaders.setCurrentItem(item)

    @pyqtSignature("on_btnDeleteHeader_clicked()")    
    def on_btnDeleteHeader_clicked(self):
        item = self.treeWidgetHeaders.currentItem()
        if item:
            self.treeWidgetHeaders.takeTopLevelItem(self.treeWidgetHeaders.indexOfTopLevelItem(item))
    
    def accept(self):    
        idx = self.comboBoxLanguage.currentIndex()
        lang = self.comboBoxLanguage.itemData(idx)
        self.settings.setValue("options/language", lang)
        
        userName = self.lineEditUserName.text()
        password = self.lineEditPassword.text()
        self.settings.setValue("options/username", userName)
        self.settings.setValue("options/password", password)
      
        headerFields = []
        headerValues = []
        nHeaders = self.treeWidgetHeaders.topLevelItemCount()
        for i in range(nHeaders):
            headerFields.append(self.treeWidgetHeaders.topLevelItem(i).text(0))
            headerValues.append(self.treeWidgetHeaders.topLevelItem(i).text(1))
        
        self.settings.setValue("options/headerfields", headerFields)
        self.settings.setValue("options/headervalues", headerValues)

        self.close()
    
