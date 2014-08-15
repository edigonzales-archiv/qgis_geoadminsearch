# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Fri Aug 15 16:05:23 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(422, 354)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_4 = QtGui.QGroupBox(Settings)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_13 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeWidgetHeaders = QtGui.QTreeWidget(self.groupBox_4)
        self.treeWidgetHeaders.setObjectName(_fromUtf8("treeWidgetHeaders"))
        self.horizontalLayout_2.addWidget(self.treeWidgetHeaders)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnAddHeader = QtGui.QPushButton(self.groupBox_4)
        self.btnAddHeader.setObjectName(_fromUtf8("btnAddHeader"))
        self.verticalLayout_2.addWidget(self.btnAddHeader)
        self.btnDeleteHeader = QtGui.QPushButton(self.groupBox_4)
        self.btnDeleteHeader.setObjectName(_fromUtf8("btnDeleteHeader"))
        self.verticalLayout_2.addWidget(self.btnDeleteHeader)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout_13.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "GeoAdmin Search", None))
        self.groupBox_4.setTitle(_translate("Settings", "Headers ", None))
        self.treeWidgetHeaders.headerItem().setText(0, _translate("Settings", "Field", None))
        self.treeWidgetHeaders.headerItem().setText(1, _translate("Settings", "Value", None))
        self.btnAddHeader.setText(_translate("Settings", "Add", None))
        self.btnDeleteHeader.setText(_translate("Settings", "Delete", None))

