# DL/set_window_size.py

from PyQt5.QtGui import QGuiApplication

def set_window_size(self):
    """
    设置窗口大小为屏幕的80%
    """
    # 获取屏幕尺寸
    screen = QGuiApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # 计算全屏的80%大小
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)

    # 设置窗口大小
    self.setGeometry(100, 100, width, height)
