# \method\直方图（1列）.py
import matplotlib.pyplot as plt

def run(data, column, bins=10, color="#FF5733", title="直方图"):
    """
    绘制单列数据的直方图
    :param data: 数据源 (Pandas DataFrame)
    :param column: 需要绘制的列名
    :param bins: 直方图的柱状个数
    :param color: 柱状颜色
    :param title: 图表标题
    """
    plt.rc('font', family='SimHei')  
    plt.rc('axes', unicode_minus=False)  
    plt.rcParams['font.sans-serif'] = ['SimHei']  
    plt.hist(data[column], bins=bins, color=color, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("频数")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
