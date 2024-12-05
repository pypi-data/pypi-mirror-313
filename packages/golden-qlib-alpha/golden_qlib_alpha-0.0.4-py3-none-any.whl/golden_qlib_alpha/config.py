from pathlib import Path

# 获取当前用户的home目录
HOME_DIR = Path.home()

# 定义数据存储路径为home目录下的gqlibdata目录
DATA_DIR = HOME_DIR.joinpath("gqlibdata")

DATA_DIR_HDF5 = DATA_DIR.joinpath('hdf5')
DATA_DIR_HDF5_ALL = DATA_DIR_HDF5.joinpath('all.h5')

dirs = [DATA_DIR, DATA_DIR_HDF5]
for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)



