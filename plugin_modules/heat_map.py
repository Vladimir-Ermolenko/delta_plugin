import processing
import qgis.core as qgs_core
from qgis.core import QgsVectorLayer
import qgis.gui as qgs_gui
from qgis.PyQt import QtCore, QtGui

from ..plugin_modules.delta_plugin_dialog import HeatMap


class HeatMapTool:
    def __init__(self, iface: qgs_gui.QgisInterface):
        self.iface = iface
        self.qgis_project = qgs_core.QgsProject().instance()
        self.layers = {layer.name(): layer for layer in self.qgis_project.mapLayers().values()}
        self.heat_map_dlg = HeatMap()

        self.progress_bar = self.heat_map_dlg.progressBar
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def close_window(self) -> None:
        self.heat_map_dlg.close()

    def generate_layer_list(self) -> None:
        for layer in self.layers.keys():
            self.heat_map_dlg.comboBox_2.addItem(layer)

    def add_int_mask(self):
        int_validator = QtGui.QIntValidator()
        int_validator.setRange(1, 10000)
        self.heat_map_dlg.lineEdit.setValidator(int_validator)
        self.heat_map_dlg.lineEdit_2.setValidator(int_validator)

    def create_grid(self, layer) -> QgsVectorLayer:
        layer_ext = layer.extent()
        extent = f'{layer_ext.xMinimum()},{layer_ext.xMaximum()},{layer_ext.yMinimum()},{layer_ext.yMaximum()}'
        crs = self.qgis_project.crs().toWkt()
        h_spacing = int(self.heat_map_dlg.lineEdit.text())
        v_spacing = int(self.heat_map_dlg.lineEdit_2.text())

        params = {
            'TYPE': 2,
            'EXTENT': extent,
            'HSPACING': h_spacing,
            'VSPACING': v_spacing,
            'HOVERLAY': 0,
            'VOVERLAY': 0,
            'CRS': crs,
            'OUTPUT': 'memory:'
        }

        grid = processing.run('native:creategrid', params)['OUTPUT']
        grid.setName('Grid')
        self.qgis_project.addMapLayer(grid)

        return grid

    def progress_changed(self, progress):
        self.progress_bar.setValue(round(progress))

    def count_points(self, point_layer, grid_layer) -> QgsVectorLayer:
        params = {
            'POLYGONS': grid_layer,
            'POINTS': point_layer,
            'FIELD': 'NUMPOINTS',
            'OUTPUT': 'memory:'
        }

        feedback = qgs_core.QgsProcessingFeedback()
        feedback.progressChanged.connect(self.progress_changed)

        count_layer = processing.run('native:countpointsinpolygon', params, feedback=feedback)['OUTPUT']
        count_layer.setName('heatmap')
        self.qgis_project.addMapLayer(count_layer)

        return count_layer

    @staticmethod
    def style_heatmap(count_layer) -> None:
        color_ramp = qgs_core.QgsStyle().defaultStyle().colorRamp('Spectral')
        color_ramp.invert()

        symbol = qgs_core.QgsSymbol.defaultSymbol(count_layer.geometryType())
        symbol.symbolLayer(0).setStrokeStyle(QtCore.Qt.PenStyle(QtCore.Qt.NoPen))

        renderer = qgs_core.QgsGraduatedSymbolRenderer()
        renderer.setSourceSymbol(symbol)
        renderer.setClassAttribute('NUMPOINTS')
        renderer.setSourceColorRamp(color_ramp)
        renderer.setMode(qgs_core.QgsGraduatedSymbolRenderer.EqualInterval)
        renderer.updateClasses(count_layer, 100)

        count_layer.setRenderer(renderer)
        count_layer.triggerRepaint()

    def main(self, point_layer):
        grid_layer = self.create_grid(point_layer)
        count_layer = self.count_points(point_layer, grid_layer)
        self.style_heatmap(count_layer)

    def heat_map_run(self) -> None:
        if not self.heat_map_dlg.isVisible():
            if self.qgis_project.absoluteFilePath() != "":

                self.generate_layer_list()

                self.add_int_mask()

                point_layer = self.layers[self.heat_map_dlg.comboBox_2.currentText()]

                self.heat_map_dlg.pushButton_3.clicked.connect(lambda: self.main(point_layer))
                self.heat_map_dlg.pushButton.clicked.connect(self.close_window)

                self.heat_map_dlg.activateWindow()

                self.heat_map_dlg.exec()
