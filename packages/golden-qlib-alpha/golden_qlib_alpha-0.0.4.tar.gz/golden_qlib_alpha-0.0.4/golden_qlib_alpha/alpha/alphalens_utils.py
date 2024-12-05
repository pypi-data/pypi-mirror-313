# encoding:utf8
from alphalens.utils import get_clean_factor_and_forward_returns


# 将tears.py中的get_values()函数改为to_numpy()


def make_alphalens_datas(df, alpha_col):
    # alphalens接受的数据必须是双索引，date,code
    alpha_df = df.set_index([df.index, 'code'])
    alpha_df.sort_index(level=0, inplace=True, ascending=True)
    # 使用pivot_table把因子值，按symbol提出来
    close_df = df.pivot_table(index='date', columns='code', values='close', dropna=True)
    return alpha_df[alpha_col], close_df


if __name__ == '__main__':
    from golden_qlib_alpha.datafeed.dataloader import Dataloader
    from datetime import datetime
    df = Dataloader().load_one_df(['510300.SH'],datetime(2021,1,1),datetime(2022,10,1),
                                  names=['close', 'mom_20', 'rate'], fields=['$close',
                                                                             '$close/Ref($close,20)-1',
                                                                             '$close/Ref($close,1)-1'
                                                                             ])
    alpha_df, close_df = make_alphalens_datas(df, 'rate')
    print(alpha_df, close_df)

    from alphalens.utils import get_clean_factor_and_forward_returns

    # 将tears.py中的get_values()函数改为to_numpy()
    ret = get_clean_factor_and_forward_returns(alpha_df, close_df)
    print(ret)

    from alphalens.tears import create_returns_tear_sheet

    create_returns_tear_sheet(ret, long_short=False)
