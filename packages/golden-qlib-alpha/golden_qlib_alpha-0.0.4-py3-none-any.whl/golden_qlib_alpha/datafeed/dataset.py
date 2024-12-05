import numpy as np
import datetime as dt
from golden_qlib_alpha.datafeed.dataloader import Dataloader


def get_date_by_percent(start_date, end_date, percent):
    days = (end_date - start_date).days
    target_days = np.trunc(days * percent)
    target_date = start_date + dt.timedelta(days=target_days)
    # print days, target_days,target_date
    return target_date


def split_df(df, x_cols, y_col, split_date=None, split_ratio=0.8):
    if not split_date:
        split_date = get_date_by_percent(df.index[0], df.index[df.shape[0] - 1], split_ratio)

    input_data = df[x_cols]
    output_data = df[y_col]

    # Create training and test sets
    X_train = input_data[input_data.index < split_date]
    X_test = input_data[input_data.index >= split_date]
    Y_train = output_data[output_data.index < split_date]
    Y_test = output_data[output_data.index >= split_date]

    return X_train, X_test, Y_train, Y_test


class Dataset:
    def __init__(self, symbols, feature_names, feature_fields, split_date, label_name='label', label_field=None):
        self.feature_names = feature_names
        self.feature_fields = feature_fields
        self.split_date = split_date
        self.label_name = label_name
        self.label_field = 'Sign(Ref($close,-1)/$close -1)' if label_field is None else label_field

        names = self.feature_names + [self.label_name]
        fields = self.feature_fields + [self.label_field]
        loader = Dataloader()
        self.df = loader.load_one_df(symbols, names, fields)

    def get_split_dataset(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_train, X_test, Y_train, Y_test

    def get_train_data(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_train, Y_train

    def get_test_data(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_test, Y_test


if __name__ == '__main__':
    codes = ['000300.SH', 'SPX']
    names = []
    fields = []
    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)"]
    names += ["CORR30"]

    dataset = Dataset(codes, names, fields, split_date='2020-01-01')
    X_train, Y_train = dataset.get_train_data()
    print(X_train, Y_train)
