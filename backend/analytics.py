import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


def compute_hedge_ratio(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]


def compute_zscore(series, window=50):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std


def compute_adf_pvalue(series):
    return adfuller(series.dropna())[1]


def compute_rolling_correlation(x, y, window=50):
    return x.rolling(window).corr(y)
