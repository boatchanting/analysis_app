# \method\决策树回归.py
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run(data, condition_columns, target_column, criterion='mse', max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=42):
    """
    决策树回归器
    :param data: 数据源 (Pandas DataFrame)
    :param condition_columns: 作为特征的列名列表
    :param target_column: 目标列名
    :param criterion: 划分标准（'mse' 或 'friedman_mse' 或 'mae'）
    :param max_depth: 树的最大深度
    :param min_samples_split: 内部节点再划分所需的最小样本数
    :param min_samples_leaf: 叶子节点最少样本数
    :param random_state: 随机种子（用于数据划分）
    """
    # 数据划分
    if not condition_columns or target_column not in data.columns:
        raise ValueError("请确保选择了特征列和目标列")
    
    X = data[condition_columns]
    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # 初始化并训练决策树回归器
    model = DecisionTreeRegressor(criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                  min_samples_leaf=min_samples_leaf, random_state=random_state)
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # 输出结果
    print(f"决策树回归器的均方误差: {mse:.4f}")
    print(f"决策树回归器的R²得分: {r2:.4f}")
