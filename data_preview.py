from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QLabel
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd

class DataPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = None  # 保存数据

    def init_ui(self):
        layout = QVBoxLayout()

        # 数据表格视图
        self.table_view = QTableView()
        self.status_label = QLabel("当前无数据加载")

        layout.addWidget(self.status_label)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def update_preview(self, data: pd.DataFrame):
        """
        更新数据预览
        :param data: 加载完成的 Pandas DataFrame
        """
        if data is not None:
            self.data = data
            model = PandasTableModel(data)
            self.table_view.setModel(model)
            self.status_label.setText("数据预览更新成功")
        else:
            self.status_label.setText("数据预览失败: 数据为空")

class PandasTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.data.columns[section]
            if orientation == Qt.Vertical:
                return self.data.index[section]
        return None
