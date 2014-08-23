# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_htmlpopup.ui'
#
# Created: Sat Aug 23 17:34:07 2014
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

class Ui_HtmlPopup(object):
    def setupUi(self, HtmlPopup):
        HtmlPopup.setObjectName(_fromUtf8("HtmlPopup"))
        HtmlPopup.setWindowModality(QtCore.Qt.NonModal)
        HtmlPopup.resize(517, 327)
        self.gridLayout = QtGui.QGridLayout(HtmlPopup)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(HtmlPopup)
        self.webView.setProperty("url", QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(HtmlPopup)
        QtCore.QMetaObject.connectSlotsByName(HtmlPopup)

    def retranslateUi(self, HtmlPopup):
        HtmlPopup.setWindowTitle(_translate("HtmlPopup", "HtmlPopup", None))

from PyQt4 import QtWebKit
