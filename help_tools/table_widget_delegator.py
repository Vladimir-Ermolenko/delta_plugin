from typing import Optional
from qgis.PyQt.QtWidgets import QStyledItemDelegate, QComboBox, QLineEdit, QTableWidget


class WidgetsDelegate(QStyledItemDelegate):

    def __init__(self, table_widget: QTableWidget, combobox_data: Optional[list] = None) -> None:

        super().__init__(parent=None)
        self.combobox_data = combobox_data
        self.table_widget = table_widget

    def createEditor(self, widget, options, index):

        if index.column() == 1:
            editor = QComboBox(widget)
            return editor

        if index.column() == 2:
            editor = QLineEdit(widget)
            return editor

    def setEditorData(self, editor, index) -> None:

        if index.column() == 1:

            for item in self.combobox_data:
                editor.addItem(item)

    def updateEditorGeometry(self, editor, options, index) -> None:
        editor.setGeometry(options.rect)

    def clear_table_data(self) -> None:
        # delete old info from table when layer update
        for row in range(self.table_widget.rowCount()):
            self.table_widget.removeCellWidget(row, 1)
            self.table_widget.takeItem(row, 1)
            self.table_widget.removeCellWidget(row, 2)
            self.table_widget.takeItem(row, 2)

    def autocomplete_data(self, ac_config: dict) -> None:
        self.clear_table_data()
        # add row with in table with some ac_config strings.
        for row in range(1, self.table_widget.rowCount() + 1):
            column_alias = ac_config.get(str(row), "")
            for alias in column_alias:
                if alias and alias.lower() in {col_name.lower() for col_name in self.combobox_data}:
                    qb_widget = QComboBox()

                    for item in self.combobox_data:
                        qb_widget.addItem(item)

                    for col_name in self.combobox_data:
                        if str(alias).lower() == str(col_name).lower():
                            qb_widget.setCurrentText(col_name)
                    self.table_widget.setCellWidget(row - 1, 1, qb_widget)
