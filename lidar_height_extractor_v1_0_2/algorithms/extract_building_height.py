# -*- coding: utf-8 -*-
import os, tempfile, datetime, logging
from osgeo import gdal, osr
import numpy as np
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterPointCloudLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterCrs,
    QgsCoordinateReferenceSystem,
    QgsProcessingOutputLayerDefinition,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsVectorFileWriter,
)
from qgis.PyQt.QtCore import QVariant
import processing

class LiDARHeightExtractorAlgorithm(QgsProcessingAlgorithm):
    PARAM_POLYGON = 'polygon_layer'
    PARAM_POINTCLOUD = 'point_cloud'
    PARAM_DEM_EXPR = 'dem_filter_expression'
    PARAM_GROUND_EXPR = 'ground_filter_ie_classification__2'
    PARAM_RES = 'resolution'
    PARAM_TILE = 'tile_size'
    PARAM_TARGET_CRS = 'target_crs'
    PARAM_OUTPUT_POLY = 'output_polygons'

    def initAlgorithm(self, config=None):
        # Move polygon to top and rename param
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.PARAM_POLYGON, 'Polygon layer', types=[QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterPointCloudLayer(
            self.PARAM_POINTCLOUD, 'Point Cloud'))
        self.addParameter(QgsProcessingParameterExpression(
            self.PARAM_DEM_EXPR,
            'DEM filter expression (optional, e.g.: "Classification != 7" to exclude noise)',
            parentLayerParameterName=self.PARAM_POINTCLOUD,
            defaultValue='',
            optional=True,
            type=Qgis.ExpressionType.PointCloud
        ))
        self.addParameter(QgsProcessingParameterExpression(
            self.PARAM_GROUND_EXPR,
            'Ground filter for DTM. i.e.: "Classification = 2"',
            parentLayerParameterName=self.PARAM_POINTCLOUD,
            defaultValue='Classification = 2',
            type=Qgis.ExpressionType.PointCloud
        ))
        self.addParameter(QgsProcessingParameterNumber(
            self.PARAM_RES, 'Raster resolution (m)',
            type=QgsProcessingParameterNumber.Double, defaultValue=1.0, minValue=0.05))
        self.addParameter(QgsProcessingParameterNumber(
            self.PARAM_TILE, 'Tile size (px)',
            type=QgsProcessingParameterNumber.Integer, defaultValue=1000, minValue=100))
        self.addParameter(QgsProcessingParameterCrs(
            self.PARAM_TARGET_CRS, 'Target CRS (optional)', optional=True))
        self.addParameter(QgsProcessingParameterVectorDestination(
            self.PARAM_OUTPUT_POLY, 'Output polygons with lidar_height'))

    def shortHelpString(self):
        return ('LiDARHeightExtractor: compute nDSM using custom point cloud filters and extract max height per polygon (buildings, trees, ...).')

    def _crs_to_authid(self, crs_val):
        try:
            if isinstance(crs_val, QgsCoordinateReferenceSystem):
                return crs_val.authid()
            return str(crs_val)
        except Exception:
            return None

    def _wkt_to_authid(self, wkt):
        try:
            s = osr.SpatialReference()
            s.ImportFromWkt(wkt)
            code = s.GetAuthorityCode(None)
            auth = s.GetAuthorityName(None)
            if code and auth:
                return f"{auth}:{code}"
            return None
        except Exception:
            return None

    def _extract_output_path(self, output_def):
        if isinstance(output_def, QgsProcessingOutputLayerDefinition):
            return output_def.sink.staticValue()
        return str(output_def)

    def processAlgorithm(self, parameters, context, model_feedback):
        polygon_layer_id = parameters[self.PARAM_POLYGON]
        res = float(parameters[self.PARAM_RES])
        tile = int(parameters[self.PARAM_TILE])
        target_crs_param = parameters.get(self.PARAM_TARGET_CRS, None)
        output_poly_raw = parameters[self.PARAM_OUTPUT_POLY]
        output_poly = self._extract_output_path(output_poly_raw)

        log_path = os.path.join(tempfile.gettempdir(), f"lidar_height_extractor_v1_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logger = logging.getLogger('LiDARHeightExtractor_v1')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        if not any(isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', '') == fh.baseFilename for h in logger.handlers):
            logger.addHandler(fh)

        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results, outputs = {}, {}
        resampled_tmp = None
        ndsm_tmp = None

        try:
            logger.info('Paso 0: DEM (pdal:exportrastertin - all points)')
            alg_params = {'FILTER_EXPRESSION': parameters[self.PARAM_DEM_EXPR] if parameters.get(self.PARAM_DEM_EXPR) else None,'FILTER_EXTENT': None,'INPUT': parameters[self.PARAM_POINTCLOUD],
                          'ORIGIN_X': None,'ORIGIN_Y': None,'RESOLUTION': res,'TILE_SIZE': tile,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
            outputs['dem'] = processing.run('pdal:exportrastertin', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            dem_path = outputs['dem']['OUTPUT']
            logger.info(f'DEM generado: {dem_path}')

            feedback.setCurrentStep(1);  logger.info('Paso 1: DTM (pdal:exportrastertin - ground filtered)')
            if feedback.isCanceled(): return {}
            alg_params = {'FILTER_EXPRESSION': parameters[self.PARAM_GROUND_EXPR],'FILTER_EXTENT': None,'INPUT': parameters[self.PARAM_POINTCLOUD],
                          'ORIGIN_X': None,'ORIGIN_Y': None,'RESOLUTION': res,'TILE_SIZE': tile,'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT}
            outputs['dtm'] = processing.run('pdal:exportrastertin', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            dtm_path = outputs['dtm']['OUTPUT']
            logger.info(f'DTM generado: {dtm_path}')

            feedback.setCurrentStep(2); logger.info('Paso 2: nDSM = DEM - DTM (NumPy/GDAL directo)')
            if feedback.isCanceled(): return {}
            
            # Open rasters with GDAL
            dem_ds = gdal.Open(dem_path)
            dtm_ds = gdal.Open(dtm_path)
            
            if not dem_ds or not dtm_ds:
                raise Exception("Error al abrir los rásteres DEM o DTM con GDAL")
            
            dem_band = dem_ds.GetRasterBand(1)
            dem_gt = dem_ds.GetGeoTransform()
            dem_proj = dem_ds.GetProjection()
            dem_xsize = dem_ds.RasterXSize
            dem_ysize = dem_ds.RasterYSize
            dtm_xsize = dtm_ds.RasterXSize
            dtm_ysize = dtm_ds.RasterYSize

            # Resample DTM if necessary
            need_resample = (dem_xsize != dtm_xsize) or (dem_ysize != dtm_ysize) or (dem_ds.GetGeoTransform() != dtm_ds.GetGeoTransform())

            if need_resample:
                logger.info('Rásteres con diferente tamaño/transform — re-muestreando DTM a rejilla DEM')
                resampled_dtm = os.path.join(tempfile.gettempdir(), f"dtm_resampled_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tif")
                resampled_tmp = resampled_dtm

                dem_minx = dem_gt[0]
                dem_maxy = dem_gt[3]
                dem_maxx = dem_minx + dem_gt[1] * dem_xsize
                dem_miny = dem_maxy + dem_gt[5] * dem_ysize

                dst_srs = None
                if target_crs_param:
                    dst_srs = self._crs_to_authid(target_crs_param)
                    logger.info(f'Usuario solicitó CRS destino: {dst_srs}')

                if not dst_srs and dem_proj:
                    try_auth = self._wkt_to_authid(dem_proj)
                    if try_auth:
                        dst_srs = try_auth
                        logger.info(f'Usando DEM CRS authid detectado: {dst_srs}')
                    else:
                        dst_srs = dem_proj

                warp_kwargs = dict(format='GTiff', outputBounds=(dem_minx, dem_miny, dem_maxx, dem_maxy),
                                   xRes=dem_gt[1], yRes=abs(dem_gt[5]), width=dem_xsize, height=dem_ysize,
                                   resampleAlg=gdal.GRA_Bilinear)
                if dst_srs:
                    warp_kwargs['dstSRS'] = dst_srs

                warp_opts = gdal.WarpOptions(**warp_kwargs)
                gdal.Warp(resampled_dtm, dtm_path, options=warp_opts)

                dtm_ds = None
                dtm_path = resampled_dtm
                dtm_ds = gdal.Open(dtm_path)

            dtm_band = dtm_ds.GetRasterBand(1)

            # Read and compute nDSM
            dem_data = dem_band.ReadAsArray().astype(np.float32)
            dtm_data = dtm_band.ReadAsArray().astype(np.float32)
            logger.info(f'DEM shape: {dem_data.shape}, DTM shape: {dtm_data.shape}')

            ndsm_data = dem_data - dtm_data
            
            # Create temporary nDSM raster
            ndsm_tmp = os.path.join(tempfile.gettempdir(), f"ndsm_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tif")
            driver = gdal.GetDriverByName('GTiff')
            ndsm_ds = driver.Create(ndsm_tmp, dem_ds.RasterXSize, dem_ds.RasterYSize, 1, gdal.GDT_Float32)
            ndsm_ds.SetGeoTransform(dem_ds.GetGeoTransform())
            ndsm_ds.SetProjection(dem_ds.GetProjection())
            ndsm_band = ndsm_ds.GetRasterBand(1)
            ndsm_band.WriteArray(ndsm_data)
            ndsm_band.FlushCache()
            
            dem_ds = None
            dtm_ds = None
            ndsm_ds = None
            
            logger.info(f'nDSM temporal guardado en: {ndsm_tmp}')

            # Paso 3: Zonal statistics
            feedback.setCurrentStep(3); logger.info('Paso 3: Calculando estadísticas zonales (max nDSM por polígono)')
            if feedback.isCanceled(): return {}

            # Load polygon layer
            polygon_layer = context.getMapLayer(polygon_layer_id)
            if not polygon_layer:
                raise Exception(f"No se pudo cargar la capa de polígonos: {polygon_layer_id}")

            logger.info(f'Capa de polígonos cargada: {polygon_layer.name()} con {polygon_layer.featureCount()} features')

            # Create output layer by copying input
            out_provider_name = polygon_layer.dataProvider().name()
            output_layer = QgsVectorLayer(polygon_layer.source(), 'polygons_with_height', out_provider_name)
            
            # Add lidar_height field if not exists
            field_index = output_layer.fields().indexFromName('lidar_height')
            if field_index == -1:
                output_layer.startEditing()
                output_layer.addAttribute(QgsField('lidar_height', QVariant.Double))
                output_layer.commitChanges()

            # Open nDSM raster
            ndsm_raster_ds = gdal.Open(ndsm_tmp)
            if not ndsm_raster_ds:
                raise Exception(f"No se pudo abrir raster nDSM: {ndsm_tmp}")

            ndsm_band = ndsm_raster_ds.GetRasterBand(1)
            ndsm_data_read = ndsm_band.ReadAsArray().astype(np.float32)
            ndsm_gt = ndsm_raster_ds.GetGeoTransform()

            logger.info(f'Raster nDSM cargado: shape {ndsm_data_read.shape}, geotransform {ndsm_gt}')

            # Calculate max nDSM for each polygon
            output_layer.startEditing()
            lidar_height_idx = output_layer.fields().indexFromName('lidar_height')

            logger.info(f'Iniciando cálculo de máximos por polígono. Total features: {output_layer.featureCount()}')
            feature_count = 0
            
            for feature in output_layer.getFeatures():
                feature_count += 1
                if feature_count % 100 == 0:
                    logger.info(f'Procesados {feature_count} polígonos...')
                
                geom = feature.geometry()
                
                # Get polygon bounds
                bbox = geom.boundingBox()
                xmin, xmax, ymin, ymax = bbox.xMinimum(), bbox.xMaximum(), bbox.yMinimum(), bbox.yMaximum()

                # Convert coords to raster indices
                col_min = int((xmin - ndsm_gt[0]) / ndsm_gt[1])
                col_max = int((xmax - ndsm_gt[0]) / ndsm_gt[1]) + 1
                row_min = int((ymax - ndsm_gt[3]) / ndsm_gt[5])
                row_max = int((ymin - ndsm_gt[3]) / ndsm_gt[5]) + 1

                # Clamp to raster bounds
                col_min = max(0, min(col_min, ndsm_data_read.shape[1] - 1))
                col_max = max(0, min(col_max, ndsm_data_read.shape[1]))
                row_min = max(0, min(row_min, ndsm_data_read.shape[0] - 1))
                row_max = max(0, min(row_max, ndsm_data_read.shape[0]))

                # Extract raster subset within bounds
                if col_max <= col_min or row_max <= row_min:
                    logger.warning(f'Feature {feature.id()} tiene bounds fuera del raster')
                    output_layer.changeAttributeValue(feature.id(), lidar_height_idx, 0.0)
                    continue

                raster_subset = ndsm_data_read[row_min:row_max, col_min:col_max]

                # Calculate max (ignore NaN and negative values - ground classification)
                mask = (raster_subset > 0.0) & (~np.isnan(raster_subset))
                if mask.any():
                    max_val = float(np.max(raster_subset[mask]))
                else:
                    max_val = 0.0

                # Round to 2 decimals
                max_val_rounded = round(max_val, 2)

                # Update feature
                output_layer.changeAttributeValue(feature.id(), lidar_height_idx, max_val_rounded)

            output_layer.commitChanges()
            ndsm_raster_ds = None

            logger.info(f'Estadísticas zonales completadas. Total features procesados: {feature_count}')

            logger.info(f'Guardando capa de polígonos en: {output_poly}')
            
            # Determine output path
            if not output_poly or 'memory:' in str(output_poly) or 'TEMPORARY_OUTPUT' in str(output_poly):
                output_poly = os.path.join(tempfile.gettempdir(), f"polygons_lidar_height_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.gpkg")
                logger.info(f'Output remapped a archivo temporal: {output_poly}')

            # Export output layer using QgsVectorFileWriter
            error, error_msg = QgsVectorFileWriter.writeAsVectorFormatV2(
                output_layer,
                output_poly,
                context.transformContext(),
                QgsVectorFileWriter.SaveVectorOptions()
            )
            if error != QgsVectorFileWriter.NoError:
                raise Exception(f'QgsVectorFileWriter error {error}: {error_msg}')

            logger.info(f'Capa de polígonos guardada exitosamente en: {output_poly}')
            results[self.PARAM_OUTPUT_POLY] = output_poly
            results['log_file'] = log_path
            
            # Load the layer into QGIS
            try:
                project = context.project()
                if project:
                    output_layer_loaded = project.addMapLayer(
                        QgsVectorLayer(output_poly, 'lidar_height', 'ogr')
                    )
                    logger.info(f'Capa cargada en QGIS: {output_layer_loaded.name() if output_layer_loaded else "FAILED"}')
                else:
                    logger.warning('No project available in context, layer not loaded')
            except Exception as load_err:
                logger.warning(f'Could not load layer into QGIS: {str(load_err)}')

        except Exception as e:
            logger.error(f'Error en procesamiento: {str(e)}', exc_info=True)
            raise
        finally:
            # Cleanup temporaries
            try:
                if resampled_tmp and os.path.exists(resampled_tmp):
                    os.remove(resampled_tmp)
                    logger.info(f'Removed temporary resampled DTM: {resampled_tmp}')
            except Exception:
                pass
            try:
                if ndsm_tmp and os.path.exists(ndsm_tmp):
                    os.remove(ndsm_tmp)
                    logger.info(f'Removed temporary nDSM raster: {ndsm_tmp}')
            except Exception:
                pass

        return results

    def name(self): return 'LiDARHeightExtractor'
    def displayName(self): return 'LiDARHeightExtractor + Zonal Stats'
    def group(self): return 'LiDAR'
    def groupId(self): return 'lidar_height_extractor_v1'
    def createInstance(self): return LiDARHeightExtractorAlgorithm()