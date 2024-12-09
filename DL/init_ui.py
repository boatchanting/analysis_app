# DL/init_ui.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSplitter, QTreeWidget, QLabel
from PyQt5.QtCore import Qt

def init_ui(self):
    """
    初始化用户界面，设置布局和控件。
    """
    self.load_stylesheet("styles/data_loader.qss")  # 加载样式表
    layout = QVBoxLayout(self)  # 创建垂直布局

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
