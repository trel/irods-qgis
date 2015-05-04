# -*- coding: utf-8 -*-
"""
/***************************************************************************
 irods_qgisDialog
                                 A QGIS plugin
 Connect to irods via qgis
                             -------------------
        begin                : 2014-12-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Amit Juneja / BCF
        email                : amitj@email.arizona
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *

import tempfile

#from irods_qgis import irods_qgis
from irods.session import iRODSSession
from irods.exception import CAT_INVALID_AUTHENTICATION , OVERWITE_WITHOUT_FORCE_FLAG
#from helpers.tab_layout import tab_dialog
from helpers.error import error
from helpers.replace import replace
from helpers.new_file_name import new_file_name
from helpers.check_network import internet_on
import webbrowser

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'table_dialog.ui'))


class table_dialog(QtGui.QDialog, FORM_CLASS):

    connection_object = ''
    root_path = ''
    logout_var = False
    import_tree = ''
    export_tree = ''
    current_layer = ''
    current_store = ''
    sources = {}


    def __init__(self,creds,parent=None):
        """Constructor."""
        super(table_dialog, self).__init__(parent)

        #initialize dicts and lists for the plugin

        self.root_path = str(creds['datastore']) #store the root datastore for user
        self.connection_object = creds['sess']
        self.setupUi(self)
        self.init_import_tab()
        self.set_events()
        self.init_export_tab()


    ## INITIALIZE IMPORT TAB FUNCTIONS


    def set_events(self):

        """
        Set events for all the button pushes

        """
        self.logout_i.clicked.connect(self.logout)#logout(self.connection_object, self.logout_var) )
        self.logout_e.clicked.connect(self.logout)
        self.import_tab.expanded.connect(self.expand)
        self.export_tab.expanded.connect(self.expand_export)
        self.import_tab.clicked.connect(self.enable_upload)
        self.tabWidget.currentChanged.connect(self.tab_changed)
        #self.export_tab.clicked.connect(self.enable_export)
        self.datastore_e.returnPressed.connect(self.change_datastore_export_tree)
        self.datastore_i.returnPressed.connect(self.change_datastore)
        self.upload_i.clicked.connect(self.load_layers)
        self.upload_e.clicked.connect(self.init_export_tree)
        self.search_button_i.clicked.connect(self.search_import)
        self.search_i.returnPressed.connect(self.search_import)
        self.search_button_e.clicked.connect(self.search_export)
        self.search_e.returnPressed.connect(self.search_export)
        self.help.clicked.connect(self.help_action)
        self.help_2.clicked.connect(self.help_action)

    def init_import_tab(self):

        """ Creates the tree view layout and appends a model to the tree """

        self.import_tree = self.import_tab
        self.import_tree.setColumnCount(3)
        self.import_tree.header().hideSection(3)
        self.import_tree.header().resizeSection(0,150)
        self.datastore_i.setText(self.root_path)
        self.addItems(self.import_tree,self.root_path,self.import_tree)

    def addItems(self,parent,path,tab):

        """ 
        Adds sub-items to the tree view when an item is expanded

        path : path to the parent obtained from function above

        parent : The QModel object for tree view

        """
        folders = []
        files = []
        sizes = []
        date_files = []
        date_folder = []
        datastore = str(path)
        icon_path_folder = ':/plugins/irods_qgis/folder.png'
        icon_folder = QIcon(icon_path_folder)
        icon_path_file = ':/plugins/irods_qgis/file-icon.png'
        icon_file = QIcon(icon_path_file)
        item_count = 0
        try:
            coll = self.connection_object.collections.get(datastore)
        except:
            if internet_on():
                item = QTreeWidgetItem(parent,['Not Found'])
                tab.insertTopLevelItem(item_count,item)
                return False
            else:
                e = error("Network Error.Check your Connection")
                #self.dialog.reject()
               

        for col in coll.subcollections:
            folders.append("%s"%(col.name))
            

        for col in coll.data_objects:
            files.append("%s"%(col.name))
            sizes.append(int(col.size))
            date_files.append(str(col.create_time))

        if folders or files:

            for index,text in enumerate(folders):
                store_name = "%s/%s"%(path,text)
                item = QTreeWidgetItem(parent,[text,'',''])
                item.setText(3,store_name)
                item.setIcon(0,icon_folder)
                tab.insertTopLevelItem(item_count,item)
                item_count +=1
                item = QTreeWidgetItem(item,[''])

            for index,text in enumerate(files):
                store_name = "%s/%s"%(path,text)
                item = QTreeWidgetItem(parent,[text, self.get_file_size(sizes[index]), date_files[index]])
                item.setText(3,store_name)
                item.setIcon(0,icon_file)
                tab.insertTopLevelItem(item_count,item)
                item_count +=1


        else:
            item = QTreeWidgetItem(parent,[''])
            tab.insertTopLevelItem(item_count,item)
        return True

    def tab_changed(self):
        if self.tabWidget.currentIndex() == 1:
            self.init_export_tab()

    def help_action(self):
        webbrowser.open_new_tab('https://github.com/BioComputing/irods-qgis')

    ## INITIALIZE EXPORT TAB FUNCTIONS



    def init_export_tab(self):
        self.datastore_e.setEnabled(False)
        self.search_e.setEnabled(False)
        self.search_button_e.setEnabled(False)
        self.datastore_e.setText('')
        self.export_tree = self.export_tab
        self.export_tree.clear()
        self.export_tree.setColumnCount(0)
        self.export_tree.setHeaderLabel('Layer Name')
        self.addOpenLayers()
        self.upload_e.setText('Select')
        self.upload_e.setEnabled(False)
        self.logout_e.setText('Log Out')

        ## export TAB events for showing open layers | Disconnect them if clicked on Select and vice versa

        self.export_tab.clicked.disconnect()
        self.export_tab.clicked.connect(self.enable_select)
        self.upload_e.clicked.disconnect()
        self.upload_e.clicked.connect(self.init_export_tree)
        self.logout_e.clicked.disconnect()
        self.logout_e.clicked.connect(self.logout)

    def addOpenLayers(self):
        """ 
        Add map layers from current canvas to the list view in export tab 

        parent : Reference to the current QModel for tree view in export tab

        """

        layer_names = []
        layers = QgsMapLayerRegistry.instance().mapLayers()
        icon_path_layer = ':/plugins/irods_qgis/layers.png'
        layer_count = 0

        for layer in layers:
            layer_names.append(layers[layer])

        for name in layer_names:
            icon = QIcon(icon_path_layer)
            item = QTreeWidgetItem(self.export_tree,[str(name.name())+str(name.source())[-4:]])
            item.setIcon(0,icon)
            self.sources[str(name.name())+str(name.source())[-4:]] = str(name.source())
            self.export_tree.insertTopLevelItem(layer_count,item)
            layer_count += 1



    ## COMMON EVENTS

    def expand(self,index):
        """
        Callback after an item is expanded in the tree view

        index : Index of the item selected

        """
        item = self.import_tree.itemFromIndex(index)
        if item.childCount() ==1 and not item.child(0).text(3):
            item.takeChild(0)
            path = item.text(3)
            self.addItems(item,path,self.import_tree)
        else:
            pass

    def expand_export(self,index):
        """
        Callback after an item is expanded in the tree view

        index : Index of the item selected

        """
        item = self.export_tree.itemFromIndex(index)
        if item.childCount() ==1 and not item.child(0).text(3):
            item.takeChild(0)
            path = item.text(3)
            self.addItems(item,path,self.import_tree)
        else:
            pass

    def logout(self):
        """ Logout button functionality """
        self.connection_object = ''
        self.logout_var = True
        self.reject()

    def add_search_items(self,parent,path_list):
        count = 0
        icon_path_folder = ':/plugins/irods_qgis/folder.png'
        icon_folder = QIcon(icon_path_folder)
        icon_path_file = ':/plugins/irods_qgis/file-icon.png'
        icon_file = QIcon(icon_path_file)
        for path in path_list:
            if path[0] == 0:
                col = self.connection_object.collections.get(path[1])
                item = QTreeWidgetItem([str(col.name),'',''])
                item.setText(3,path[1])
                item.setIcon(0,icon_folder)
                parent.insertTopLevelItem(count,item)
                item = QTreeWidgetItem(item,[''])
            else:
                col = self.connection_object.data_objects.get(path[1])
                item = QTreeWidgetItem([str(col.name),self.get_file_size(col.size),str(col.modify_time)])
                item.setText(3,path[1])
                item.setIcon(0,icon_file)
                parent.insertTopLevelItem(count,item)
            count+=1


    ## IMPORT EVENTS


    def enable_upload(self,index):
        """
        Enables import button after a FILE is clicked

        index : Index of the item selected

        """
        item = self.import_tree.itemFromIndex(index)
        if item.text(1):
            self.upload_i.setEnabled(True)
            self.current_layer = str(item.text(0))
            self.current_store = str(item.text(3))
        else:
            self.upload_i.setEnabled(False)
            self.datastore_i.setText(item.text(3))

    def change_datastore(self):
        """
        Changes datastore after it is typed and return is pressed (for import tab)

        index : Index of the item selected

        """
        path = str(self.datastore_i.text())
        self.import_tree.clear()
        if path:
            self.addItems(self.import_tree,path,self.import_tree)
        else:
            #self.addItems(self.import_tree,path,self.import_tree)
            self.addItems(self.import_tree,self.root_path,self.import_tree)

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

    def search_import(self):
        paths = []
        query = str(self.search_i.text())
        if query:
            result = self.import_tree.findItems(query,Qt.MatchContains)
            if result:
                for item in result:
                    if item.text(1):
                        paths.append([1,str(item.text(3))])
                    else:
                        paths.append([0,str(item.text(3))])
                self.import_tree.clear()
                self.add_search_items(self.import_tree,paths)
            else:
                self.import_tree.clear()
                item = QTreeWidgetItem(['No Results Found'])
                self.import_tree.insertTopLevelItem(0,item)
        else:
            self.import_tree.clear()
            self.addItems(self.import_tree,self.root_path,self.import_tree)


    ## EXPORT EVENTS

    def enable_select(self,index):
        """
        Enables select button after a LAYER is clicked

        """

        self.upload_e.setEnabled(True)
        item = self.export_tree.itemFromIndex(index)
        self.current_layer = item.text(0)

    def enable_export(self,index):
        """
        Enables export button after a FOLDER is clicked

        """
        item = self.export_tree.itemFromIndex(index)
        if not item.text(1):
            self.upload_e.setEnabled(True)
            self.current_store = str(item.text(3))
            self.datastore_e.setText(item.text(3))
        else:
            self.upload_e.setEnabled(False)
            

    def init_export_tree(self):
        """
        Creates an export tree, similar to import tree for selecting a folder
        to save the layer from QGIS to IRODS

        """
        if self.root_path == '/iplant/home/shared':
            e = error('Guests cannot save files')
            pass
        else:
            self.datastore_e.setEnabled(True)
            self.search_e.setEnabled(True)
            self.search_button_e.setEnabled(True)
            self.datastore_e.setText(self.root_path)
            self.export_tree.clear()
            self.export_tree.setColumnCount(3)
            self.export_tree.setHeaderLabels(['Name', 'Size', 'Date Modified', ''])
            self.export_tree.header().hideSection(3)
            self.export_tree.header().resizeSection(0,150)
            self.addItems(self.export_tree,self.root_path,self.export_tree)
            self.upload_e.setText('Export')
            self.upload_e.setEnabled(False)
            self.logout_e.setText('Back')

            ## export tree events | Disconnect them if clicked on back and vice versa

            self.export_tab.clicked.disconnect()
            self.export_tab.clicked.connect(self.enable_export)
            self.upload_e.clicked.disconnect()
            self.upload_e.clicked.connect(self.save)
            self.logout_e.clicked.disconnect()
            self.logout_e.clicked.connect(self.init_export_tab)


    def change_datastore_export_tree(self):
        """
        Changes datastore after it is typed and return is pressed (for export tab)

        index : Index of the item selected

        """
        path = str(self.datastore_e.text())
        self.export_tree.clear()
        if path:
            self.addItems(self.export_tree,path,self.export_tree)
        else:
            self.addItems(self.export_tree,self.root_path,self.export_tree)

    def save(self):

        """ Saves the layer in selected folder in user's irods datastore """
        try:
            obj = self.connection_object.data_objects.create(str(self.current_store+'/'+self.current_layer))
        except:
            r = replace()
            selection = r.selection
            if not selection:
                new_name = new_file_name()
                val = new_name.file_name
                if val:
                    if self.current_layer[-4:] == '.shp':
                        self.save_shp(self.current_store+'/'+val)
                    else:
                        name = self.current_store+'/'+val+self.current_layer[-4:]
                        name = str(name)
                        obj = self.connection_object.data_objects.create(name)
                        file = obj.open()
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
                    try:
                      obj = self.connection_object.data_objects.create(str(self.current_store+'/'+self.current_layer))
                    except Exception as e:
                        if e == OVERWITE_WITHOUT_FORCE_FLAG:
                            obj = self.connection_object.data_objects.create(str(self.current_store+'/'+self.current_layer))
                        else:
                            obj = self.connection_object.data_objects.get(str(self.current_store+'/'+self.current_layer))
                    finally:
                        file2 = open(self.sources[self.current_layer],'r+')
                        payload = file2.read()
                        file = obj.open('r+')
                        file.write('')
                        file.write(payload)
                        file.close()
                        file2.close()

            self.init_export_tab()

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
            # Refresh the import tab too
            self.import_tree.clear()
            self.addItems(self.import_tree,self.root_path,self.import_tree)
            # Get back to Export tab 
            self.init_export_tab()



    def save_shp(self,val,get=False):

        """ Saves the shapefile. Takes care of the other files associated with shapefiles 

            val : Name of the layer to be stored in datastore minus the extension 

            get : If the layer does not exist, it is created and get is False.     

        """

        val = str(val)
        exts = ['.shp','.prj','.shx','.dbf']
        for ext in exts:
            if get:
                try:
                    obj = self.connection_object.data_objects.get(str(val+ext))
                    file = obj.open('r+')
                except:
                    obj = self.connection_object.data_objects.create(str(val+ext))
            else:
                try:
                    obj = self.connection_object.data_objects.create(str(val+ext))
                except Exception as e:
                    if e == OVERWITE_WITHOUT_FORCE_FLAG:
                        pass
                    else:
                        er = error(str(e))

            file = obj.open('w+')
            file2 = open(self.sources[self.current_layer][:-4]+ext,'r+')
            payload = file2.read()
            file.write('')
            file.write(payload)
            file.close()
            file2.close()
            # Refresh the import tab too
            self.import_tree.clear()
            self.addItems(self.import_tree,self.root_path,self.import_tree)


    def search_export(self):
        paths = []
        query = str(self.search_e.text())
        if query:
            result = self.export_tree.findItems(query,Qt.MatchContains)
            if result:
                for item in result:
                    if item.text(1):
                        paths.append([1,str(item.text(3))])
                    else:
                        paths.append([0,str(item.text(3))])
                self.export_tree.clear()
                self.add_search_items(self.export_tree,paths)
            else:
                self.export_tree.clear()
                item = QTreeWidgetItem(['No Results Found'])
                self.export_tree.insertTopLevelItem(0,item)
        else:
            self.export_tree.clear()
            self.addItems(self.export_tree,self.root_path,self.export_tree)

    ## QGIS FUNCTIONS

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
            #self.create_export_tree()

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
            #self.create_export_tree()


    ## HELPER METHODS

    def get_file_size(self,size):

        """
        Calculates the size of a file in appropriate unit

        Size : Size of the file in bits

         """

        n = len(str(size))
        result = ''
        if (n<=4):
            result = '%.2F bytes'%(size/8.0)
        elif (n<7):
            result = '%.2F KB'%(size/1024.0)
        elif (n<13):
            result = '%.2F MB'%((size/1024.0)/1024.0)
        elif (n>13):
            result = '%.2F GB'%(((size/1024.0)/1024.0)/1024.0)

        return result

    def get_source(self,store):

        """ 
        Returns the file content for the selected file on irods datastore

        Store : Datastore url for the selected file

        """

        try:
            source = self.connection_object.data_objects.get(str(store))
            file = source.open()
        except:
            return False
            #print 'ERROR: File Not Found'
        else:
            payload = file.read()
            file.close()
            return payload

        file = open()
        QgsMapLayerRegistry.instance().addMapLayer()


    # METADATA FUNCTIONS

    def get_num_of_items(store, count=0):
        """ Return the number of items in a collections """

        coll = self.connection_object.collections.get(store)

        if coll.data_objects != []:
            for col in coll.data_objects:
                count += 1

        if coll.subcollections != []:
            for col in coll.subcollections:
                count += 1
                self.get_num_of_items(str(col.path),count)

        return count





   