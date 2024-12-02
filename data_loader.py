import pandas as pd
import chardet
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QGuiApplication

class DataLoader(QWidget):
    # 定义信号
    data_loaded = pyqtSignal(pd.DataFrame)  # 信号：数据加载完成，传递 Pandas DataFrame

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.load_stylesheet("styles/data_loader.qss") # 加载样式表
        layout = QVBoxLayout(self) # 创建垂直布局

        # 文件选择按钮
        self.load_button = QPushButton("点我选择文件进行加载")
        self.load_button.setObjectName("load_button")  # 设置对象名，方便QSS选择
        self.load_button.clicked.connect(self.load_data)

        # 状态标签
        self.status_label = QLabel("请选择文件进行加载或者直接拖动数据进入窗格")
        self.status_label.setObjectName("status_label")  # 设置对象名，方便QSS选择
        self.status_label.setAlignment(Qt.AlignCenter)  # 设置标签文字居中
        layout.addWidget(self.status_label)
        layout.addWidget(self.load_button)
        layout.setStretch(0, 1)  # 标签占 10%
        layout.setStretch(1, 8)  # 按钮占 80%
        self.setLayout(layout)

        # 启用拖放功能
        self.setAcceptDrops(True)

    def set_window_size(self):
        # 获取屏幕尺寸
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算全屏的80%大小
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)

        # 设置窗口大小
        self.setGeometry(100, 100, width, height)
    
    def load_stylesheet(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"读取样式表失败: {e}")

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
        # 设置默认文件路径
        default_path = ".\\example\\example.xlsx"

        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", default_path, "数据文件 (*.csv *.xlsx *.xls *.txt)"
        )
        if file_path:
            try:
                # 检测文件编码
                encoding = self.detect_encoding(file_path)

                # 根据文件类型加载数据
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=encoding)
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path) # 这里一定不要加encoding参数，否则会报错!
                elif file_path.endswith('.txt'):
                    df = pd.read_table(file_path, encoding=encoding)
                else:
                    raise ValueError("不支持的文件格式")

                # 通过信号发送数据
                self.data_loaded.emit(df)
                self.status_label.setText(f"数据加载成功：{file_path}")
            except Exception as e:
                self.status_label.setText(f"加载数据失败: {e}")
    
    def dragEnterEvent(self, event):
        """
        拖拽进入事件，允许接受文件拖拽
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """
        拖拽放下事件，处理文件拖拽
        """
        # 获取拖拽的文件路径
        file_path = event.mimeData().urls()[0].toLocalFile()

        if file_path:
            try:
                # 检测文件编码
                encoding = self.detect_encoding(file_path)

                # 根据文件类型加载数据
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=encoding)
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path) # 这里一定不要加encoding参数，否则会报错!
                elif file_path.endswith('.txt'):
                    df = pd.read_table(file_path, encoding=encoding)
                else:
                    raise ValueError("不支持的文件格式")

                # 通过信号发送数据
                self.data_loaded.emit(df)
                self.status_label.setText(f"数据加载成功：{file_path}")
            except Exception as e:
                self.status_label.setText(f"加载数据失败: {e}")
    

