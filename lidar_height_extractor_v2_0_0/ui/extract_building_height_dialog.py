# -*- coding: utf-8 -*-
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import QgsProject

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), '../forms/extract_building_height_dialog_base.ui'))

class ExtractBuildingHeightDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(ExtractBuildingHeightDialog, self).__init__(parent)
        self.setupUi(self)
