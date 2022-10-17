from pathlib import Path
import json
import xml.etree.ElementTree as ET

import qgis.core as qgs_core
from json import JSONDecodeError


class ConfigWorker:

    def __init__(self, header: str):

        self.header = header
        self.config_file_path = Path(__file__).parents[1].joinpath('configs/config.json')

        self.styles_config_path = Path(
            qgs_core.QgsProject.instance().fileName()).parent.joinpath('style_files/config_styles.json')
        # self.styles_qml_path = Path(
        #     qgs_core.QgsProject.instance().fileName()).parent.joinpath('style_files/qml_files/')

        self.config_file = self._get_config_file()
        self.styles_config_file = self._get_styles_config_file()

    def _get_config_file(self):
        with open(self.config_file_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)

    def _get_styles_config_file(self):
        try:
            with open(self.styles_config_path, 'r', encoding='utf-8') as styles_config_file:
                return json.load(styles_config_file)
        except JSONDecodeError:
            with open(self.styles_config_path, 'r', encoding='utf-8-sig') as styles_config_file:
                return json.load(styles_config_file)

    def config_reader(self) -> dict:
        return self.config_file.get(self.header)

    def styles_config_reader(self) -> dict:
        return self.styles_config_file.get(self.header)

    def config_writer(self, change_field: str, new_value: Path) -> None:
        self.config_file[self.header][change_field] = str(new_value)
        with open(self.config_file_path, 'w', encoding='utf-8') as config_file:
            config_file.write(json.dumps(self.config_file, ensure_ascii=False))
