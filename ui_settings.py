# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Sat Aug 16 16:30:48 2014
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
        self.tabOptions = QtGui.QWidget()
        self.tabOptions.setObjectName(_fromUtf8("tabOptions"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tabOptions)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.groupBox_2 = QtGui.QGroupBox(self.tabOptions)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.comboBoxProvider = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxProvider.setObjectName(_fromUtf8("comboBoxProvider"))
        self.horizontalLayout_3.addWidget(self.comboBoxProvider)
        self.gridLayout_7.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.tabOptions)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBoxLanguage = QtGui.QComboBox(self.groupBox)
        self.comboBoxLanguage.setObjectName(_fromUtf8("comboBoxLanguage"))
        self.horizontalLayout.addWidget(self.comboBoxLanguage)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tabOptions, _fromUtf8(""))
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
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 1, 0, 1, 1)
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
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
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
        self.groupBox_2.setTitle(_translate("Settings", "Service provider ", None))
        self.label_4.setText(_translate("Settings", "Preferred provider ", None))
        self.groupBox.setTitle(_translate("Settings", "Language ", None))
        self.label_3.setText(_translate("Settings", "Query language ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOptions), _translate("Settings", "Options", None))
        self.label.setText(_translate("Settings", "User name ", None))
        self.label_2.setText(_translate("Settings", "Password ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAuthentification), _translate("Settings", "Authentification", None))
        self.treeWidgetHeaders.headerItem().setText(0, _translate("Settings", "Field", None))
        self.treeWidgetHeaders.headerItem().setText(1, _translate("Settings", "Value", None))
        self.btnAddHeader.setText(_translate("Settings", "Add", None))
        self.btnDeleteHeader.setText(_translate("Settings", "Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHeaders), _translate("Settings", "Headers", None))

