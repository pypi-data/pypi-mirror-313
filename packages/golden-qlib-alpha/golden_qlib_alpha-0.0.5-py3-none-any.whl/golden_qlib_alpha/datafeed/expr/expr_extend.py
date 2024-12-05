import numpy as np

from golden_qlib_alpha.datafeed.expr.ops import PairOperator, Rolling
import pandas as pd
import statsmodels.api as sm


class RSRS(PairOperator):
    def __init__(self, feature_left, feature_right, N):
        self.N = N
        super(RSRS, self).__init__(feature_left, feature_right)

    def _load_internal(self, instrument, start_index, end_index, *args):
        series_left = self.feature_left.load(instrument, start_index, end_index)
        series_right = self.feature_right.load(instrument, start_index, end_index)

        # 确保两个序列的索引一致
        if not series_left.index.equals(series_right.index):
            raise ValueError("The indices of series_left and series_right must be the same.")

        slope = []
        R2 = []
        n = self.N
        for i in range(len(series_left)):
            if i < (self.N - 1):
                slope.append(pd.NA)
                R2.append(pd.NA)
            else:
                x = series_right.iloc[i - n + 1:i + 1]  # 使用 iloc 选择子序列
                x = sm.add_constant(x)
                y = series_left.iloc[i - n + 1:i + 1]
                regr = sm.OLS(y, x)
                res = regr.fit()
                beta = round(res.params.iloc[1], 2)  # 使用 iloc 访问斜率值
                slope.append(beta)
                R2.append(res.rsquared)

        betas = pd.Series(slope, index=series_left.index)
        betas.name = 'beta'
        r2 = pd.Series(R2, index=series_left.index)
        r2.name = 'r2'
        return betas, r2

class Norm(Rolling):
    def __init__(self, feature, N):
        super(Norm, self).__init__(feature, N, "slope")

    def _load_internal(self, instrument, start_index, end_index, *args):
        # 因子标准化
        def get_zscore(sub_series):
            mean = np.mean(sub_series)
            std = np.std(sub_series)
            return (sub_series.iloc[-1] - mean) / std  # 使用 .iloc 访问最后一个元素

        series = self.feature.load(instrument, start_index, end_index)
        series = series.fillna(0.0).astype(float)
        result = series.rolling(self.N, min_periods=100).apply(get_zscore)
        series = pd.Series(result, index=series.index)
        return series