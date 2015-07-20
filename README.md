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

*Note : At the moment only basic vector and raster data are supported. More support for other formats will be added soon*

# System Requirements

##### Windows (8 or older)

- Qgis 2.8.2 (Wien) or older
	
##### Mac OSX (10.10.2 or older)

- Qgis 2.8.2 (Wien) or older
	
##### Linux (Ubuntu 14.04 or older)

- Qgis 2.8.2 (Wien) or older

# Installation
#### Step 1

To install the plugin, clone the repository 
	
	git clone https://github.com/BioComputing/irods-qgis.git
	
#### Step 2

##### Windows
	
	Place the folder in C://Users/<username>/.qgis2/python/plugins
	
##### Mac OSX
	
	Place the folder in /Users/<username>/.qgis2/python/plugins
	
##### Linux
	
	Place the folder in /<username>/.qgis2/python/plugins
	
	
*Note : If __python__ folder does not exist, create the folder*
	
#### Step 3

Select 'Manage Python Plugins' option under Plugins menu in Qgis

!["Image N/A"] (img/img1.png)

#### Step 4

Search for the plugin in 'All' plugins, and check the box next to **iRods** to enable the plugin
		
!["Image N/A"] (img/img2.png)

*Note: Plugin will be available on the plugin toolbar and under plugins menu after it is enabled*

# Bug Tracker

https://github.com/BioComputing/irods-qgis/issues

# Credit

The plugin is funded by DataNet Federation Consortium (http://datafed.org/) supported by the National Science Foundation under Grant Number OCI 0940841 and developed by Amit Juneja at the University of Arizona

A special thanks to Iplant Collaborative (http://www.iplantcollaborative.org/) and python-irodsclient (https://github.com/iPlantCollaborativeOpenSource/python-irodsclient) team

# License

GNU GPL. Read more on https://github.com/BioComputing/irods-qgis/blob/master/LICENSE.md


function mvn = q(y)
	mu = [0,0]
	sigma = [0.5,0.3;0.4,2.0]
	X = linspace(-10,10)
	y = zeros(1,100)
	Xy = [X(:),y(:)]
	mvn = mvnpdf(Xy,mu,sigma);
endfunction



