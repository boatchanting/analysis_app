# DA/update_columns.py

def update_columns(self, data):
    """
    更新数据列名，在参数界面需要时使用
    :param data: 当前加载的数据 (Pandas DataFrame)
    """
    self.data = data
    # 如果当前已有选中的算法，重新生成参数界面
    if self.current_algorithm:
        from DA.load_algorithm_parameters import load_algorithm_parameters
        load_algorithm_parameters(self)
