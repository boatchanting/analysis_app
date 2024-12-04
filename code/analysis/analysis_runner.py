# code/analysis/analysis_runner.py
# 用于执行选中的算法的类
"""
类名：AnalysisRunner
功能：执行选中的算法
具体用法：
    1. 初始化 AnalysisRunner 对象，传入状态标签和数据
    2. 调用 run_analysis 方法，传入算法路径和参数
    3. 程序会自动读取算法配置文件，并动态加载算法脚本，调用算法的 run 函数并传递参数
"""
import os
import json
import importlib.util

class AnalysisRunner:
    def __init__(self, status_label, data):
        self.status_label = status_label
        self.data = data

    def run_analysis(self, algorithm_path, parameters):
        """
        执行选中的算法
        """
        if not algorithm_path:
            self.status_label.setText("请先选择算法")
            return

        # 获取算法脚本路径 (脚本与配置文件同名，只是扩展名不同)
        algorithm_dir = os.path.dirname(algorithm_path)
        try:
            with open(algorithm_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            self.status_label.setText(f"读取配置文件失败：{e}")
            return

        algorithm_script = config.get('algorithm')
        if not algorithm_script:
            self.status_label.setText("算法配置中缺少 'algorithm' 字段")
            return

        algorithm_script_path = os.path.join(algorithm_dir, f"{algorithm_script}.py")

        # 确保脚本文件存在
        if not os.path.exists(algorithm_script_path):
            self.status_label.setText(f"算法脚本 {algorithm_script_path} 不存在")
            return

        # 动态加载算法脚本
        try:
            spec = importlib.util.spec_from_file_location(algorithm_script, algorithm_script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 调用算法的 run 函数并传递参数
            module.run(self.data, **parameters)
            self.status_label.setText(f"算法 {algorithm_script} 执行成功")
        except Exception as e:
            self.status_label.setText(f"算法执行失败：{e}")
