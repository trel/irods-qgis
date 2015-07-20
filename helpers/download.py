# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Fri Jan  9 18:39:35 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os

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

class download(object):

    selection = False
    dialog = ''
    del_folder=''
    name = ''

    def __init__(self,del_folder):
        Dialog = QtGui.QDialog()
        self.del_folder=os.path.basename(del_folder)
        self.dialog = Dialog
        self.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 120)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 20, 231, 40))
        self.label.setObjectName(_fromUtf8("label"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 80, 164, 32))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        new_del_folder = ''
        size = len(self.del_folder)
        print size
        if (size>17):
            new_del_folder = self.del_folder[:5] + '...' +self.del_folder[size-9:-4] + self.del_folder[-4:] 
        else:
            new_del_folder = self.del_folder
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#7f0f05;\">Incorrect spatial format.<br> Download <b>%s</b> ?</span></p></body></html>"%(new_del_folder), None))


    def accept(self):
        self.selection = True
        fname = QtGui.QFileDialog.getExistingDirectory()
        if fname:
            if os.path.basename(fname) =='untitled':
                fname = fname[:-9]
            self.name = fname
        else:
            self.reject()
        self.dialog.reject()

    def reject(self):
        self.selection = False
        self.dialog.reject()



