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
                {
                    "name": "颜色",
                    "type": "color",
                    "function": "color",
                    "default": "#FFFFFF",
                    "description": "请选择颜色"
                }
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
                    "description": "是否显示图例"
                }
                """
                widget = QCheckBox()
                widget.setChecked(param.get('default', False))
                self.parameter_widgets[param['name']] = widget
            elif param['type'] == 'number':
                """
                整数输入框控件:
                json配置示例
                {
                    "name": "透明度",
                    "type": "number",
                    "function": "alpha",
                    "range": [0, 100],
                    "default": 50,
                    "description": "请输入透明度"
                }
                """
                widget = QLineEdit()
                # 设置默认值
                widget.setText(str(param.get('default', 0)))
                # 设置占位符文本
                widget.setPlaceholderText(f"请输入{param['name']}（范围：{param.get('range')[0]} 到 {param.get('range')[1]}）")
                
                # 设置输入验证器，限制为整数，并指定范围
                validator = QIntValidator(param.get('range')[0], param.get('range')[1])
                widget.setValidator(validator)
                
                self.parameter_widgets[param['name']] = widget

            elif param['type'] == 'float':
                """
                小数输入控件:
                json配置示例
                {
                    "name": "学习率",
                    "type": "float",
                    "function": "learning_rate",
                    "default": 0.01,
                    "range": [0.0001, 1],
                    "description": "设置学习率（范围：0.0001 到 1）"
                }
                """
                widget = QLineEdit()
                widget.setPlaceholderText(f"请输入 {param['name']}（范围：{param.get('range')[0]} 到 {param.get('range')[1]}）")
                widget.setValidator(QDoubleValidator(param.get('range')[0], param.get('range')[1], 4))  # 限制为小数，最多四位
                if 'default' in param:
                    widget.setText(str(param['default']))
                self.parameter_widgets[param['name']] = widget
                self.parameter_layout.addWidget(widget)

            elif param['type'] == 'text': # 文本框控件
                """
                文本输入框控件:
                json配置示例
                """
                widget = QLineEdit()
                widget.setText(param.get('default', '请输入文本'))
                self.parameter_widgets[param['name']] = widget         

            elif param['type'] == 'combo_box':
                """
                下拉框控件:
                json配置示例
                {
                    "name": "距离度量方式",
                    "type": "combo_box",
                    "options": ["minkowski", "euclidean", "manhattan", "chebyshev", "seuclidean", "mahalanobis"],
                    "default": "minkowski",
                    "description": "选择距离度量方式"
                }
                """
                widget = QComboBox()
                
                # 添加选项到下拉框
                if 'options' in param:
                    widget.addItems(param['options'])
                
                # 设置默认值
                if 'default' in param:
                    widget.setCurrentText(param['default'])
                
                # 保存控件
                self.parameter_widgets[param['name']] = widget
                self.parameter_layout.addWidget(widget)
       
        
            
            else:
                widget = QLabel("未知参数类型")
            self.parameter_layout.addWidget(widget)
        print(self.parameter_widgets)  # 调试用，检查控件

    except Exception as e:
        self.status_label.setText(f"加载参数失败：{e}")
