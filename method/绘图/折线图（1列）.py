# \method\折线图（1列）.py
import matplotlib.pyplot as plt

def run(data, column, color="#0000FF", linestyle="-", title="折线图"):
    """
    绘制单列数据的折线图
    :param data: 数据源 (Pandas DataFrame)
    :param column: 需要绘制的列名
    :param color: 线的颜色
    :param linestyle: 线型
    :param title: 图表标题
    """
    plt.rc('font', family='SimHei')  
    plt.rc('axes', unicode_minus=False)  
    plt.rcParams['font.sans-serif'] = ['SimHei']  
    plt.plot(data[column], color=color, linestyle=linestyle)
    plt.title(title)
    plt.xlabel("索引")
    plt.ylabel(column)
    plt.grid(True)
    plt.show()
