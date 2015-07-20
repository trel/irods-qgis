import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
import resources

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'metadata.ui'))

class metadata(QtGui.QDialog, FORM_CLASS):

	meta = ''

	def __init__(self,meta, parent=None):
		 super(metadata, self).__init__(parent)
		 self.setupUi(self)
		 self.meta  = meta
		 count = 0
		 print  self.tableWidget.item(0,0)
		 for val in meta:
		 	newitem = QTableWidgetItem(val)
		 	self.tableWidget.setItem(count,0,newitem)
		 	count += 1