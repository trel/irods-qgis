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

#from irods_qgis import irods_qgis
from irods.session import iRODSSession
from irods.exception import CAT_INVALID_AUTHENTICATION
from helpers.tab_layout import tab_dialog
from helpers.error import error
from helpers.check_network import internet_on

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'irods_qgis_dialog_base.ui'))


class irods_qgisDialog(QtGui.QDialog, FORM_CLASS):

    creds = []
    sess = ''

    def __init__(self,parent=None):
        """Constructor."""
        super(irods_qgisDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def get_sess(self):
        return self.sess

    def return_values(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        port = self.portLineEdit.text()
        host = self.hostLineEdit.text()
        zone = self.zoneLineEdit.text()
        self.creds = [username,password,port,host,zone]

    def accept(self):
        # Do something useful here - delete the line containing pass and
            # substitute with your code.
            self.return_values()
            sess_credentials =  self.creds
            username = str(sess_credentials[0])
            password = str(sess_credentials[1])
            port = str(sess_credentials[2])
            host = str(sess_credentials[3])
            zone = str(sess_credentials[4])
            datastore = "/%s/home/%s"%(zone,username)
            print username, password, port, host, zone, datastore
            try:
                self.sess = iRODSSession(host=host, port=port, user=username, password=password, zone=zone)
                coll = self.sess.collections.get(datastore)

            except Exception as e:
                print e
                self.sess = ''
                if e == CAT_INVALID_AUTHENTICATION:
                    e = error("Log In Failed")
                else:

                    if internet_on():
                        e = error("Log In Failed")
                    else:
                     e = error("Network Error. Check Your Connection")

            else:
                creds = {"datastore":datastore, "sess":self.sess}
                self.dlg2 = tab_dialog()
                Dialog = QtGui.QDialog()
                self.dlg2.setupUi(Dialog, creds)
                self.setVisible(False)
                Dialog.show()
                result2 = Dialog.exec_()
                if self.dlg2.logout_var:
                    self.sess = ''
                    self.setVisible(True)


