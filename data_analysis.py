import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QHBoxLayout, QComboBox, QLineEdit, QListWidget, QCheckBox, QColorDialog, QSpinBox
)
from PyQt5.QtCore import Qt
import importlib


class DataAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = None  # 用于存储当前加载的数据
        self.current_algorithm = None
        self.current_parameters = {}
        self.parameter_widgets = {}  # 保存参数控件，方便获取值

    def update_columns(self, data):
        """
        更新数据列名，在参数界面需要时使用
        :param data: 当前加载的数据 (Pandas DataFrame)
        """
        self.data = data
        # 如果当前已有选中的算法，重新生成参数界面
        if self.current_algorithm:
            self.load_algorithm_parameters()

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

    def load_algorithms(self):
        """
        加载 method/ 目录下的 JSON 配置文件，并构建树状结构
        """
        method_dir = os.path.join(os.getcwd(), 'method')
        if not os.path.exists(method_dir):
            self.status_label.setText(f"算法目录 {method_dir} 不存在")
            return

        for root, dirs, files in os.walk(method_dir):
            relative_path = os.path.relpath(root, method_dir)
            parent_item = self.algorithm_tree.invisibleRootItem() if relative_path == '.' else self.find_tree_item(relative_path)

            if parent_item is None:
                continue

            # 添加子目录
            for dir_name in dirs:
                dir_item = QTreeWidgetItem(parent_item, [dir_name])
                dir_item.setData(0, Qt.UserRole, os.path.join(relative_path, dir_name))

            # 添加 JSON 文件
            for file_name in files:
                if file_name.endswith('.json'):
                    algorithm_name = os.path.splitext(file_name)[0]
                    file_item = QTreeWidgetItem(parent_item, [algorithm_name])
                    file_item.setData(0, Qt.UserRole, os.path.join(relative_path, file_name))

    def find_tree_item(self, path):
        """
        根据相对路径在树中查找对应的 QTreeWidgetItem
        """
        parts = path.split(os.sep)
        parent = self.algorithm_tree.invisibleRootItem()
        for part in parts:
            found = False
            for i in range(parent.childCount()):
                item = parent.child(i)
                if item.text(0) == part:
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
        if algorithm_path and algorithm_path.endswith('.json'):
            self.current_algorithm = os.path.join('method', algorithm_path)
            self.load_algorithm_parameters()

    def load_algorithm_parameters(self):
        """
        加载选中算法的 JSON 配置并生成参数设置界面
        """
        # 清空参数布局
        self.clear_layout(self.parameter_layout)
        self.parameter_widgets.clear()

        try:
            with open(self.current_algorithm, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.current_parameters = config.get('parameters', [])
            self.status_label.setText(f"已加载算法：{config.get('name')}")

            for param in self.current_parameters:
                label = QLabel(param['name'])
                self.parameter_layout.addWidget(label)

                if param['type'] == 'column_select':
                    widget = QComboBox()
                    if self.data is not None:
                        widget.addItems(self.data.columns)
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'multi_column_select':
                    widget = QListWidget()
                    widget.setSelectionMode(QListWidget.MultiSelection)
                    if self.data is not None:
                        widget.addItems(self.data.columns)
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'color':
                    widget = QPushButton("选择颜色")
                    widget.clicked.connect(self.select_color)
                    widget.setStyleSheet(f"background-color: {param.get('default', '#FFFFFF')}")
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'boolean':
                    widget = QCheckBox()
                    widget.setChecked(param.get('default', False))
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'number':
                    widget = QSpinBox()
                    widget.setRange(*param.get('range', [0, 100]))
                    widget.setValue(param.get('default', 0))
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'text':
                    widget = QLineEdit()
                    widget.setText(param.get('default', ''))
                    self.parameter_widgets[param['name']] = widget
                else:
                    widget = QLabel("未知参数类型")
                self.parameter_layout.addWidget(widget)

        except Exception as e:
            self.status_label.setText(f"加载参数失败：{e}")

    def select_color(self):
        """
        打开颜色选择器
        """
        button = self.sender()
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}")

    def run_analysis(self):
        """
        执行选中的算法
        """
        if not self.current_algorithm:
            self.status_label.setText("请先选择算法")
            return

        # 收集用户输入的参数
        params = {}
        for name, widget in self.parameter_widgets.items():
            if isinstance(widget, QComboBox):
                params[name] = widget.currentText()
            elif isinstance(widget, QListWidget):
                params[name] = [item.text() for item in widget.selectedItems()]
            elif isinstance(widget, QPushButton):
                params[name] = widget.styleSheet().split("background-color: ")[-1].strip(";")
            elif isinstance(widget, QCheckBox):
                params[name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                params[name] = widget.value()
            elif isinstance(widget, QLineEdit):
                params[name] = widget.text()

        # 动态加载对应的算法实现
        algorithm_name = os.path.splitext(os.path.basename(self.current_algorithm))[0]
        try:
            module = importlib.import_module(f"method.{algorithm_name}")
            module.run(self.data, **params)
            self.status_label.setText(f"算法 {algorithm_name} 执行成功")
        except Exception as e:
            self.status_label.setText(f"算法执行失败：{e}")

    @staticmethod
    def clear_layout(layout):
        """
        清除布局中的所有控件
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    DataAnalysis.clear_layout(item.layout())
