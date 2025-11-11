# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider
from .algorithms.extract_building_height import ExtractBuildingHeightAlgorithm

class LidarProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(ExtractBuildingHeightAlgorithm())

    def id(self): return 'lidar'
    def name(self): return 'LiDAR'
    def longName(self): return 'Procesos LiDAR'
