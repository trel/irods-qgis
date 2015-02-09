# -*- coding: utf-8 -*-
"""
/***************************************************************************
 irods_qgis
                                 A QGIS plugin
 Connect to irods via qgis
                             -------------------
        begin                : 2014-12-23
        copyright            : (C) 2014 by Amit Juneja / BCF
        email                : amitj@email.arizona
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load irods_qgis class from file irods_qgis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .irods_qgis import irods_qgis
    return irods_qgis(iface)
