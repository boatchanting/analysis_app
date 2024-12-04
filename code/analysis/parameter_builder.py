# code/analysis/parameter_builder.py
# 用于生成算法参数设置界面的类
"""
该类负责生成算法参数设置界面，根据算法的 JSON 配置文件动态生成相应的控件。
"""
import json
from PyQt5.QtWidgets import (
    QLabel, QComboBox, QListWidget, QPushButton,
    QCheckBox, QSpinBox, QLineEdit, QColorDialog
)
from PyQt5.QtCore import Qt

from .utils import clear_layout

class ParameterBuilder:
    def __init__(self, parameter_layout, status_label, data):
        self.parameter_layout = parameter_layout
        self.status_label = status_label
        self.data = data
        self.current_parameters = []
        self.parameter_widgets = {}

    def load_algorithm_parameters(self, algorithm_path):
        """
        加载选中算法的 JSON 配置并生成参数设置界面
        """
        # 清空参数布局
        clear_layout(self.parameter_layout)
        self.parameter_widgets.clear()

        try:
            with open(algorithm_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.current_parameters = config.get('parameters', [])
            self.status_label.setText(f"已加载算法：{config.get('name')}")

            for param in self.current_parameters:
                label = QLabel(param['name'])
                self.parameter_layout.addWidget(label)

                widget = self.create_widget(param)
                self.parameter_widgets[param['name']] = widget
                self.parameter_layout.addWidget(widget)

        except Exception as e:
            self.status_label.setText(f"加载参数失败：{e}")

    def create_widget(self, param):
        """
        根据参数类型创建相应的控件
        """
        param_type = param['type']
        default = param.get('default')

        if param_type == 'column_select':
            widget = QComboBox()
            if self.data is not None:
                widget.addItems(self.data.columns)
        elif param_type == 'multi_column_select':
            widget = QListWidget()
            widget.setSelectionMode(QListWidget.MultiSelection)
            if self.data is not None:
                widget.addItems(self.data.columns)
        elif param_type == 'color':
            widget = QPushButton("选择颜色")
            widget.clicked.connect(self.select_color)
            widget.setStyleSheet(f"background-color: {default or '#FFFFFF'}")
        elif param_type == 'boolean':
            widget = QCheckBox()
            widget.setChecked(default if default is not None else False)
        elif param_type == 'number':
            widget = QSpinBox()
            widget.setRange(*param.get('range', [0, 100]))
            widget.setValue(default if default is not None else 0)
        elif param_type == 'text':
            widget = QLineEdit()
            widget.setText(default or '')
        else:
            widget = QLabel("未知参数类型")
        return widget

    def select_color(self):
        """
        打开颜色选择器
        """
        button = self.sender()
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}")

    def get_parameters(self, config):
        """
        收集用户输入的参数，并映射到 run 函数的参数名称
        """
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
        return params
