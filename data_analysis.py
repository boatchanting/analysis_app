import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
    QHBoxLayout, QComboBox, QLineEdit, QListWidget, QCheckBox, QColorDialog, QSpinBox, QSplitter
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

    def load_algorithms(self):
        """
        加载 method/ 目录下的 JSON 配置文件，并构建树状结构
        """
        method_dir = os.path.join(os.getcwd(), 'method')
        if not os.path.exists(method_dir):
            self.status_label.setText(f"算法目录 {method_dir} 不存在")
            return

        for root, dirs, files in os.walk(method_dir):
            # 排除 __pycache__ 文件夹
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')

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
                """
                这里写入的代码会根据参数类型创建相应的控件，并将其添加到参数设置界面中
                """
                label = QLabel(param['name'])
                self.parameter_layout.addWidget(label)
                if param['type'] == 'column_select':
                    """
                    下拉框控件:
                    json配置示例
                    {
                        "name": "数据列",
                        "type": "column_select",
                        "function": "column",
                        "required": true,
                        "description": "请选择要绘制的列"
                    }
                    """
                    widget = QComboBox()
                    if self.data is not None:
                        widget.addItems(self.data.columns)
                    self.parameter_widgets[param['name']] = widget                    
                elif param['type'] == 'multi_column_select':
                    """
                    多选下拉框控件:
                    json配置示例
                    {
                        "name": "数据列",
                        "type": "multi_column_select",
                        "function": "column",
                        "required": true,
                        "description": "请选择要绘制的列"
                    }
                    """
                    widget = QListWidget()
                    widget.setSelectionMode(QListWidget.MultiSelection)
                    if self.data is not None:
                        widget.addItems(self.data.columns)
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'color':
                    """
                    颜色选择控件:
                    json配置示例
                    """
                    widget = QPushButton("选择颜色")
                    widget.clicked.connect(self.select_color)
                    widget.setStyleSheet(f"background-color: {param.get('default', '#FFFFFF')}")
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'boolean':
                    """
                    复选框控件:
                    json配置示例
                    {
                        "name": "是否显示图例",
                        "type": "boolean",
                        "function": "legend",
                        "required": false,
                        "default": true,
                        "description": "是否显示图例"
                    }
                    """
                    widget = QCheckBox()
                    widget.setChecked(param.get('default', False))
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'number':
                    """
                    数字输入框控件:
                    json配置示例
                    """
                    widget = QSpinBox()
                    widget.setRange(*param.get('range', [0, 100]))
                    widget.setValue(param.get('default', 0))
                    self.parameter_widgets[param['name']] = widget
                elif param['type'] == 'text': # 文本框控件
                    """
                    文本输入框控件:
                    json配置示例
                    """
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
            button.setProperty("selected_color", color.name())

    def run_analysis(self):
        """
        执行选中的算法
        """
        if not self.current_algorithm:
            self.status_label.setText("请先选择算法")
            return

        # 获取当前选中的算法配置文件路径
        algorithm_json_path = self.current_algorithm
        algorithm_dir = os.path.dirname(algorithm_json_path)
        
        # 读取 JSON 配置文件
        try:
            with open(algorithm_json_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            self.status_label.setText(f"读取配置文件失败：{e}")
            return
        
        # 获取算法脚本路径 (脚本与配置文件同名，只是扩展名不同)
        algorithm_script_path = os.path.join(algorithm_dir, config['algorithm'] + '.py')
        
        # 确保脚本文件存在
        if not os.path.exists(algorithm_script_path):
            self.status_label.setText(f"算法脚本 {algorithm_script_path} 不存在")
            return

        # 收集用户输入的参数，并映射到 run 函数的参数名称
        params = {}
        for param in config["parameters"]:
            param_name = param["name"]
            param_function = param["function"]  # 从配置文件获取函数名
            widget = self.parameter_widgets.get(param_name)

            if widget:
                if isinstance(widget, QComboBox):
                    params[param_function] = widget.currentText()
                elif isinstance(widget, QLineEdit):
                    params[param_function] = widget.text()
                elif isinstance(widget, QSpinBox):
                    params[param_function] = widget.value()
                elif isinstance(widget, QCheckBox):
                    params[param_function] = widget.isChecked()
                elif isinstance(widget, QListWidget):
                    params[param_function] = [item.text() for item in widget.selectedItems()]
                elif isinstance(widget, QPushButton):
                    params[param_function] = widget.property("selected_color") or param.get('default', '#FFFFFF')

        # 动态加载算法脚本
        try:
            spec = importlib.util.spec_from_file_location(config['algorithm'], algorithm_script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 调用算法的 run 函数并传递参数
            module.run(self.data, **params)
            self.status_label.setText(f"算法 {config['algorithm']} 执行成功")
        except Exception as e:
            self.status_label.setText(f"算法执行失败：{e}")

    @staticmethod
    def clear_layout(layout): #用于清除布局中的所有控件
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
