# DL/load_stylesheet.py

def load_stylesheet(self, path):
    """
    加载指定路径的样式表并应用到窗口。
    :param path: 样式表文件路径
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
    except Exception as e:
        print(f"读取样式表失败: {e}")
