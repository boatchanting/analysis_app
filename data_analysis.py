from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QListWidget, QHBoxLayout, QListWidgetItem, QColorDialog,
    QLineEdit, QCheckBox, QSpinBox, QFileDialog
)
from PyQt5.QtCore import Qt
import importlib
import os
import sys
import random

class DataAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = None  # 用于存储当前加载的数据

    def init_ui(self):
        main_layout = QHBoxLayout()

        # 左侧：算法树状选择控件
        self.algorithm_tree = QTreeWidget()
        self.algorithm_tree.setHeaderLabel("算法选择")
        self.load_algorithms()
        self.algorithm_tree.itemClicked.connect(self.on_algorithm_selected)

        # 右侧：参数设置和执行区域
        self.right_layout = QVBoxLayout()

        # 参数设置区域（动态变化）
        self.parameter_widget = QWidget()
        self.parameter_layout = QVBoxLayout()
        self.parameter_widget.setLayout(self.parameter_layout)

        # 执行按钮
        self.run_button = QPushButton("运行分析")
        self.run_button.clicked.connect(self.run_analysis)

        # 状态标签
        self.status_label = QLabel("请选择算法并设置参数")

        # 将控件添加到右侧布局
        self.right_layout.addWidget(self.parameter_widget)
        self.right_layout.addWidget(self.run_button)
        self.right_layout.addWidget(self.status_label)
        self.right_layout.addStretch()

        # 添加左右布局
        main_layout.addWidget(self.algorithm_tree, 1)
        main_layout.addLayout(self.right_layout, 2)
        self.setLayout(main_layout)

        # 保存当前选中的算法信息
        self.current_algorithm = None
        self.current_algorithm_module = None

    def load_algorithms(self):
        """
        加载 method/ 目录下的算法，并构建树状结构
        """
        method_dir = os.path.join(os.getcwd(), 'method')
        if not os.path.exists(method_dir):
            self.status_label.setText(f"算法目录 {method_dir} 不存在")
            return

        # 遍历文件目录
        for root, dirs, files in os.walk(method_dir):
            relative_path = os.path.relpath(root, method_dir)
            if relative_path == '.':
                # 如果是顶层目录，则将子节点挂载到根
                parent_item = self.algorithm_tree
            else:
                # 查找父节点
                parent_item = self.find_tree_item(relative_path)

            if parent_item is None:
                continue

            # 添加子目录
            for dir_name in dirs:
                dir_item = QTreeWidgetItem(parent_item, [dir_name])
                dir_item.setData(0, Qt.UserRole, os.path.join(relative_path, dir_name))

            # 添加算法文件
            for file_name in files:
                if file_name.endswith('.py'):
                    algorithm_name = os.path.splitext(file_name)[0]
                    file_item = QTreeWidgetItem(parent_item, [algorithm_name])
                    file_item.setData(0, Qt.UserRole, os.path.join(relative_path, file_name))

    def find_tree_item(self, path):
        """
        根据相对路径在树中查找对应的 QTreeWidgetItem
        """
        parts = path.split(os.sep)
        parent = self.algorithm_tree.invisibleRootItem()  # 从根节点开始查找
        for part in parts:
            found = False
            for i in range(parent.childCount()):  # 遍历子节点
                item = parent.child(i)
                if item.text(0) == part:  # 匹配节点名称
                    parent = item
                    found = True
                    break
            if not found:
                return None
        return parent


    def on_algorithm_selected(self, item, column):
        """
        当用户在树中选择算法时，更新参数设置界面
        """
        algorithm_path = item.data(0, Qt.UserRole)
        if algorithm_path and algorithm_path.endswith('.py'):
            # 保存当前选中的算法信息
            self.current_algorithm = algorithm_path.replace('\\', '/')
            # 动态加载算法模块
            module_name = self.current_algorithm.replace('/', '.').replace('.py', '')
            try:
                if module_name in sys.modules:
                    del sys.modules[module_name]
                self.current_algorithm_module = importlib.import_module(module_name)
                self.status_label.setText(f"已选择算法：{item.text(0)}")
                # 动态生成参数界面
                self.generate_parameter_ui()
            except Exception as e:
                self.status_label.setText(f"加载算法失败：{e}")
        else:
            self.current_algorithm = None
            self.current_algorithm_module = None
            self.parameter_layout = QVBoxLayout()
            self.parameter_widget.setLayout(self.parameter_layout)
            self.status_label.setText("请选择具体的算法")

    def generate_parameter_ui(self):
        """
        根据算法模块的需要，动态生成参数输入界面
        """
        # 清空参数布局
        for i in reversed(range(self.parameter_layout.count())):
            widget = self.parameter_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # 检查算法模块是否有自定义的参数界面生成函数
        if hasattr(self.current_algorithm_module, 'setup_ui'):
            self.current_algorithm_module.setup_ui(self.parameter_layout, self.data)
        else:
            # 默认提示
            label = QLabel("该算法未提供参数设置界面")
            self.parameter_layout.addWidget(label)

    def update_columns(self, data):
        """
        更新数据，在参数界面中需要使用
        """
        self.data = data
        # 如果已经选择了算法，重新生成参数界面，以便参数界面可以获取最新的数据列名
        if self.current_algorithm_module is not None:
            self.generate_parameter_ui()

    def run_analysis(self):
        """
        执行选中的算法
        """
        if self.current_algorithm_module is None:
            self.status_label.setText("请先选择算法")
            return

        # 从参数界面获取参数
        if hasattr(self.current_algorithm_module, 'get_params'):
            params = self.current_algorithm_module.get_params()
        else:
            params = {}

        # 传入数据和参数执行算法
        try:
            self.current_algorithm_module.run(self.data, **params)
            self.status_label.setText("算法执行成功")
        except Exception as e:
            self.status_label.setText(f"算法执行失败：{e}")
