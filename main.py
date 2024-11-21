import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from data_loader import DataLoader
from data_preview import DataPreview
from data_analysis import DataAnalysis

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据分析软件")
        self.setGeometry(100, 100, 800, 600)

        # 初始化界面布局
        self.init_ui()

    def init_ui(self):
        # 主窗口的中心组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Tab布局
        self.tabs = QTabWidget()
        self.data_loader = DataLoader()
        self.data_preview = DataPreview()
        self.data_analysis = DataAnalysis()

        # 添加Tab页面
        self.tabs.addTab(self.data_loader, "数据加载")
        self.tabs.addTab(self.data_preview, "数据预览")
        self.tabs.addTab(self.data_analysis, "数据分析")

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

        # 信号与槽：数据加载后更新预览和列名框
        self.data_loader.data_loaded.connect(self.data_preview.update_preview)
        self.data_loader.data_loaded.connect(self.data_analysis.update_columns)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
