import os
import importlib
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem,
    QPushButton, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt


class DataAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None  # 当前加载的数据
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 树状算法选择器
        self.algorithm_tree = QTreeWidget()
        self.algorithm_tree.setHeaderLabel("选择算法")
        self.algorithm_tree.itemClicked.connect(self.display_algorithm_config)

        # 参数输入区
        self.param_input_area = QStackedWidget()

        # 数据列选择部分
        column_selection_layout = QHBoxLayout()
        self.all_columns_list = QListWidget()  # 显示所有列名
        self.selected_columns_list = QListWidget()  # 显示已选择的列
        column_selection_layout.addWidget(QLabel("所有列："))
        column_selection_layout.addWidget(self.all_columns_list)
        column_selection_layout.addWidget(QLabel("选择列："))
        column_selection_layout.addWidget(self.selected_columns_list)

        # 运行按钮
        self.run_button = QPushButton("运行算法")
        self.run_button.clicked.connect(self.run_analysis)

        # 状态标签
        self.status_label = QLabel("请先选择算法")

        # 添加控件到布局
        layout.addWidget(QLabel("算法选择："))
        layout.addWidget(self.algorithm_tree)
        layout.addWidget(QLabel("参数配置："))
        layout.addWidget(self.param_input_area)
        layout.addLayout(column_selection_layout)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # 加载算法
        self.load_algorithms()

    def load_algorithms(self):
        """
        加载 `method` 文件夹中的所有算法，并构建树状选择器
        """
        self.methods = {}
        method_dir = "method"
        for category in os.listdir(method_dir):
            category_path = os.path.join(method_dir, category)
            if os.path.isdir(category_path):
                category_item = QTreeWidgetItem([category])
                self.algorithm_tree.addTopLevelItem(category_item)

                for algorithm in os.listdir(category_path):
                    if algorithm.endswith(".py"):
                        algorithm_name = os.path.splitext(algorithm)[0]
                        algorithm_path = os.path.join(category_path, algorithm)
                        self.methods[algorithm_name] = algorithm_path

                        algorithm_item = QTreeWidgetItem([algorithm_name])
                        category_item.addChild(algorithm_item)

    def update_columns(self, data):
        """
        更新列选择框，显示数据的列名
        """
        self.data = data
        self.all_columns_list.clear()
        self.selected_columns_list.clear()
        if data is not None:
            for column in data.columns:
                item = QListWidgetItem(column)
                self.all_columns_list.addItem(item)

    def display_algorithm_config(self, item):
        """
        根据选择的算法显示对应的参数输入界面
        """
        algorithm_name = item.text(0)
        if algorithm_name in self.methods:
            module_path = self.methods[algorithm_name].replace("/", ".").replace("\\", ".").rstrip(".py")
            module = importlib.import_module(module_path)

            # 动态加载算法的自定义界面
            self.param_input_area.clear()
            if hasattr(module, "get_config_ui"):
                config_widget = module.get_config_ui()
                self.param_input_area.addWidget(config_widget)
                self.param_input_area.setCurrentWidget(config_widget)
            else:
                self.param_input_area.addWidget(QLabel("该算法没有自定义配置界面"))
            self.status_label.setText(f"已选择算法：{algorithm_name}")
        else:
            self.status_label.setText("请选择有效的算法")

    def run_analysis(self):
        """
        运行选中的算法
        """
        current_widget = self.param_input_area.currentWidget()
        if current_widget and hasattr(current_widget, "collect_params"):
            params = current_widget.collect_params()
            self.status_label.setText(f"运行算法，参数：{params}")
        else:
            self.status_label.setText("没有可用的参数配置")
