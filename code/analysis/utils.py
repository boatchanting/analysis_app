# code/analysis/utils.py

from PyQt5.QtWidgets import QLayout

def clear_layout(layout: QLayout):
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
                clear_layout(item.layout())
