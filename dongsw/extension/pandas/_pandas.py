import pandas as pd

def qcut_(data, q = None, by = None, *args, **kwargs):
    '''
    similar to pd.qcut(), but return a list of cut result.

    eg.
    qcut_(pd.Series([1,2,3,4,5]), 2)
    output: 
    [0    1
    1    2
    2    3
    dtype: int64, 
    3    4
    4    5
    dtype: int64]

    data: pd.Series or pd.DataFrame. If DataFrame, must set by param.
    by: column name you select in data or a pd.Series which has the same index.
    return: a list of cut result by qcut.
    '''    
    if isinstance(data, pd.Series):
        by_series = data
    elif isinstance(data, pd.DataFrame) and by is not None:
        by_series = _uniform_the_by_param_to_series(data, by)
    else:
        raise Exception('The param \'data\' must be pd.Series or pd.DataFrame. If DataFrame, must set key param.')

    result = pd.qcut(by_series, q, *args, *kwargs)

    return [pair[1] for pair in data.groupby(result)]

def mean_(data, by = None, invalid_value = None, *args, **kwargs):
    '''
    similar to pd.mean(), but support weighted mean.

    data: pd.Series or pd.DataFrame.
    by: weight used in calculation. column name you select in data or a pd.Series which has the same index.
    invalid_value: if an error occurs during the calculation (for example, non numeric types participate in the calculation), 
    replace the error with a default value.
    return: same as pd.mean().

    '''
    def cal_weighted_mean(by, target):
        return (by * target).sum() / by.sum()
    if by is None:
        return data.mean(*args, *kwargs)
    
    by_series = _uniform_the_by_param_to_series(data, by)
    func = lambda x: cal_weighted_mean(by_series, x)
    return _call_func_adaptive(data, lambda x: _call_func_without_error(x, func, invalid_value))

def rolling_apply_(df, window, func, min_periods = None, *args, **kwargs):
    # todo 有时候index不对
    '''
    pd.rolling_apply_(data, 2, lambda x: x.iloc[1])
    '''
    def _func(x, df, func):
        if len(x) < min_periods:
            return pd.Series(dtype='object')
        start_index = x.index[0]
        end_index = x.index[-1]
        return func(df.loc[start_index:end_index, :])

    if min_periods is None:
        min_periods = window
    s = df.iloc[:, 0]
    roll = s.rolling(window, *args, *kwargs)
    roll = map(lambda x: _func(x, df, func), roll)
    return pd.DataFrame(roll)

def _uniform_the_by_param_to_series(data, by):
    if isinstance(by, str):
        by_series = data[by]
    elif isinstance(by, pd.Series):
        by_series = by
    else:
        raise Exception('The param \'by\' must be pd.Series or string.')
    return by_series

def _call_func_adaptive(data, func, axis = 0):
    '''
    if data is pd.DataFrame instead of pd.Series, then auto apply.
    '''
    if isinstance(data, pd.DataFrame):
        return data.apply(func, axis = axis)
    else:
        return func(data)

def _call_func_without_error(x, func, invalid_value):
    if invalid_value is None:
        return func(x)
    try:
        return func(x)
    except:
        return invalid_value
