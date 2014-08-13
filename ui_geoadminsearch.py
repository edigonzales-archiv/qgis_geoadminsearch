# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geoadminsearch.ui'
#
# Created: Wed Aug 13 21:23:58 2014
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

class Ui_GeoAdminSearch(object):
    def setupUi(self, GeoAdminSearch):
        GeoAdminSearch.setObjectName(_fromUtf8("GeoAdminSearch"))
        GeoAdminSearch.resize(422, 354)
        self.gridLayout = QtGui.QGridLayout(GeoAdminSearch)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_4 = QtGui.QGroupBox(GeoAdminSearch)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_13 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidgetSearchTables = QtGui.QListWidget(self.groupBox_4)
        self.listWidgetSearchTables.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetSearchTables.setObjectName(_fromUtf8("listWidgetSearchTables"))
        self.horizontalLayout_2.addWidget(self.listWidgetSearchTables)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnAddSearchTable = QtGui.QPushButton(self.groupBox_4)
        self.btnAddSearchTable.setObjectName(_fromUtf8("btnAddSearchTable"))
        self.verticalLayout_2.addWidget(self.btnAddSearchTable)
        self.btnDeleteSearchTable = QtGui.QPushButton(self.groupBox_4)
        self.btnDeleteSearchTable.setObjectName(_fromUtf8("btnDeleteSearchTable"))
        self.verticalLayout_2.addWidget(self.btnDeleteSearchTable)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout_13.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(GeoAdminSearch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(GeoAdminSearch)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GeoAdminSearch.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GeoAdminSearch.reject)
        QtCore.QMetaObject.connectSlotsByName(GeoAdminSearch)

    def retranslateUi(self, GeoAdminSearch):
        GeoAdminSearch.setWindowTitle(_translate("GeoAdminSearch", "GeoAdmin Search", None))
        self.groupBox_4.setTitle(_translate("GeoAdminSearch", "Search tables", None))
        self.btnAddSearchTable.setText(_translate("GeoAdminSearch", "Add", None))
        self.btnDeleteSearchTable.setText(_translate("GeoAdminSearch", "Delete", None))

