# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Fri Aug 15 18:31:40 2014
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
        Settings.resize(422, 316)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Settings)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabAuthentification = QtGui.QWidget()
        self.tabAuthentification.setObjectName(_fromUtf8("tabAuthentification"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabAuthentification)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.tabAuthentification)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tabAuthentification)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditUserName = QtGui.QLineEdit(self.tabAuthentification)
        self.lineEditUserName.setObjectName(_fromUtf8("lineEditUserName"))
        self.gridLayout_3.addWidget(self.lineEditUserName, 0, 1, 1, 1)
        self.lineEditPassword = QtGui.QLineEdit(self.tabAuthentification)
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPassword.setObjectName(_fromUtf8("lineEditPassword"))
        self.gridLayout_3.addWidget(self.lineEditPassword, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabAuthentification, _fromUtf8(""))
        self.tabHeaders = QtGui.QWidget()
        self.tabHeaders.setObjectName(_fromUtf8("tabHeaders"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabHeaders)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeWidgetHeaders = QtGui.QTreeWidget(self.tabHeaders)
        self.treeWidgetHeaders.setObjectName(_fromUtf8("treeWidgetHeaders"))
        self.horizontalLayout_2.addWidget(self.treeWidgetHeaders)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnAddHeader = QtGui.QPushButton(self.tabHeaders)
        self.btnAddHeader.setObjectName(_fromUtf8("btnAddHeader"))
        self.verticalLayout_2.addWidget(self.btnAddHeader)
        self.btnDeleteHeader = QtGui.QPushButton(self.tabHeaders)
        self.btnDeleteHeader.setObjectName(_fromUtf8("btnDeleteHeader"))
        self.verticalLayout_2.addWidget(self.btnDeleteHeader)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabHeaders, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "GeoAdmin Search", None))
        self.label.setText(_translate("Settings", "User name ", None))
        self.label_2.setText(_translate("Settings", "Password ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAuthentification), _translate("Settings", "Authentification", None))
        self.treeWidgetHeaders.headerItem().setText(0, _translate("Settings", "Field", None))
        self.treeWidgetHeaders.headerItem().setText(1, _translate("Settings", "Value", None))
        self.btnAddHeader.setText(_translate("Settings", "Add", None))
        self.btnDeleteHeader.setText(_translate("Settings", "Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHeaders), _translate("Settings", "Headers", None))

