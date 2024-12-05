# \method\条形堆积图（多列）.py
import matplotlib.pyplot as plt
import numpy as np

def run(data, columns, colors=None, title="条形堆积图"):
    """
    绘制多列数据的条形堆积图
    :param data: 数据源 (Pandas DataFrame)
    :param columns: 需要绘制的列名列表
    :param colors: 颜色列表，每列对应一个颜色
    :param title: 图表标题
    """
    if not columns or len(columns) < 2:
        raise ValueError("请选择至少两个列进行堆积条形图绘制")

    plt.rc('font', family='SimHei')  
    plt.rc('axes', unicode_minus=False)  
    plt.rcParams['font.sans-serif'] = ['SimHei']  

    # 数据准备
    x = np.arange(len(data))  # X轴为索引
    bottom = np.zeros(len(data))  # 初始底部为 0

    if colors is None or len(colors) < len(columns):
        # 若颜色数量不足，自动生成颜色
        colors = plt.cm.tab10.colors[:len(columns)]

    # 绘制堆积条形图
    for i, column in enumerate(columns):
        plt.bar(x, data[column], bottom=bottom, color=colors[i], label=column)
        bottom += data[column]  # 更新底部位置

    plt.title(title)
    plt.xlabel("索引")
    plt.ylabel("值")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="图例")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
