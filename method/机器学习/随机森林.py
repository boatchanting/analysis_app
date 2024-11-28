# RandomForest.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def run(data, target_column, feature_columns, test_size=0.2, shuffle=True, n_estimators=100, max_depth=None):
    """
    使用随机森林算法进行分类任务。
    
    :param data: 输入数据 (Pandas DataFrame)
    :param target_column: 目标列（y）
    :param feature_columns: 特征列（X）
    :param test_size: 测试集占比，默认 0.2
    :param shuffle: 是否打乱数据，默认 True
    :param n_estimators: 随机森林中树的数量，默认 100
    :param max_depth: 树的最大深度，默认 None
    """
    # 提取特征数据和目标数据
    X = data[feature_columns]
    y = data[target_column]
    
    # 划分数据集（训练集和测试集）
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=shuffle, random_state=42)

    # 创建随机森林模型
    rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

    # 训练模型
    rf.fit(X_train, y_train)

    # 预测
    y_pred = rf.predict(X_test)

    # 评估模型
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型准确度: {accuracy * 100:.2f}%")

    return rf
