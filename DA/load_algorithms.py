# DA/load_algorithms.py

import os
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt

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
