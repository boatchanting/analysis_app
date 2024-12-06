# \method\决策树.py
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run(data, condition_columns, target_column, max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42):
    """
    决策树分类器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param max_depth: 决策树的最大深度
    :param min_samples_split: 节点分裂所需的最小样本数
    :param min_samples_leaf: 叶节点所需的最小样本数
    :param random_state: 随机种子
    """
    # 数据验证
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    # 特征和目标分离
    X = data[condition_columns]
    y = data[target_column]
    
    # 数据划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练决策树分类器
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # 输出结果
    print(f"决策树分类器的准确率: {acc:.4f}")
    print("分类报告:")
    print(report)
