# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoAdminSearch
                                 A QGIS plugin
 Sogis Suche Plugin
                             -------------------
        begin                : 2014-03-09
        copyright            : (C) 2014 by Stefan Ziegler 
        email                : stefan.ziegler.de@gmail.com
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


def name():
    return "GeoAdmin Search"

def description():
    return "GeoAdmin Search Plugin"

def version():
    return "Version 0.1"

def icon():
    return "icon.png"

def qgisMinimumVersion():
    return "2.4"

def author():
    return "Stefan Ziegler"

def email():
    return "stefan.ziegler.de@gmail.com"

def classFactory(iface):
    from geoadminsearch import GeoAdminSearch
    return GeoAdminSearch(iface)
