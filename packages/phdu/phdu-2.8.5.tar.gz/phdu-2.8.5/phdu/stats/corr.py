"""
Correlation metrics
"""
import pandas as pd
import numpy as np
try:
    shell = get_ipython().__class__.__name__
    if shell == 'ZMQInteractiveShell': # script being run in Jupyter notebook
        from tqdm.notebook import tqdm
    elif shell == 'TerminalInteractiveShell': #script being run in iPython terminal
        from tqdm import tqdm
except NameError:
    from tqdm import tqdm # Probably runing on standard python terminal. If does not work => should be replaced by tqdm(x) = identity(x)

def corr_pruned(df, col=None, method='spearman', alpha=0.05, ns_to_nan=True, correct_by_multiple_comp='by'):
    """
    Returns correlation between DataFrame features with pvalue < alpha.

    Parameters
    ----------
    df : pd.DataFrame
    col : str, optional. Single column to correlate with all other columns. If None, all correlations are computed.
    method : str, optional. Correlation method. Default is 'spearman'.
    alpha : float, optional. Significance level. Default is 0.05.
    ns_to_nan : bool, optional. If True, non-significant correlations are set to NaN. Default is True.
    correct_by_multiple_comp : str, optional. If not None, correct p-values for multiple comparisons. Default is 'by' (benjamini-yekutieli).
    """
    import scipy.stats as ss
    corr_func = getattr(ss, f"{method}r")
    c = {}
    p = {}
    coltypes = df.dtypes
    numerical_columns = coltypes != 'object'
    categorical_columns = coltypes == 'category'
    if method == 'spearman':
        valid_columns = numerical_columns | categorical_columns
    else:
        valid_columns = numerical_columns & (~categorical_columns)
    valid_columns = valid_columns[valid_columns].index
    if col is not None:
        col_iterator_1 = [col]
        col_iterator_2 = tqdm(valid_columns)
    else:
        col_iterator_1 = tqdm(valid_columns)
        col_iterator_2 = valid_columns

    for col1 in col_iterator_1:
        for col2 in col_iterator_2:
            if (col1, col2) in c or (col2, col1) in c:
                continue
            elif col1 == col2:
                c[(col1, col2)] = 1.0
                p[(col1, col2)] = 0
            else:
                corr, pval = corr_func(*(df[[col1, col2]].dropna().values.T))
                c[(col1, col2)] = corr
                c[(col2, col1)] = corr
                p[(col1, col2)] = pval
                p[(col2, col1)] = pval
    c = pd.Series(c).unstack()
    p = pd.Series(p).unstack()
    if correct_by_multiple_comp is not None:
        p_corrected = ss.false_discovery_control(p.values.ravel(), method=correct_by_multiple_comp)
        p_corrected = pd.DataFrame(p_corrected.reshape(p.shape), columns=p.columns, index=p.index)
        if ns_to_nan:
            c[p_corrected > alpha] = np.NaN
    else:
        p_corrected = None
        if ns_to_nan:
            c[p > alpha] = np.NaN
    return c, p, p_corrected
