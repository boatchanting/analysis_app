# DA/select_color.py

from PyQt5.QtWidgets import QColorDialog

def select_color(self):
    """
    用于打开颜色选择器和储存颜色配置参数
    """
    button = self.sender()
    color = QColorDialog.getColor()
    if color.isValid():
        button.setStyleSheet(f"background-color: {color.name()}")
        button.setProperty("selected_color", color.name())
