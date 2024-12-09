# \method\XGBoost分类.py
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run(data, condition_columns, target_column, n_estimators=100, max_depth=3, learning_rate=0.1, gamma=0, subsample=1, colsample_bytree=1, random_state=42):
    """
    XGBoost分类器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param n_estimators: XGBoost中的弱学习器数量
    :param max_depth: 树的最大深度
    :param learning_rate: 学习率
    :param gamma: 正则化参数，控制每棵树的复杂度
    :param subsample: 用于训练的样本比例
    :param colsample_bytree: 用于每棵树的特征子样本比例
    :param random_state: 随机种子（用于数据划分）
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化XGBoost分类器
    model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        gamma=gamma,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state
    )
    
    # 训练模型
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # 输出结果
    print(f"XGBoost分类器的准确率: {acc:.4f}")
    print("分类报告:")
    print(report)
