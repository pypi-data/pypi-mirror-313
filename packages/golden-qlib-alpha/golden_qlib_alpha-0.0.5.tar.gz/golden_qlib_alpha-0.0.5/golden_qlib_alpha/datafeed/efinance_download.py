import efinance as ef
import pandas as pd
from golden_qlib_alpha.config import DATA_DIR_HDF5_ALL
from datetime import datetime
import time
# q表示前复权，h表示后复权,n表示无
def efinance_down_funds(symbols,start_date='20100101',end_date='2022118',qfq='h'):
    if qfq=='q':
        fqt=1
    elif qfq=='h':
        fqt=2
    else:
        fqt=0
    end_date=datetime.now().strftime('%Y%m%d')
    print(end_date)
    #打开基金列表
    stocks=[]
    for x in symbols:
        stocks.append(x.split('.')[0]) #efinance只需要数字
    #下载数据
    with pd.HDFStore(DATA_DIR_HDF5_ALL.resolve()) as store:
        for stock in stocks:
            df=ef.stock.get_quote_history(stock,start_date,end_date,fqt=fqt)
            print(df.tail())
            df.columns=['code_name','code','date','open','close','high','low','volume','amount','amplitude','change_percentage','change_amount','turn']
            name=str(stock)
            if name.startswith('5'):
                name+=".SH"
            else:
                name+=".SZ"
                
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index)
            df.sort_index(ascending=True, inplace=True)
            
            store[name]=df
            time.sleep(1)
    return 0

if __name__ == '__main__':
    from golden_qlib_alpha.config import DATA_DIR_HDF5_ALL

    print(DATA_DIR_HDF5_ALL.resolve())

    symbols = ['000300.SH', '000905.SH', 'SPX', '399006.SZ']
    #download_symbols(symbols, b_index=True)

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
        print(store['510300.SH'].head())