# 项目用途

参考ailabx和qlib，优化了一些代码，将qlib因子计算独立出来使用。并简化使用方法。

# 用法设计

## 数据 
使用内置的下载数据工具或使用自有数据源,会默认下载几个ETF数据，data_update可用传入codes列表。
```
from golden_qlib_alpha.data.data_update import data_update
def test():
    data_update()

if __name__ == '__main__':
    test()
```


## 计算因子

```
from golden_qlib_alpha.datafeed.dataloader import Dataloader

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
```

用户可以将因子写在用户指定的csv中:
```
因子名，因子表达式
feature1,$close/Ref($close,20)-1
```
label设置：
```
label0,Ref($close, -5)/Ref($close, -1) - 1
```

读取csv文件，并对指定的数据开展这些表达式的计算。

## 因子分析

注意：
alphalens要安装alphalens-reloaded版本
```
pip install alphalens-reloaded
```

因子分析使用方法见tests目录的"test-alphalens.ipynb"