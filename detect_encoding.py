# DL/detect_encoding.py

import chardet

def detect_encoding(self, file_path, sample_size=1024):
    """
    检测文件编码方式
    :param file_path: 文件路径
    :param sample_size: 检测编码的样本大小
    :return: 检测到的编码方式
    """
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(sample_size)
        result = chardet.detect(raw_data)
        return result['encoding']
    except Exception as e:
        self.status_label.setText(f"检测编码失败: {e}")
        return None
