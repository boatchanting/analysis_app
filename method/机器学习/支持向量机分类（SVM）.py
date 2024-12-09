# \method\SVM分类.py
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run(data, condition_columns, target_column, kernel='rbf', C=1.0, gamma='scale', degree=3, coef0=0.0, random_state=42):
    """
    支持向量机分类器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param kernel: 核函数类型（'linear', 'poly', 'rbf', 'sigmoid'）
    :param C: 惩罚参数，控制分类器的复杂度（越大越复杂）
    :param gamma: 核函数的系数（'scale', 'auto' 或具体的数值）
    :param degree: 多项式核函数的度数（适用于'poly'核）
    :param coef0: 核函数的常数项（适用于'poly'或'sigmoid'核）
    :param random_state: 随机种子（用于数据划分）
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练支持向量机分类器
    model = SVC(kernel=kernel, C=C, gamma=gamma, degree=degree, coef0=coef0, random_state=random_state)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    # 输出结果
    print(f"支持向量机分类器的准确率: {acc:.4f}")
    print("分类报告:")
    print(report)
