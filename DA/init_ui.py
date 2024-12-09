# DA/init_ui.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSplitter, QTreeWidget, QLabel
from PyQt5.QtCore import Qt

def init_ui(self):
    """
    初始化用户界面，设置主布局和各个控件。该方法使用QSplitter将界面分为左右两部分，
    左侧为算法选择区域，右侧为参数设置和执行区域。
    """
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSplitter, QTreeWidget, QLabel

    # 主布局使用 QSplitter
    main_splitter = QSplitter(Qt.Horizontal)

    # 左侧：算法树状选择控件
    self.algorithm_tree = QTreeWidget()
    self.algorithm_tree.setHeaderLabel("算法选择")
    self.load_algorithms()
    self.algorithm_tree.itemClicked.connect(self.on_algorithm_selected)

    # 设置算法树控件初始宽度占比为 30%
    main_splitter.addWidget(self.algorithm_tree)
    main_splitter.setStretchFactor(0, 1)  # 设置左侧为固定占比

    # 右侧：参数设置和执行区域
    self.parameter_widget = QWidget()
    self.parameter_layout = QVBoxLayout()
    self.parameter_widget.setLayout(self.parameter_layout)

    # 执行按钮
    self.run_button = QPushButton("运行分析")
    self.run_button.clicked.connect(self.run_analysis)

    # 状态标签
    self.status_label = QLabel("请选择算法并设置参数")

    # 右侧布局
    right_layout = QVBoxLayout()
    right_layout.addWidget(self.parameter_widget)
    right_layout.addWidget(self.run_button)
    right_layout.addWidget(self.status_label)
    right_layout.addStretch()

    right_widget = QWidget()
    right_widget.setLayout(right_layout)

    main_splitter.addWidget(right_widget)
    main_splitter.setStretchFactor(1, 2)  # 设置右侧为可扩展区域

    # 主布局
    main_layout = QVBoxLayout()
    main_layout.addWidget(main_splitter)
    self.setLayout(main_layout)
