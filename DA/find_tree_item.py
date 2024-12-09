# DA/find_tree_item.py

import os

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
