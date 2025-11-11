# -*- coding: utf-8 -*-
import os, tempfile, datetime, logging
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterPointCloudLayer,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
)
import processing

class ExtractBuildingHeightAlgorithm(QgsProcessingAlgorithm):
    PARAM_BUILDINGS = 'buildings'
    PARAM_GROUND_EXPR = 'ground_filter_ie_classification__2'
    PARAM_POINTCLOUD = 'point_cloud'
    PARAM_RES = 'resolution'
    PARAM_TILE = 'tile_size'
    PARAM_OUT = 'Buildings_with_heights'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.PARAM_BUILDINGS, 'Buildings', types=[QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterExpression(
            self.PARAM_GROUND_EXPR,
            'Ground filter. i.e.: "Classification = 2"',
            parentLayerParameterName=self.PARAM_POINTCLOUD,
            defaultValue='Classification = 2',
            type=Qgis.ExpressionType.PointCloud
        ))
        self.addParameter(QgsProcessingParameterPointCloudLayer(
            self.PARAM_POINTCLOUD, 'Point Cloud'))
        self.addParameter(QgsProcessingParameterNumber(
            self.PARAM_RES, 'Raster resolution (m)',
            type=QgsProcessingParameterNumber.Double, defaultValue=1.0, minValue=0.05))
        self.addParameter(QgsProcessingParameterNumber(
            self.PARAM_TILE, 'Tile size (px)',
            type=QgsProcessingParameterNumber.Integer, defaultValue=1000, minValue=100))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.PARAM_OUT, 'Buildings_with_heights',
            type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True))

    def shortHelpString(self):
        return ('<b>ExtractBuildingHeight</b><br/>'
                'DEM (todos los puntos) + DTM (filtro de suelo) → nDSM = DEM − DTM → Máximo por edificio + campo redondeado.<br/>'
                '<b>Parámetros:</b> Buildings, Ground filter, Point Cloud, <i>Raster resolution</i>, <i>Tile size</i>.')

    def processAlgorithm(self, parameters, context, model_feedback):
        res = float(parameters[self.PARAM_RES])
        tile = int(parameters[self.PARAM_TILE])

        log_path = os.path.join(tempfile.gettempdir(), f"extract_building_height_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logger = logging.getLogger('ExtractBuildingHeight')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        if not any(isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', '') == fh.baseFilename for h in logger.handlers):
            logger.addHandler(fh)

        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results, outputs = {}, {}

        logger.info('Paso 0: DEM (pdal:exportrastertin)')
        alg_params = {'FILTER_EXPRESSION': None,'FILTER_EXTENT': None,'INPUT': parameters[self.PARAM_POINTCLOUD],
                      'ORIGIN_X': None,'ORIGIN_Y': None,'RESOLUTION': res,'TILE_SIZE': tile,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
        outputs['dem'] = processing.run('pdal:exportrastertin', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1);  logger.info('Paso 1: DTM con filtro suelo')
        if feedback.isCanceled(): return {}
        alg_params = {'FILTER_EXPRESSION': parameters[self.PARAM_GROUND_EXPR],'FILTER_EXTENT': None,'INPUT': parameters[self.PARAM_POINTCLOUD],
                      'ORIGIN_X': None,'ORIGIN_Y': None,'RESOLUTION': res,'TILE_SIZE': tile,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
        outputs['dtm'] = processing.run('pdal:exportrastertin', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2);  logger.info('Paso 2: nDSM = DEM - DTM (qgis:rastercalculator)')
        if feedback.isCanceled(): return {}
        alg_params = {'EXPRESSION': 'B - A','LAYERS': [outputs['dtm']['OUTPUT'], outputs['dem']['OUTPUT']],
                      'CELLSIZE': 0,'EXTENT': None,'CRS': None,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
        outputs['ndsm'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3); logger.info('Paso 3: Estadística zonal (máximo)')
        if feedback.isCanceled(): return {}
        alg_params = {'COLUMN_PREFIX': 'height','INPUT': parameters[self.PARAM_BUILDINGS],'INPUT_RASTER': outputs['ndsm']['OUTPUT'],
                      'RASTER_BAND': 1,'STATISTICS': [6],'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
        outputs['zonal'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4); logger.info('Paso 4: Redondeo (field calculator)')
        if feedback.isCanceled(): return {}
        expr = 'round("height_max", 2)'
        alg_params = {'FIELD_LENGTH': 0,'FIELD_NAME': 'height_rounded','FIELD_PRECISION': 2,'FIELD_TYPE': 0,
                      'FORMULA': expr,'INPUT': outputs['zonal']['OUTPUT'],'OUTPUT': parameters[self.PARAM_OUT]}
        out = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        logger.info('Hecho. Log: %s', log_path)
        results[self.PARAM_OUT] = out['OUTPUT'];  results['log_file'] = log_path
        return results

    def name(self): return 'ExtractBuildingHeight'
    def displayName(self): return 'ExtractBuildingHeight'
    def group(self): return 'lidar'
    def groupId(self): return 'lidar'
    def createInstance(self): return ExtractBuildingHeightAlgorithm()
