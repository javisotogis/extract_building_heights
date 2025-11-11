# -*- coding: utf-8 -*-
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QProgressDialog, QMessageBox
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.core import QgsProject, QgsMapLayerType, QgsProcessingFeedback, QgsMessageLog, Qgis
import processing

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), '../forms/extract_building_height_dialog_base.ui'))

class ProgressFeedback(QgsProcessingFeedback):
    def __init__(self, progress_dialog):
        super().__init__()
        self.dlg = progress_dialog
    def setProgress(self, progress):
        try:
            self.dlg.setValue(int(progress))
        except Exception:
            pass
    def pushInfo(self, info):
        QgsMessageLog.logMessage(info, 'ExtractBuildingHeight', Qgis.Info)
    def pushWarning(self, info):
        QgsMessageLog.logMessage(info, 'ExtractBuildingHeight', Qgis.Warning)
    def pushDebugInfo(self, info):
        QgsMessageLog.logMessage(info, 'ExtractBuildingHeight', Qgis.Info)

class ExtractBuildingHeightDialog(QDialog, FORM_CLASS):
    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.setupUi(self)
        self.populate()
        self.buttonBox.accepted.connect(self.run_tool)
        self.btnOpenLog.setEnabled(False)
        self.btnOpenLog.clicked.connect(self.open_log)
        self._last_log = None

    def populate(self):
        self.cmbBuildings.clear()
        self.cmbPointCloud.clear()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.type() == QgsMapLayerType.VectorLayer and getattr(lyr, 'geometryType', lambda: -1)() == 2:
                self.cmbBuildings.addItem(lyr.name(), lyr.id())
            if lyr.type() == QgsMapLayerType.PointCloudLayer:
                self.cmbPointCloud.addItem(lyr.name(), lyr.id())

    def selectedLayer(self, combo):
        lid = combo.currentData()
        return QgsProject.instance().mapLayer(lid)

    def run_tool(self):
        buildings = self.selectedLayer(self.cmbBuildings)
        pcl = self.selectedLayer(self.cmbPointCloud)
        ground_expr = self.leGroundExpr.text().strip() or 'Classification = 2'
        res = float(self.spRes.value())
        tile = int(self.spTile.value())

        params = {
            'buildings': buildings,
            'ground_filter_ie_classification__2': ground_expr,
            'point_cloud': pcl,
            'resolution': res,
            'tile_size': tile,
            'Buildings_with_heights': 'memory:'
        }

        progress = QProgressDialog('Ejecutando ExtractBuildingHeight…', 'Cancelar', 0, 100, self)
        progress.setWindowModality(True)
        progress.show()
        feedback = ProgressFeedback(progress)

        try:
            res = processing.run('lidar:ExtractBuildingHeight', params, feedback=feedback)
            if isinstance(res, dict):
                if 'Buildings_with_heights' in res:
                    self.iface.addVectorLayer(res['Buildings_with_heights'], 'building_height', 'ogr')
                if 'log_file' in res and res['log_file'] and os.path.exists(res['log_file']):
                    self._last_log = res['log_file']
                    self.btnOpenLog.setEnabled(True)
                    QgsMessageLog.logMessage(f"Log guardado en: {res['log_file']}", 'ExtractBuildingHeight', Qgis.Info)
        finally:
            progress.reset()

    def open_log(self):
        if self._last_log and os.path.exists(self._last_log):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self._last_log))
        else:
            QMessageBox.information(self, 'ExtractBuildingHeight', 'No hay log disponible todavía. Ejecuta el proceso primero.')
