
def test1():
    from golden_qlib_alpha.config import DATA_DIR_HDF5_ALL
    from golden_qlib_alpha.datafeed.efinance_download import efinance_down_funds
    import pandas as pd
    
    print(DATA_DIR_HDF5_ALL.resolve())

    etfs = ['510300.SH',  # 沪深300ETF
            '159949.SZ',  # 创业板50
            '510050.SH',  # 上证50ETF
            '159928.SZ',  # 中证消费ETF
            '510500.SH',  # 500ETF
            '159915.SZ',  # 创业板 ETF
            '512120.SH',  # 医药50ETF
            '159806.SZ',  # 新能车ETF
            '510880.SH',  # 红利ETF
            ]

    efinance_down_funds(etfs)

    with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
        print('读数据')
        print(store['510300.SH'])

def test2():
    from golden_qlib_alpha.data.data_update import data_update
    data_update()

if __name__ == '__main__':
    test2()
