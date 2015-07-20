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
import resources

import tempfile
import time

#from irods_qgis import irods_qgis
from irods.session import iRODSSession
from irods.exception import CAT_INVALID_AUTHENTICATION , OVERWITE_WITHOUT_FORCE_FLAG, CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME
#from helpers.tab_layout import tab_dialog
from helpers.error import error
from helpers.replace import replace
from helpers.new_file_name import new_file_name
from helpers.new_folder_name import new_folder_name
from helpers.check_network import internet_on
from helpers.content_type import content_types
from helpers.metadata import metadata
from helpers.delete_conf import del_conf
from helpers.download import download
import webbrowser

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'table_dialog copy.ui'))


class table_dialog(QtGui.QDialog, FORM_CLASS):

    connection_object = ''
    root_path = ''
    logout_var = False
    import_tree = ''
    export_tree = ''
    current_layer = ''
    current_store = ''
    current_index = ''
    sources = {}

    # List of Functions

        ## INITIALIZE IMPORT TAB FUNCTIONS

            # set_events ()
            # init_import_tab ()
            # addItems (parent,path,tab)
            # tab_changed ()
            # help_action ()

        ## INITIALIZE EXPORT TAB FUNCTIONS

            # init_export_tab ()
            # addOpenLayers ()

        ## COMMON EVENTS

            # expand (index)
            # expand_export (index)
            # logout ()
            # add_search_items (parent,path_list)
            # navigate_home_url ()
            # navigate_shared_url ()
            # pre_change_datastore ()
            # get_spatial_extension ()
            # set_prog_bar_text (text=None,spatial=None)
            # addFolder ()
            # delFolder ()
            # metadata ()
            # download_file (path, filestore)

        ## IMPORT EVENTS

            # enable_upload (index)
            # change_datastore (url=None)
            # load_layers (tree)
            # search_import ()

        ## EXPORT EVENTS

            # enable_select (index)
            # enable_export (index)
            # init_export_tree ()
            # pre_change_datastore_export_tree ()
            # change_datastore_export_tree ()
            # save ()
            # save_shp (val,get=False)
            # search_export ()

        ## QGIS FUNCTIONS

            # load_raster_layer (path,base_name)
            # load_vector_layer (path,base_name,provider='ogr')
            # get_file_size (size)
            # get_source (store)
            # init_progress ()
            # update_timer (val)
            # restart_timer ()

        ## METADATA FUNCTIONS

            # get_num_of_items (store,count=0)


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
        self.tabWidget.setCurrentIndex(0)

        # hide progress bar and display text
        self.progressBar.hide()
        self.set_prog_bar_text('No spatial file selected')
        # Initialize icons
        icon_add_folder= QIcon(':/plugins/irods_qgis/add-folder.png')
        icon_delete= QIcon(':/plugins/irods_qgis/delete.png')
        icon_home= QIcon(':/plugins/irods_qgis/home.png')
        icon_shared= QIcon(':/plugins/irods_qgis/globe_disconnected.png')

        self.add_folder.setIcon(icon_add_folder)
        self.delete_2.setIcon(icon_delete)
        self.add_folder1.setIcon(icon_add_folder)
        self.delete_3.setIcon(icon_delete)

        self.home_url.setIcon(icon_home)
        self.shared_url.setIcon(icon_shared)
        self.home_url_2.setIcon(icon_home)
        self.shared_url_2.setIcon(icon_shared)

        if self.root_path == '/iplant/home/shared':
            self.add_folder.setEnabled(False)
            self.delete_2.setEnabled(False)


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
        self.add_folder.clicked.connect(lambda :self.addFolder())
        self.add_folder1.clicked.connect(lambda :self.addFolder(export=True))
        self.delete_2.clicked.connect(lambda :self.delFolder())
        self.delete_3.clicked.connect(lambda :self.delFolder(export=True))
        self.get_info_i.clicked.connect(lambda :self.metadata())
        self.get_info_e.clicked.connect(lambda :self.metadata(export=True))
        #self.export_tab.clicked.connect(self.enable_export)
        self.datastore_e.returnPressed.connect(self.pre_change_datastore_export_tree)
        self.datastore_i.returnPressed.connect(self.pre_change_datastore )
        self.view_i.clicked.connect(self.pre_change_datastore )
        self.view_e.clicked.connect(self.pre_change_datastore_export_tree)
        self.upload_i.clicked.connect(self.load_layers)
        self.upload_e.clicked.connect(self.init_export_tree)
        self.search_button_i.clicked.connect(self.search_import)
        self.search_i.returnPressed.connect(self.search_import)
        self.search_button_e.clicked.connect(self.search_export)
        self.search_e.returnPressed.connect(self.search_export)
        self.help.clicked.connect(self.help_action)
        self.help_2.clicked.connect(self.help_action)
        self.home_url.clicked.connect(lambda :self.navigate_home_url())
        self.home_url_2.clicked.connect(lambda :self.navigate_home_url(export=True))
        self.shared_url.clicked.connect(lambda :self.navigate_shared_url())
        self.shared_url_2.clicked.connect(lambda :self.navigate_shared_url(export=True))

    def init_import_tab(self):

        """ Creates the tree view layout and appends a model to the tree """

        self.import_tree = self.import_tab
        self.import_tree.setColumnCount(3)
        self.get_info_i.setEnabled(False)
        self.import_tree.header().hideSection(3)
        self.import_tree.header().resizeSection(0,150)
        self.datastore_i.setText(self.root_path)
        self.addItems(self.import_tree,self.root_path,self.import_tree)
        self.current_store = self.root_path

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
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

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
        QApplication.restoreOverrideCursor() 
        return True

    def tab_changed(self):

        """ Restore tab to import on log in """

        if self.tabWidget.currentIndex() == 1:
            self.init_export_tab()

    def help_action(self):

        """ Open git page on a web browser """

        webbrowser.open_new_tab('https://github.com/BioComputing/irods-qgis')

    ## INITIALIZE EXPORT TAB FUNCTIONS



    def init_export_tab(self):

        """ initialize export tab on click """

        self.datastore_e.setEnabled(False)
        self.search_e.setEnabled(False)
        self.search_button_e.setEnabled(False)
        self.datastore_e.setText('')
        self.export_tree = self.export_tab
        self.export_tree.clear()
        self.export_tree.setColumnCount(0)
        self.export_tree.setHeaderLabel('Layer Name')
        self.addOpenLayers()
        self.upload_e.setText('Next')
        self.upload_e.setEnabled(False)
        self.logout_e.setText('Log Out')
        self.add_folder1.setEnabled(False)
        self.delete_3.setEnabled(False)
        self.home_url_2.setEnabled(False)
        self.shared_url_2.setEnabled(False)
        self.progressBar_2.hide()
        self.set_prog_bar_text('Select a layer to export',export=True)
        self.get_info_e.setEnabled(False)

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

        """ Display search results in the tree widget 

            parent : reference to the parent tree item
            path_list : list of items in the current tree (represented by datastore url)

        """
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

    def navigate_home_url(self,export=False):
        """ Navigate to home datastore url """

        if not export:
            self.get_info_i.setEnabled(False)
            self.change_datastore(self.root_path)
            self.datastore_i.setText(self.root_path)
        else:
            self.get_info_e.setEnabled(False)
            self.change_datastore_export_tree(self.root_path)
            self.datastore_e.setText(self.root_path)

    def navigate_shared_url(self,export=False):
        """ Navigate to shared datastore url """
        if not export:
            self.get_info_i.setEnabled(False)
            self.change_datastore("/iplant/home/shared")
            self.datastore_i.setText("/iplant/home/shared")
        else:
            self.get_info_e.setEnabled(False)
            self.change_datastore_export_tree("/iplant/home/shared")
            self.datastore_e.setText("/iplant/home/shared")

    def pre_change_datastore(self):
        """ setup before changing the import tree on return press"""
        if str(self.datastore_i.text())==self.root_path:
            self.get_info_i.setEnabled(False)
        self.change_datastore(self.datastore_i.text())


    def get_spatial_extension(self):
        """ Get spatial extension on of the selected file """
        ext = os.path.splitext(self.current_layer)[1][1:]
        list = ['shp','shx', 'dbf', 'prj', 'csv', 'tif', 'tiff','png','bmp','jpg','jpeg']
        if ext in list:
            if ext == 'shp' or ext== 'shx' or ext=='prj' or ext =='dbf':
                return 'Esri Shapefile'
            elif ext == 'csv':
                return 'Delimited Text Layer'
            else:
                return 'Raster Image Layer'

        return 'No Spatial File Selected'

    def set_prog_bar_text(self,text=None,spatial=None,export=False):
         """ Set progress bar label text for import and export tabs """
         if not export:
            if spatial:
                self.prog_label.setText('%s selected'%(spatial.title()))
            if text:
                self.prog_label.setText(text)
         if export :
            if spatial:
                self.prog_label2.setText('%s selected'%(spatial.title()))
            if text:
                self.prog_label2.setText(text)

    def addFolder(self,export=False):
        """ add folder to the selected location in user datastore """
        new_name = new_folder_name()
        val = new_name.file_name
        
        if self.current_store:
            try:
                if not export:
                    self.connection_object.collections.create('%s/%s'%(str(self.datastore_i.text()),val))
                else:
                    self.connection_object.collections.create('%s/%s'%(str(self.datastore_e.text()),val))
            except Exception, e:
                e = error('A folder with this name exists')
            else:         
                if not export:      
                    self.import_tree.clear()
                    self.change_datastore(self.datastore_i.text())
                else:
                    self.export_tree.clear()
                    self.change_datastore_export_tree(str(self.datastore_e.text()))

    def delFolder(self,export=False):
        """ delete folder from the selected location in user datastore """
        if not export:
            
            conf = del_conf(str(self.datastore_i.text()))
            selection = conf.selection
            if selection:
                if not str(self.datastore_i.text()) == self.root_path :
                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    try:
                        self.connection_object.collections.remove('%s'%(str(self.datastore_i.text())))
                    except:
                        QApplication.restoreOverrideCursor()
                        e = error('Error Occured. Try Again')
                    else:
                        QApplication.restoreOverrideCursor() 
                        self.datastore_i.setText(self.root_path)               
                        self.change_datastore(self.root_path)
                        
                else:
                    QApplication.restoreOverrideCursor()
                    e = error('Cannot delete root folder')
        else:
             conf = del_conf(str(self.datastore_e.text()))
             selection = conf.selection
             if selection: 
                if not str(self.datastore_e.text()) == self.root_path :
                    try:
                        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                        self.connection_object.collections.remove('%s'%(str(self.datastore_e.text())))
                    except E:
                        QApplication.restoreOverrideCursor()
                        e = error('Error Occured. Try Again')
                    else:
                        QApplication.restoreOverrideCursor()
                        self.datastore_e.setText(self.root_path)                    
                        self.change_datastore_export_tree(self.root_path)
                    
                else:
                        QApplication.restoreOverrideCursor()
                        e = error('Cannot delete root folder')
        

    def metadata(self,export=False):
        """ Get meta for the selected file """
        if not export:
            item = self.import_tree.itemFromIndex(self.current_index)
        else:
            item = self.export_tree.itemFromIndex(self.current_index)
        meta = []
        
        if item.text(1):
            coll = self.connection_object.data_objects.get(self.current_store)
            meta.append(coll.name)
            meta.append(coll.path)
            meta.append(self.get_file_size(coll.size))
            meta.append(str(coll.create_time))
            meta.append(str(coll.modify_time))
            ext = os.path.splitext(str(coll.path))[1][1:]
            if ext in content_types:
                meta.append(content_types[ext])
            else:
                meta.append('Unknown')
        else:
            coll = self.connection_object.collections.get(self.current_store)
            meta.append(coll.name)
            meta.append(coll.path)
            meta.append('N/A')
            meta.append('N/A')
            meta.append('N/A')
            meta.append('Directory')
        

        m = metadata(meta)
        m.show()
        result = m.exec_()

    def download_file(self,path,filestore):
        """ Download file which cannot be imported to qgis """
        filestore = str(filestore)
        path = str(path)
        fullpath = path+'/'+os.path.basename(filestore)
        source = self.get_source(filestore)
        file = open(fullpath,'w+')
        file.write(source)
        file.close()
        name  = os.path.basename(filestore)
        if len(name)>20:
            new_name = name[:5] + '...' +name[len(name)-9:-4] + name[-4:]
        else:
            new_name = name
        self.set_prog_bar_text('Downloaded \n %s'%(new_name))

    ## IMPORT EVENTS


    def enable_upload(self,index):
        """
        Enables import button after a FILE is clicked

        index : Index of the item selected

        """
        item = self.import_tree.itemFromIndex(index)
        self.get_info_i.setEnabled(True)
        if item.text(1):
            self.upload_i.setEnabled(True)
            self.current_index = index
            self.current_layer = str(item.text(0))
            get_ext = self.get_spatial_extension()
            if get_ext:
                self.set_prog_bar_text(spatial = get_ext)
            self.current_store = str(item.text(3))
            self.datastore_i.setText(item.text(3)[:-(len(self.current_layer)+1)])
        else:
            self.current_index = index
            self.current_store = str(item.text(3))
            self.upload_i.setEnabled(False)
            self.datastore_i.setText(item.text(3))

    def change_datastore(self, url=None):
        """
        Changes datastore after it is typed and return is pressed (for import tab)

        index : Index of the item selected

        """
        if not url:
            path = str(self.datastore_i.text())
        else:
            path = url
        self.import_tree.clear()
        if path == self.root_path:
            self.current_store = self.root_path
        if path:
            self.addItems(self.import_tree,path,self.import_tree)
        else:
            #self.addItems(self.import_tree,path,self.import_tree)
            self.addItems(self.import_tree,self.root_path,self.import_tree)

    def load_layers(self):

        """ 
        Calls all the functions involved with loading a selected layer from the irods datastore

        tree : Reference to the current QModelIndex object

        """
        #check file extension
        self.set_prog_bar_text('Starting import...')
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
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
            QApplication.restoreOverrideCursor()
            d = download(os.path.basename(self.current_layer))
            if not d.selection:
                return False
            else:
                self.download_file(d.name,self.current_store)
                return False
        self.set_prog_bar_text('Preparing to Download %s'%(filename))
        dirpath = tempfile.mkdtemp()
        if file_type:
            if not file_ext == 'csv':
                main_file_path = ''
                for ext in shp_ext:
                    file_path = dirpath+'/'+base_name+'.'+ext
                    if ext == 'shp':
                        main_file_path = file_path
                    file = open(file_path,'wb')
                    file_source = self.get_source(store[:-3]+ext)
                    if file_source:
                        file.write(file_source)
                        file.close()
                    else:
                        QApplication.restoreOverrideCursor()
                        e = error("File Not Found or Corrupted'")
                        return False
                self.load_vector_layer(main_file_path,base_name)
                self.set_prog_bar_text('%s loaded'%(filename))
            else:
                file_path = dirpath+'/'+filename
                file = open(file_path,'wb')
                file_source = self.get_source(store)
                if file_source:
                    file.write(file_source)
                    file.close()
                else:
                    QApplication.restoreOverrideCursor()
                    e = error("File Not Found or Corrupted'")
                    return False
                self.load_vector_layer(file_path,base_name,'delimitedtext')
                self.set_prog_bar_text('%s loaded'%(filename))
        else:
            file_path = dirpath+'/'+filename
            file = open(file_path, 'wb')
            file_source = self.get_source(store)
            if file_source:
                file.write(file_source)
                file.close()
            else:
                QApplication.restoreOverrideCursor()
                e = error("File Not Found or Corrupted'")
                return False
            self.load_raster_layer(file_path,base_name)
            self.set_prog_bar_text('%s loaded'%(filename))

    def search_import(self):
        """ Search for query in the current import tree items """
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
            self.datastore_i.setText(self.root_path)
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
        self.get_info_e.setEnabled(True)
        if not item.text(1):
            self.upload_e.setEnabled(True)
            self.current_index = index
            self.current_store = str(item.text(3))
            self.datastore_e.setText(item.text(3))
        else:
            self.current_index = index
            self.current_store = str(item.text(3))
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
            self.upload_e.setEnabled(True)
            self.logout_e.setText('Back')
            if not self.root_path == '/iplant/home/shared':
                self.add_folder1.setEnabled(True)
                self.delete_3.setEnabled(True)
            self.home_url_2.setEnabled(True)
            self.shared_url_2.setEnabled(True)
            self.progressBar_2.hide()
            self.get_info_e.setEnabled(False)
            size = len(self.current_layer)
            if (size>20):
                layer = self.current_layer[:5] + '...' +self.current_layer[size-9:-4] + self.current_layer[-4:] 
            else:
                layer= self.current_layer
            self.set_prog_bar_text("%s \nlayer selected\n (Choose a folder)"%(str(layer)),export=True)
            self.current_store = self.root_path

            ## export tree events | Disconnect them if clicked on back and vice versa

            self.export_tab.clicked.disconnect()
            self.export_tab.clicked.connect(self.enable_export)
            self.upload_e.clicked.disconnect()
            self.upload_e.clicked.connect(self.save)
            self.logout_e.clicked.disconnect()
            self.logout_e.clicked.connect(self.init_export_tab)

    def pre_change_datastore_export_tree(self):
        """ Function ofr setting up export tree change on return press """
        if str(self.datastore_e.text())==self.root_path:
            self.get_info_e.setEnabled(False)
        text = str(self.datastore_e.text())
        self.change_datastore_export_tree(text)

    def change_datastore_export_tree(self, url=None):
        """
        Changes datastore after it is typed and return is pressed (for export tab)

        index : Index of the item selected

        """
        if not url:
            path = str(self.datastore_e.text())
        else:
            path = url
        self.export_tree.clear()
        if path == self.root_path:
            self.current_store = self.root_path
        if path:
            self.addItems(self.export_tree,path,self.export_tree)
        else:
            self.addItems(self.export_tree,self.root_path,self.export_tree)


    def save(self):
        """ Save selected layer to chosen folder on export tab """

        QApplication.restoreOverrideCursor()
        self.set_prog_bar_text('Saving...',export=True)
        ext = self.current_layer[-3:]
        if ext == 'shp':
            self.save_shp()
        else:
            path = '%s/%s'%(self.current_store,self.current_layer)
            #Check if file exists in the folder
            try:
                coll = self.connection_object.data_objects.create(str(path))
            except:
                layer_created = False
                while(not layer_created):
                    r = replace()
                    selection = r.selection
                    # if user decides to change the name and create duplicate
                    if not selection :
                        new_name = new_file_name()
                        val = new_name.file_name
                        #create the file with new name
                        try:
                            obj = '%s/%s.%s'%(self.current_store,val,self.current_layer[-3:])
                            coll = self.connection_object.data_objects.create(str(obj))

                        except:
                            e = error('Layer with same name exists. Try again')
                        else:
                            layer_created = True
                    # If user decides to keep the same name for the layer
                    else:
                        try: 
                            coll = self.connection_object.data_objects.get(str(path))
                        except Exception as e:
                            e = error('%s. Try Again'%str(e))
                        else:
                            layer_created = True
            finally:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                file = open(str(self.sources[self.current_layer]),'rb')
                payload = file.read()
                file2 = coll.open('r+')
                file2.write('')
                file2.write(payload)
                file.close()
                file2.close()
                QApplication.restoreOverrideCursor()
                self.import_tree.clear()
                self.addItems(self.import_tree,self.root_path,self.import_tree)
    #            # Get back to Export tab 
                self.init_export_tab()

    def save_shp(self):
            """ Save selected shapefile in export tab"""

            exts = ['.shp','.prj','.shx','.dbf']
            path = '%s/%s'%(self.current_store,self.current_layer)  
            try:
                #see if the shp file exists
                coll = self.connection_object.data_objects.create(str(path))
            except:
                layer_created = False
                while(not layer_created):
                    r = replace()
                    selection = r.selection
                    # if user decides to change the name and create duplicate
                    if not selection :
                        new_name = new_file_name()
                        val = new_name.file_name
                        #create the file with new name
                        for ext in exts:
                            try:
                                obj = '%s/%s%s'%(self.current_store,val,ext)
                                coll = self.connection_object.data_objects.create(str(obj))

                            except:
                                layer_created = False
                                e = error('Layer with same name exists. Try again')
                            else:
                                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                                file = open(str(self.sources[self.current_layer][:-4]+ext),'rb')
                                payload = file.read()
                                file2 = coll.open('r+')
                                file2.write('')
                                file2.write(payload)
                                file.close()
                                file2.close()
                                QApplication.restoreOverrideCursor()
                                layer_created = True
                    # If user decides to keep the same name for the layer
                    else:
                        for ext in exts:
                            try: 
                                obj = '%s/%s%s'%(self.current_store,self.current_layer[:-4],ext)
                                coll = self.connection_object.data_objects.get(str(obj))
                            except Exception as e:
                                layer_created = False
                                e = error('%s. Try Again'%str(e))
                            else:
                                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                                file = open(str(self.sources[self.current_layer][:-4]+ext),'rb')
                                payload = file.read()
                                file2 = coll.open('r+')
                                file2.write(payload)
                                file.close()
                                file2.close()
                                QApplication.restoreOverrideCursor()
                                layer_created = True
            else:
                exts = ['.prj','.shx','.dbf']
                QApplication.restoreOverrideCursor()
                self.set_prog_bar_text('Saving...',export=True)
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                # create the shp file before creating other 3
                file = open(str(self.sources[self.current_layer][:-4]+'.shp'),'rb')
                payload = file.read()
                file2 = coll.open('r+')
                file2.write('')
                file2.write(payload)
                file.close()
                file2.close()
                QApplication.restoreOverrideCursor()
                for ext in exts:
                            try:
                                obj = '%s/%s%s'%(self.current_store,self.current_layer[:-4],ext)
                                coll = self.connection_object.data_objects.create(str(obj))

                            except:
                                layer_created = False
                                e = error('Layer with same name exists. Try again')
                            else:
                                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                                file = open(str(self.sources[self.current_layer][:-4]+ext),'rb')
                                payload = file.read()
                                file2 = coll.open('r+')
                                file2.write('')
                                file2.write(payload)
                                file.close()
                                file2.close()
                                QApplication.restoreOverrideCursor()
                                layer_created = True
            finally:
                self.import_tree.clear()
                self.addItems(self.import_tree,self.root_path,self.import_tree)
    #            # Get back to Export tab 
                self.init_export_tab()



    def search_export(self):
        """ Search for query in current export tree """

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
            self.datastore_e.setText(self.root_path)
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
            file_size = int(source.size)
            file = source.open() #consider this line again
        except:
            return False
            #print 'ERROR: File Not Found'
        else:
            payload = ''
            a = ''
            self.prog_label.hide()
            self.progressBar.show()
            for r,row in enumerate(file.read()):
                if r==1:
                    QApplication.restoreOverrideCursor()
                progress = (r/float(source.size))*100.00
                self.update_timer(int(progress))
                payload += row
            self.update_timer(100)
            file.close()
            self.restart_timer()
            return payload


        file = open()
        QgsMapLayerRegistry.instance().addMapLayer()


    def update_timer(self, val):
        """ Mandatory timer event function for progress bar """
        
        self.step = val
        self.progressBar.setValue(self.step)

    def restart_timer(self):
        """ Mandatory timer event function for progress bar"""
        
        self.progressBar.reset()
        self.progressBar.hide()
        self.prog_label.show()
        self.prog_label.setText('Download Complete. Loading Layer...')


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





   