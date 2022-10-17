import os

from qgis.PyQt.QtWidgets import QProgressDialog, QProgressBar
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.core import QgsVectorLayer, QgsFeatureRequest


def progress_dialog(text_arguments: dict):

    progress_d = QProgressDialog()
    progress_d.setWindowTitle(text_arguments["title"])
    progress_d.setLabelText(text_arguments["label"])
    progress_d.setCancelButton(None)

    prog_bar = QProgressBar(progress_d)
    prog_bar.setTextVisible(True)

    progress_d.setBar(prog_bar)
    progress_d.setMinimumWidth(300)
    progress_d.show()

    return progress_d, prog_bar


def translate(message: str) -> str:

    # initialize locale
    plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # print(plugin_dir)
    locale = QSettings().value('locale/userLocale')[0:2]
    locale_path = os.path.join(
        plugin_dir,
        'i18n',
        f'Delta_{locale}.qm')

    if os.path.exists(locale_path):
        translator = QTranslator()
        translator.load(locale_path)
        QCoreApplication.installTranslator(translator)

    # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    return QCoreApplication.translate('Delta', message)


def check_db_version(db_source: str) -> bool:

    layer_features = QgsVectorLayer(f"{db_source}|layername=sys_info", "sys_inf_l", "ogr")
    feature_request = QgsFeatureRequest().setFilterExpression('"property"=\'database_version\'')
    result = layer_features.getFeatures(feature_request)

    return bool(int(next(result)["value"]) >= 2)
