# DA/clear_layout.py

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
                from DA.clear_layout import clear_layout
                clear_layout(item.layout())
