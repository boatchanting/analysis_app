# \method\KNN回归.py
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run(data, condition_columns, target_column, n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', random_state=42):
    """
    K近邻回归器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param n_neighbors: 邻居的数量
    :param weights: 权重函数 ('uniform' 或 'distance')
    :param algorithm: 用于计算最近邻的算法 ('auto', 'ball_tree', 'kd_tree', 'brute')
    :param leaf_size: 树的叶子大小
    :param p: 距离度量的幂参数（1为曼哈顿距离，2为欧氏距离）
    :param metric: 距离度量方式
    :param random_state: 随机种子（用于数据划分）
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练KNN回归器
    model = KNeighborsRegressor(n_neighbors=n_neighbors, weights=weights, algorithm=algorithm,
                                leaf_size=leaf_size, p=p, metric=metric)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # 输出结果
    print(f"KNN回归模型的均方误差: {mse:.4f}")
    print(f"R²评分: {r2:.4f}")
