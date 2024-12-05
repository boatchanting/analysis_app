# \method\散点图（2列）.py
import matplotlib.pyplot as plt

def run(data, x_column, y_column, color="#00ADEF", marker="o", title="散点图"):
    """
    绘制两列数据的散点图
    :param data: 数据源 (Pandas DataFrame)
    :param x_column: x轴数据列名
    :param y_column: y轴数据列名
    :param color: 点的颜色
    :param marker: 点的形状
    :param title: 图表标题
    """
    plt.rc('font', family='SimHei')  
    plt.rc('axes', unicode_minus=False)  
    plt.rcParams['font.sans-serif'] = ['SimHei']  
    plt.scatter(data[x_column], data[y_column], c=color, marker=marker, alpha=0.7, edgecolors='black')
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
