# -*- coding: utf-8 -*-
from .lidar_height_extractor_plugin import LiDARHeightExtractorPlugin

def classFactory(iface):
    return LiDARHeightExtractorPlugin(iface)
