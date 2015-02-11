# irods-qgis
Plugin for a popular open source GIS platform called QGIS (http://www.qgis.org/).  The plugin allows one to:  
	- Connect to any iRODS (open source http://www.irods.org) datastore directly from QGIS.  
	- Import a spatial file from irods datastore to open map canvas on QGIS.  
	- Save a layer from the map canvas on QGIS to your iRODS datastore as a spatial file.

# Supported Formats

Vector : 
 - Shapefiles (.shp)
 - CSV (.csv)

Raster : 
 - jpeg
 - gif
 - png
 - GeoTiff (.tif)
 - bmp

*Note : At the moment only basic vector and raster data are supported. More support for other formats will be added soon

# System Requirements

##### Windows (8 or older)

- Qgis 2.4 (Chugiak) or older
	
* The plugin is not compatible with Qgis 2.6.1 (Brighton) on Windows
	
##### Mac OSX (10.10.2 or older)

- Qgis 2.6.1 (Brighton) or older
	
##### Linux (Ubuntu 14.04 or older)

- Qgis 2.6.1 (Brigton) or older

# Installation

	To install the plugin, clone the repository 
	
	-- git clone https://github.com/BioComputing/irods-qgis.git --


# Bug Tracker

https://github.com/BioComputing/irods-qgis/issues

# Credit

The plugin is funded by DataNet Federation Consortium (http://datafed.org/) supported by the National Science Foundation under Grant Number OCI 0940841 and developed by Amit Juneja at the University of Arizona

A special thanks to Iplant Collaborative (http://www.iplantcollaborative.org/) and python-irodsclient (https://github.com/iPlantCollaborativeOpenSource/python-irodsclient) team

# License

GNU GPL. Read more on https://github.com/BioComputing/irods-qgis/blob/master/LICENSE.md



