import pandas as pd
import chardet
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSignal

class DataLoader(QWidget):
    # 定义信号
    data_loaded = pyqtSignal(pd.DataFrame)  # 信号：数据加载完成，传递 Pandas DataFrame

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 文件选择按钮
        self.load_button = QPushButton("加载数据文件")
        self.load_button.clicked.connect(self.load_data)

        # 状态标签
        self.status_label = QLabel("请选择文件进行加载")

        layout.addWidget(self.load_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def detect_encoding(self, file_path, sample_size=1024):
        """
        检测文件编码方式
        :param file_path: 文件路径
        :param sample_size: 检测编码的样本大小
        :return: 检测到的编码方式
        """
        with open(file_path, "rb") as f:
            raw_data = f.read(sample_size)
        result = chardet.detect(raw_data)
        return result['encoding']

    def load_data(self):
        """
        加载数据文件，并通过信号发送加载结果
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "", "数据文件 (*.csv *.xlsx *.xls *.txt)"
        )
        if file_path:
            try:
                # 检测文件编码
                encoding = self.detect_encoding(file_path)

                # 根据文件类型加载数据
                if file_path.endswith(".csv"):
                    self.data = pd.read_csv(file_path, encoding=encoding)
                elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                    self.data = pd.read_excel(file_path)  # Excel 文件通常不需要编码检测
                elif file_path.endswith(".txt"):
                    self.data = pd.read_table(file_path, encoding=encoding)
                else:
                    raise ValueError("不支持的文件格式")

                # 更新状态标签并发送信号
                self.status_label.setText(f"文件加载成功: {file_path} (编码: {encoding})")
                self.data_loaded.emit(self.data)  # 发射数据加载完成信号

            except Exception as e:
                self.status_label.setText(f"加载失败: {e}")
