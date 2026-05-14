# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import QgsApplication
from .provider import LidarProvider
import processing

class LiDARHeightExtractorPlugin:
    ALGORITHM_ID = 'lidar_height_extractor_v2:LiDARHeightExtractor'

    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.action = None

    def tr(self, message):
        return QCoreApplication.translate('LiDARHeightExtractor', message)

    def initGui(self):
        self.provider = LidarProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        icon_path = os.path.join(os.path.dirname(__file__), 'icon.svg')
        self.action = QAction(QIcon(icon_path),
                              self.tr('LiDAR Height Extractor - v2.0.4'), self.iface.mainWindow())
        self.action.triggered.connect(self.open_dialog)
        self.iface.addPluginToMenu(self.tr('&LiDARHeightExtractor'), self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
        if self.action:
            self.iface.removePluginMenu(self.tr('&LiDARHeightExtractor'), self.action)
            self.iface.removeToolBarIcon(self.action)

    def open_dialog(self):
        registry = QgsApplication.processingRegistry()
        if not registry.algorithmById(self.ALGORITHM_ID):
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr('LiDAR Height Extractor'),
                self.tr('The LiDAR Height Extractor processing algorithm is not available.')
            )
            return

        if hasattr(self.iface, 'openProcessingAlgorithmDialog'):
            self.iface.openProcessingAlgorithmDialog(self.ALGORITHM_ID)
            return

        processing.execAlgorithmDialog(self.ALGORITHM_ID, {})
