# DL/drag_enter_event.py

from PyQt5.QtCore import Qt

def dragEnterEvent(self, event):
    """
    拖拽进入事件，允许接受文件拖拽
    """
    if event.mimeData().hasUrls():
        event.acceptProposedAction()
