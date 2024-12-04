# code/analysis/algorithm_loader.py
# 用于加载算法目录并构建树状结构的类
"""
该类主要用于在图形用户界面中显示算法目录结构，方便用户浏览和选择算法。
通过加载 method/ 目录下的 JSON 配置文件，可以动态构建树状结构，并显示目录和文件。
"""
import os
import json
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt

class AlgorithmLoader:
    def __init__(self, tree_widget: QTreeWidget, status_label):
        self.tree_widget = tree_widget
        self.status_label = status_label

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
            parent_item = self.tree_widget.invisibleRootItem() if relative_path == '.' else self.find_tree_item(relative_path)

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
        parent = self.tree_widget.invisibleRootItem()
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
