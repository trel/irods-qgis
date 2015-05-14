# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Wed Jan  7 18:44:33 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from error import error
import tempfile
from set_root_datastore import root_datastore
from replace import replace
from new_file_name import new_file_name
from check_network import internet_on

#file/folder metadata constants
NAME = 1
PATH = 3
NO_OF_ITEMS = 5
SIZE = 7
CREATED_AT = 9
MODIFIED_AT = 11 

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

class tab_dialog(object):

    """ Tab layout class. Sets up the tabs on the dialog 
    window and provides main functionality"""

    root_path = ''
    auth_object = {}
    index = [] # Index the position of files/folders when they are loaded
    current_store = ''
    current_layer = ''
    current_source = ''
    sources = {}
    dialog = ''
    logout_var = False
    no_connection = False

    def setupUi(self, Dialog, creds):

        """ Configure and setup the UI for dialog box  

        Dialog : QDialog object which inherits the tab layout
        
        creds : Dictionary object containing irods credentials and root datastore

        """

        self.dialog = Dialog
        self.root_path = creds['datastore'] #store the root datastore for user
        self.auth_object = creds #store the session object for user
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 401, 291))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setEnabled(True)
        self.tab.setObjectName(_fromUtf8("tab"))
        self.treeView = QtGui.QTreeView(self.tab)

        # Create custom tree layout with datastore
        self.create_tree()
        self.treeView.setEnabled(True)
        self.treeView.setGeometry(QtCore.QRect(10, 10, 371, 211))
        self.treeView.setObjectName(_fromUtf8("treeView"))

        # Push buttons
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(10, 229, 121, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.load_layers)
        self.pushButton_3 = QtGui.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 229, 115, 32))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_3.clicked.connect(self.logout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.treeView_2 = QtGui.QTreeView(self.tab_2)
        self.create_export_tree()
        self.treeView_2.setGeometry(QtCore.QRect(10, 10, 371, 211))
        self.treeView_2.setObjectName(_fromUtf8("treeView_2"))
        self.pushButton_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_2.clicked.connect(self.save_to_irods)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 229, 121, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_4 = QtGui.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(260, 229, 115, 32))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.setEnabled(False)
        self.pushButton_5 = QtGui.QPushButton(self.tab)
        self.pushButton_5.setGeometry(QtCore.QRect(260, 229, 115, 32))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.set_datastore)
        self.pushButton_6 = QtGui.QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QtCore.QRect(140, 229, 115, 32))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(self.logout)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        #Frame for displaying file metadata
        self.frame = QtGui.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(254, 10, 111, 211))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(_fromUtf8("background:#F5F5A3;\nopacity:0.5;\n"))
        self.frame.setGeometry(QtCore.QRect(254, 10, 0, 0))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.listWidget = QtGui.QListWidget(self.frame)
        self.listWidget.setGeometry(QtCore.QRect(15, 10, 81, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        #Frame for displaying file metadata for export tab
        self.frame_2 = QtGui.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(254, 10, 111, 211))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(_fromUtf8("background:#F5F5A3;\nopacity:0.5;\n"))
        self.frame_2.setGeometry(QtCore.QRect(254, 10, 0, 0))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.listWidget_2 = QtGui.QListWidget(self.frame_2)
        self.listWidget_2.setGeometry(QtCore.QRect(15, 10, 81, 192))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))

        #add item to list
        self.add_item_list("Name",0,True)
        self.add_item_list("N/A",NAME)
        self.add_item_list("Path",2,True)
        self.add_item_list("N/A",PATH)
        self.add_item_list("No. of items",4,True)
        self.add_item_list("N/A",NO_OF_ITEMS)
        self.add_item_list("Size",6,True)
        self.add_item_list("N/A",SIZE)
        self.add_item_list("Created at",8,True)
        self.add_item_list("N/A",CREATED_AT)
        self.add_item_list("Modified at",10,True)
        self.add_item_list("N/A",MODIFIED_AT)
        self.pushButton_4.clicked.connect(self.set_datastore)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def logout(self):

        """ Logout button functionality """

        self.auth_object['sess'] = ''
        self.logout_var = True
        self.dialog.reject()

    def back(self):

        """ Back button functionality """

        self.create_export_tree()
        self.pushButton_2.clicked.disconnect()
        self.pushButton_2.setText(_translate("Dialog", "Save to iRODS", None))
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.save_to_irods)
        self.pushButton_6.clicked.disconnect()
        self.pushButton_6.setText(_translate("Dialog", "Log Out", None))
        self.pushButton_6.clicked.connect(self.logout)
        self.frame_2.setGeometry(QtCore.QRect(254, 10, 0, 0))
        self.treeView_2.doubleClicked.disconnect()
        self.treeView_2.clicked.disconnect()
        self.treeView_2.doubleClicked.connect(self.enableButtonExportLayer)
        self.treeView_2.clicked.connect(self.enableButtonExportLayer)
        self.pushButton_4.setEnabled(False)
 
    def init_meta(self):

        """ Initialize metastructure for files/folders """

        self.add_item_text_list("N/A",NAME)
        self.add_item_text_list("N/A",PATH)
        self.add_item_text_list("N/A",NO_OF_ITEMS)
        self.add_item_text_list("N/A",SIZE)
        self.add_item_text_list("N/A",CREATED_AT)
        self.add_item_text_list("N/A",MODIFIED_AT)

    def add_item_list(self,text,index,menu=False):

        """ Append metadata items for files/folders to the list layout in the widget 

            text : item's text which will be displayed
            index : index of the item in the treeView
            menu : True if the item is a metadata menu item

        """
        item = QtGui.QListWidgetItem()
        item2 = QtGui.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(13)
        if menu:
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            item2.setFont(font)
        self.listWidget.addItem(item)
        self.listWidget_2.addItem(item2)
        self.add_item_text_list(text,index)

    def add_item_text_list(self,text,index):

        """ Set text in metadata items for files/folders """

        item = self.listWidget.item(index)
        item_2 = self.listWidget_2.item(index)
        item.setText(_translate("Dialog", text, None))
        item_2.setText(_translate("Dialog", text, None))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", self.root_path, None))
        self.pushButton.setText(_translate("Dialog", "Upload", None))
        self.pushButton_5.setText(_translate("Dialog", "Set Datastore", None))
        self.pushButton_3.setText(_translate("Dialog", "Log Out", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Import", None))
        self.pushButton_2.setText(_translate("Dialog", "Save to iRODS", None))
        self.pushButton_4.setText(_translate("Dialog", "Set Datastore", None))
        self.pushButton_6.setText(_translate("Dialog", "Log Out", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Export", None))

    def save_to_irods(self):

        """ Creates a tree structure to choose directory when user wants to save layer to irods datastore """

        self.pushButton_4.setEnabled(True)
        self.treeView_2.doubleClicked.disconnect()
        self.treeView_2.clicked.disconnect()
        self.exportModel = QStandardItemModel()
        self.addItems(self.exportModel, self.root_path)
        self.treeView_2.setModel(self.exportModel)
        tree2 = self.treeView_2
        self.pushButton_2.setText(_translate("Dialog", "Select Folder", None))
        self.pushButton_2.setEnabled(False)
        self.treeView_2.doubleClicked.connect(self.enableButtonExport)
        self.treeView_2.clicked.connect(self.enableButtonExport)
        self.treeView_2.expanded.connect(self.expand)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_6.clicked.disconnect()
        self.pushButton_6.setText(_translate("Dialog", "Back", None))
        self.pushButton_6.clicked.connect(self.back)

    def save(self):

        """ Saves the layer in selected folder in user's irods datastore """

        try:
            obj = self.auth_object['sess'].data_objects.create(str(self.current_store+'/'+self.current_layer))
        except:
            r = replace()
            selection = r.selection
            print selection
            if not selection:
                new_name = new_file_name()
                val = new_name.file_name
                if val:
                    if self.current_layer[-4:] == '.shp':
                        self.save_shp(self.current_store+'/'+val)
                    else:
                        name = self.current_store+'/'+val+self.current_layer[-4:]
                        name = str(name)
                        obj = self.auth_object['sess'].data_objects.create(name)
                        file = obj.open('r+')
                        file2 = open(self.sources[self.current_layer],'r+')
                        payload = file2.read()
                        file.write(payload)
                        file.close()
                        file2.close()
                else: 
                    e = error("Cannot leave blank")
                    pass
            else:
                if self.current_layer[-4:] =='.shp':
                    self.save_shp(self.current_store+'/'+self.current_layer[:-4],get=True)
                else:
                    obj = self.auth_object['sess'].data_objects.get(str(self.current_store+'/'+self.current_layer))
                    file2 = open(self.sources[self.current_layer],'r+')
                    payload = file2.read()
                    file = obj.open('r+')
                    file.write('')
                    file.write(payload)
                    file.close()
                    file2.close()

        else:
            if self.current_layer[-4:] == '.shp':
                self.save_shp(str(self.current_store+'/'+self.current_layer[:-4]))
            else:
                file = obj.open('r+')
                file2 = open(self.sources[self.current_layer],'r+')
                payload = file2.read()
                file.write(payload)
                file.close()
                file2.close()


        self.pushButton_2.clicked.disconnect()
        self.pushButton_2.setText(_translate("Dialog", "Save to iRODS", None))
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.save_to_irods)
        self.pushButton_6.clicked.disconnect()
        self.pushButton_6.setText(_translate("Dialog", "Log Out", None))
        self.pushButton_6.clicked.connect(self.logout)
        self.frame_2.setGeometry(QtCore.QRect(254, 10, 0, 0))
        self.pushButton_4.setEnabled(False)
        self.create_export_tree()

    def save_shp(self,val,get=False):

        """ Saves the shapefile. Takes care of the other files associated with shapefiles 

            val : Name of the layer to be stored in datastore minus the extension 

            get : If the layer does not exist, it is created and get is False.     

        """

        val = str(val)
        exts = ['.shp','.prj','.shx','.dbf']
        for ext in exts:
            print ext,val
            if get:
                try:
                    obj = self.auth_object['sess'].data_objects.get(str(val+ext))
                    file = obj.open('r+')
                except:
                    obj = self.auth_object['sess'].data_objects.create(str(val+ext))
            else:
                obj = self.auth_object['sess'].data_objects.create(str(val+ext))

            file = obj.open('r+')
            file2 = open(self.sources[self.current_layer][:-4]+ext,'r+')
            payload = file2.read()
            file.write('')
            file.write(payload)
            file.close()
            file2.close()


    def set_datastore(self):

        """ Allows user to set the root datastore """

        obj = root_datastore(str(self.root_path))
        value = obj.root_store
        try :
            self.auth_object['sess'].collections.get(str(value))
        except : 
            if internet_on():
                e = error("Incorrect datastore")
            else:
                e = error("Network Error. Check Your Connection")
            return False

        else:
            self.root_path = str(value)
            self.frame.setGeometry(QtCore.QRect(254, 10, 0, 0))
            self.frame_2.setGeometry(QtCore.QRect(254, 10, 0, 0))
            self.dialog.setWindowTitle(_translate("Dialog", self.root_path, None))
            self.create_tree()
            if self.tabWidget.currentIndex() ==1:
                self.save_to_irods()
            else:
                self.create_export_tree()

    def enableButton(self,tree):

        """ Configures class variables when a file/folder is selected on the dialog box 

            tree : Reference to the current QModelIndex object

        """
        scroll_size = self.treeView.verticalScrollBar().maximum()

        self.init_meta()
        item = tree.model().itemFromIndex(tree)
        data = tree.data()

        self.current_store = self.build_structure(tree) 
        self.current_layer = tree.data()

        if not data:
            self.frame.setGeometry(QtCore.QRect(254, 10, 0, 0))

        if not item.hasChildren() and data:
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
        self.display_metadata()

        if scroll_size <=0:
            self.frame.setGeometry(QtCore.QRect(270, 10, 111, 211))
        else:
            self.frame.setGeometry(QtCore.QRect(254, 10, 111, 211))


    def display_metadata(self):

        """ Provides functionality for displaying metadata of files/folders """

        type = False
        err = False
        # Tyep True : File, Type False: Folder

        try:
            obj = self.auth_object['sess'].collections.get(str(self.current_store))
        except Exception as e:
            try:
                obj = self.auth_object['sess'].data_objects.get(str(self.current_store))
                type = True
            except Exception as e:
                err = True
        finally:
            if not err:
                if type:
                    size = self.get_file_size(obj.size)
                    metas= [obj.name,size,obj.create_time,obj.modify_time]
                    self.load_items_list(file=metas)
                else: 
                    count = 0 
                    for item in obj.subcollections:
                        count = count+1

                    for item in obj.data_objects:
                        count = count+1
                    metas = [count,obj.name,obj.path]

                    self.load_items_list(folder=metas)
            else:
                e = error("Network Error.Check your Connection")
                self.dialog.reject()
     

    def load_items_list(self,file='',folder=''):

        """ Loads metadata items for files/folders in the list view widget """

        if file:
            self.add_item_text_list(str(file[0]),NAME)
            self.add_item_text_list(str(file[1]),SIZE)
            self.add_item_text_list(str(file[2]),CREATED_AT)
            self.add_item_text_list(str(file[3]),MODIFIED_AT)
            self.add_item_text_list(str(self.current_store),PATH)
        else:
            self.add_item_text_list(str(folder[1]),NAME)
            self.add_item_text_list(str(folder[0]),NO_OF_ITEMS)
            self.add_item_text_list(str(folder[2]),PATH)

    def get_file_size(self,size):

        """
        Calculates the size of a file in appropriate unit

        Size : Size of the file in bits

         """

        n = len(str(size))
        result = ''
        if (n<=4):
            result = '%.2F bytes'%(size/8.0)
        elif (n<=7):
            result = '%.2F KB'%(size/1024.0)
        elif (n<=13):
            result = '%.2F MB'%((size/1024.0)/1024.0)
        elif (n>13):
            result = '%.2F GB'%(((size/1024.0)/1024.0)/1024.0)

        return result

    def create_tree(self):

        """ Creates the tree view layout and appends a model to the tree """

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.model = QStandardItemModel()
        self.addItems(self.model, self.root_path)
        self.treeView.setModel(self.model)
        tree = self.treeView
        self.treeView.doubleClicked.connect(self.enableButton)
        self.treeView.clicked.connect(self.enableButton)
        self.treeView.expanded.connect(self.expand)

    def create_export_tree(self):

        """ Creates the tree view layout and appends a model to the tree """

        self.treeView_2.setContextMenuPolicy(Qt.CustomContextMenu)
        try:
            self.treeView_2.doubleClicked.disconnect()
            self.treeView_2.clicked.disconnect()
        except:
            self.treeView_2.doubleClicked.connect(self.enableButtonExportLayer)
            self.treeView_2.clicked.connect(self.enableButtonExportLayer)
        finally:
            self.model2 = QStandardItemModel()
            self.addItemsExport(self.model2)
            self.treeView_2.setModel(self.model2)
            tree2 = self.treeView_2
            self.treeView_2.doubleClicked.connect(self.enableButtonExportLayer)
            self.treeView_2.clicked.connect(self.enableButtonExportLayer)


    def enableButtonExportLayer(self,tree2):

        """ 
        Enables the save button when a layer is selected in export tab 

        tree2 : Reference to the current QModelIndex object

        """

        self.pushButton_2.setEnabled(True)
        self.current_layer = tree2.data()

    def enableButtonExport(self,tree2): 
        
        """ 
        Same as above but enables the select folder option when a folder is selected in export tab

        tree2 : Reference to the current QModelIndex object

        """
        scroll_size = self.treeView_2.verticalScrollBar().maximum()
        self.init_meta()
        data = tree2.data()
        item = tree2.model().itemFromIndex(tree2)
        self.current_store = self.build_structure(tree2) 

        if not data:
            self.frame_2.setGeometry(QtCore.QRect(254, 10, 0, 0))

        if data and item.hasChildren():
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setEnabled(False)
        self.display_metadata()

        if scroll_size <=0:
            self.frame_2.setGeometry(QtCore.QRect(270, 10, 111, 211))
        else:
            self.frame_2.setGeometry(QtCore.QRect(254, 10, 111, 211))


    def addItemsExport(self,parent):
        """ 
        Add map layers from current canvas to the list view in export tab 

        parent : Reference to the current QModel for tree view in export tab

        """

        layer_names = []
        layers = QgsMapLayerRegistry.instance().mapLayers()
        icon_path_layer = ':/plugins/irods_qgis/layers.png'

        for layer in layers:
            layer_names.append(layers[layer])

        for name in layer_names:
            icon = QIcon(icon_path_layer)
            item = QStandardItem(icon,str(name.name())+str(name.source())[-4:])
            self.sources[str(name.name())+str(name.source())[-4:]] = str(name.source())
            parent.appendRow(item)


        
    def expand(self,tree):
        """
        Callback after an item is expanded in the tree view

        tree : Reference to current QModelIndex object

        """

        self.frame.setGeometry(QtCore.QRect(254, 10, 0, 0))
        item = tree.model().itemFromIndex(tree)
        if item not in self.index:
            #for i in items :
            self.index.append(item)
            item.removeRow(0)
            store = self.build_structure(tree)
            self.addItems(item,str(store))

    def build_structure(self,tree):

        """ 
        Builds path for the selected item on the treeview for either tab (unless layers are open on the export tab)

        tree : Reference to the current QModelIndex object

        """

        path = self.root_path 
        current_tree = tree
        current_name = tree.data()
        while current_tree.parent().data():

            path = path + '/' + current_tree.parent().data()
            current_tree = current_tree.parent()

        path = path + '/' + current_name

        return path

    def addItems(self,parent,path):

        """ 
        Adds sub-items to the tree view when an item is expanded

        path : path to the parent obtained from function above

        parent : The QModel object for tree view

        """
        self.no_connection = False
        folders = []
        files = []
        datastore = path
        dummy_child = QStandardItem('')
        icon_path_folder = ':/plugins/irods_qgis/folder.png'
        icon_path_file = ':/plugins/irods_qgis/file-icon.png'
        try:
            coll = self.auth_object['sess'].collections.get(datastore)
        except Exception as e:
            if internet_on():
                parent.appendRow(dummy_child)
                return False
            else:
                e = error("Network Error.Check your Connection")
                self.dialog.reject()

        for col in coll.subcollections:
            folders.append("%s"%(col.name))

        for col in coll.data_objects:
            files.append("%s"%(col.name))

        if folders or files:

            for text in folders:
                icon = QIcon(icon_path_folder)
                item = QStandardItem(icon,text)
                parent.appendRow(item)
                item.appendRow(dummy_child)

            for text in files:
                icon = QIcon(icon_path_file)
                item = QStandardItem(icon,text)
                parent.appendRow(item)

        else:

            parent.appendRow(dummy_child)


    ###########  LOADING LAYERS ################

    def load_layers(self,tree):

        """ 
        Calls all the functions involved with loading a selected layer from the irods datastore

        tree : Reference to the current QModelIndex object

        """

        #check file extension
        filename =  self.current_layer
        store = self.current_store
        file_type = True
        # True : Vector
        # False : Raster
        file_ext = filename[-3:]
        base_name = filename[:-4]
        vector_formats = ['shp', 'dbf', 'shx', 'prj', 'csv']
        raster_formats = ['png', 'jpg', 'jpeg', 'bmp', 'tif']
        shp_ext = ['shp', 'dbf', 'shx', 'prj']
        if file_ext in vector_formats:
            file_type = True
        elif file_ext in raster_formats:
            file_type = False
        else:
            e = error("Incorrect Spatial Format")
            return False
        dirpath = tempfile.mkdtemp()
        if file_type:
            if not file_ext == 'csv':
                main_file_path = ''
                for ext in shp_ext:
                    file_path = dirpath+'/'+base_name+'.'+ext
                    print file_path
                    if ext == 'shp':
                        main_file_path = file_path
                    file = open(file_path,'w+')
                    file_source = self.get_source(store[:-3]+ext)
                    if file_source:
                        file.write(file_source)
                        file.close()
                    else:
                        e = error("File Not Found or Corrupted'")
                        return False
                self.load_vector_layer(main_file_path,base_name)
            else:
                file_path = dirpath+'/'+filename
                file = open(file_path,'w+')
                file_source = self.get_source(store)
                if file_source:
                    file.write(file_source)
                    file.close()
                else:
                    e = error("File Not Found or Corrupted'")
                    return False
                self.load_vector_layer(file_path,base_name,'delimitedtext')
        else:
            file_path = dirpath+'/'+filename
            file = open(file_path, 'w+')
            file_source = self.get_source(store)
            if file_source:
                file.write(file_source)
                file.close()
            else:
                e = error("File Not Found or Corrupted'")
                return False
            self.load_raster_layer(file_path,base_name)

    def load_raster_layer(self,path,base_name):

        """ 
        Loads a raster layer to the map canvas

        path : Data source path of the layer

        base_name : Layer name to be displayed on map canvas

        """

        rlayer = QgsRasterLayer(path, base_name)
        if not rlayer.isValid():
            e = error("Layer failed to load!")
        else:
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            self.create_export_tree()

    def load_vector_layer(self,path,base_name,provider='ogr'):

        """ 
        Loads a vector layer to the map canvas

        path : Data source path of the layer

        base_name : Layer name to be displayed on map canvas

        provider : Provider name for the vector layer. Default is OGR

        """

        vlayer = QgsVectorLayer(path, base_name, 'ogr')
        if not vlayer.isValid():
            e = error("Layer failed to load!")
        else:
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)
            self.create_export_tree()


    def get_source(self,store):

        """ 
        Returns the file content for the selected file on irods datastore

        Store : Datastore url for the selected file

        """

        try:
            source = self.auth_object['sess'].data_objects.get(str(store))
            file = source.open('r+')
        except:
            return False
            #print 'ERROR: File Not Found'
        else:
            payload = file.read()
            file.close()
            return payload

        file = open()
        QgsMapLayerRegistry.instance().addMapLayer()



