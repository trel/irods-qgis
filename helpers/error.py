# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Wed Jan  7 20:27:43 2015
#      by: PyQt4 UI code generator 4.11.2
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

class error(object):

    default_text = ''

    def __init__(self,default_text):
        self.default_text = default_text
        Dialog = QtGui.QDialog()
        self.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(281, 86)
        #self.label = QtGui.QLabel(Dialog)
        #self.label.setGeometry(QtCore.QRect(130, 0, 61, 31))
        #self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(28, 30, 225, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Error", None))
        #self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt; color:#ef1700;\">Error</span></p></body></html>", None))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#0f1691;\">%s</span></p><p><br/></p></body></html>"%(self.default_text), None))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     Dialog = QtGui.QDialog()
#     ui = error()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

