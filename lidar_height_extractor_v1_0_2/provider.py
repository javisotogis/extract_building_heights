# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from .algorithms.extract_building_height import LiDARHeightExtractorAlgorithm

class LidarProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(LiDARHeightExtractorAlgorithm())

    def id(self): return 'lidar_height_extractor_v2'
    def name(self): return 'LiDAR Height Extractor'
    def longName(self): return 'LiDAR Height Extractor (v2.0.4)'
