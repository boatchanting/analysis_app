# DA/load_algorithm_parameters.py

import os
import json
from PyQt5.QtWidgets import QLabel, QComboBox, QListWidget, QPushButton, QCheckBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

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
            widget = None

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
                widget = QLineEdit()
                widget.setText(str(param.get('default', 0)))
                widget.setPlaceholderText(
                    f"请输入{param['name']}（范围：{param.get('range')[0]} 到 {param.get('range')[1]}）"
                )
                validator = QIntValidator(param.get('range')[0], param.get('range')[1])
                widget.setValidator(validator)
                self.parameter_widgets[param['name']] = widget

            elif param['type'] == 'decimal_input':
                widget = QLineEdit()
                widget.setPlaceholderText(
                    f"请输入 {param['name']}（范围：{param.get('range')[0]} 到 {param.get('range')[1]}）"
                )
                widget.setValidator(QDoubleValidator(param.get('range')[0], param.get('range')[1], 4))
                if 'default' in param:
                    widget.setText(str(param['default']))
                self.parameter_widgets[param['name']] = widget

            elif param['type'] == 'text':
                widget = QLineEdit()
                widget.setText(param.get('default', '请输入文本'))
                self.parameter_widgets[param['name']] = widget

            else:
                widget = QLabel("未知参数类型")

            if widget:
                self.parameter_layout.addWidget(widget)

    except Exception as e:
        self.status_label.setText(f"加载参数失败：{e}")
