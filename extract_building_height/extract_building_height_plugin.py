# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsApplication
from .provider import LidarProvider
from .ui.extract_building_height_dialog import ExtractBuildingHeightDialog

class ExtractBuildingHeightPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.action = None

    def tr(self, message):
        return QCoreApplication.translate('ExtractBuildingHeight', message)

    def initGui(self):
        self.provider = LidarProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        self.action = QAction(QIcon(':/plugins/extract_building_height/icon.svg'),
                              self.tr('Extraer altura de edificios (ventana)…'), self.iface.mainWindow())
        self.action.triggered.connect(self.open_dialog)
        self.iface.addPluginToMenu(self.tr('&ExtractBuildingHeight'), self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
        if self.action:
            self.iface.removePluginMenu(self.tr('&ExtractBuildingHeight'), self.action)
            self.iface.removeToolBarIcon(self.action)

    def open_dialog(self):
        dlg = ExtractBuildingHeightDialog(self.iface)
        dlg.exec_()
