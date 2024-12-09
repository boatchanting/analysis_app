# DL/drop_event.py

def dropEvent(self, event):
    """
    拖拽放下事件，处理文件拖拽
    """
    # 获取拖拽的文件路径
    if event.mimeData().hasUrls():
        file_path = event.mimeData().urls()[0].toLocalFile()

        if file_path:
            try:
                # 检测文件编码
                encoding = self.detect_encoding(file_path)

                # 根据文件类型加载数据
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding=encoding)
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)  # 这里一定不要加encoding参数，否则会报错!
                elif file_path.endswith('.txt'):
                    df = pd.read_table(file_path, encoding=encoding)
                else:
                    raise ValueError("不支持的文件格式")

                # 通过信号发送数据
                self.data_loaded.emit(df)
                self.status_label.setText(f"数据加载成功：{file_path}")
            except Exception as e:
                self.status_label.setText(f"加载数据失败: {e}")
