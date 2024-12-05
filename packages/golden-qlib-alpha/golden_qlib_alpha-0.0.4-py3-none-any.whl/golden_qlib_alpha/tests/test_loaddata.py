from golden_qlib_alpha.datafeed.dataloader import Dataloader


def test1():
    d=Dataloader()
    code = '510300.SH'
    from datetime import datetime
    fields = []
    names = []
    fields += ["Ref($close, 1)/$close"]
    names += ["ROC5"]
    fields += ["RSRS($high,$low,18)"]
    names += ['RSRS']
    fields +=["Slope($close,20)"]
    names +=['Ret20']
    fields+=['$close/Ref($close,20)-1']
    names += ['Return20']
    df=d.load_one_df([code],datetime(2021,1,1),datetime(2022,10,1),names,fields)
    print(df)

def test2():
    code = '510300.SH'
    fields = []
    names = []
    fields += ["Ref($close, 1)/$close"]
    names += ["ROC5"]
    fields += ["RSRS($high,$low,18)"]
    names += ['RSRS']
    fields +=["Slope($close,20)"]
    names +=['Ret20']
    fields+=['$close/Ref($close,20)-1']
    names += ['Return20']
    df=Dataloader().load([code],'2021-01-01','2022-10-01',names,fields)
    print(df)

if __name__ == '__main__':
    test2()