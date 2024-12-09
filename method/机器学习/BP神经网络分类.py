# \method\BP神经网络分类.py
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run(data, condition_columns, target_column, hidden_layer_sizes=(100,), activation='relu', solver='adam', max_iter=200, alpha=0.0001, random_state=42):
    """
    BP神经网络分类器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param hidden_layer_sizes: 隐藏层的层数和每层的节点数
    :param activation: 激活函数 ('identity', 'logistic', 'tanh', 'relu')
    :param solver: 优化器 ('lbfgs', 'sgd', 'adam')
    :param max_iter: 最大迭代次数
    :param alpha: 正则化参数
    :param random_state: 随机种子
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练BP神经网络分类器
    model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, max_iter=max_iter, alpha=alpha, random_state=random_state)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    return acc, report
