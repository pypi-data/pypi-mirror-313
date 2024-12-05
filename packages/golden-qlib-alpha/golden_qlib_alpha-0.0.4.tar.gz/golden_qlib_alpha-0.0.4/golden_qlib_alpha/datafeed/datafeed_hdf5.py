# encoding:utf8
import datetime

import pandas as pd

from golden_qlib_alpha.common import Singleton
from golden_qlib_alpha.config import DATA_DIR_HDF5_ALL
from loguru import logger

@Singleton
class Hdf5DataFeed:
    def __init__(self, db_name='index.h5'):
        logger.info(f'{self.__class__.__name__} 初始化...')
        self.code_dfs = {}

    def get_df(self, code, start_index=None, end_index=None, cols=None):
        if code in self.code_dfs:
            logger.debug(f'从内存里读取 {code}')
            df = self.code_dfs[code]
            if start_index is not None and end_index is not None:
                df = df.loc[start_index:end_index]
            return df

        with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
            logger.debug(f'从HDF5里读取 {code}')
            if cols is None:
                cols = ['open', 'high', 'low', 'close', 'volume', 'code', 'turn']
            df = store[code][cols]
        
        if start_index is not None and end_index is not None:
            df = df.loc[start_index:end_index]
        
        self.code_dfs[code] = df
        return df

    def get_one_df_by_codes(self, codes):
        dfs = [self.get_df(code) for code in codes]
        df_all = pd.concat(dfs, axis=0)
        df_all.dropna(inplace=True)
        df_all.sort_index(inplace=True)
        return df_all

    def get_returns_df(self, codes):
        df = self.get_one_df_by_codes(codes)
        all_close = pd.pivot_table(df, index='date', values='close', columns='code')
        returns_df = all_close.pct_change()
        returns_df.dropna(inplace=True)
        return returns_df

    def get_returns_df_ordered(self, codes):
        dfs = []
        for code in codes:
            df = self.get_df(code, cols=['close'])
            close = df['close']
            close.name = code
            dfs.append(close)
        all_close = pd.concat(dfs, axis=1)
        returns_df = all_close.pct_change()
        returns_df.dropna(inplace=True)
        return returns_df

if __name__ == '__main__':
    feed = Hdf5DataFeed()
    feed2 = Hdf5DataFeed()  # 这里feed2会与feed相同，因为是单例模式
    print(feed.get_df('159928.SZ'))
    df = feed.get_one_df_by_codes(['159928.SZ', '510300.SH'])
    print(df)