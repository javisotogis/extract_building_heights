# -*- coding: utf-8 -*-
from .extract_building_height_plugin import ExtractBuildingHeightPlugin
def classFactory(iface):
    return ExtractBuildingHeightPlugin(iface)
