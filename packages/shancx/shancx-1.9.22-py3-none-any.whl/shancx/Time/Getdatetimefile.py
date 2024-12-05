
import glob
import os
import numpy as np
import traceback

# 获取指定路径下所有文件
paths = glob.glob("/root/data/ec_filter_npy_data/*")  

# 遍历每个文件路径
for p in paths:
    try:
        # 尝试加载.npy文件
        data = np.load(p)
    except Exception as e:
        # 如果读取失败，打印错误信息并删除文件
        print(f"Error loading {p}: {traceback.format_exc()}")
        os.remove(p)
        print(f"Deleted file: {p}")


def GetMulData(conf):
    sCST = conf[0]
    eCST = conf[0]
    sCSTstr = sCST.strftime("%Y%m%d%H%M%S") 


from shancx import Mul_sub
import argparse
import datetime
import pandas as pd
def options():
    parser = argparse.ArgumentParser(description='examdatabasedata')
    parser.add_argument('--times', type=str, default='202411100000,202411101000') 
    config= parser.parse_args()
    print(config)
    config.times = config.times.split(",")
    if len(config.times) == 1:
        config.times = [config.times[0], config.times[0]]
    config.times = [datetime.datetime.strptime(config.times[0], "%Y%m%d%H%M"),
                    datetime.datetime.strptime(config.times[1], "%Y%m%d%H%M")]
    return config
if __name__ == '__main__':
    cfg = options()
    sCST = cfg.times[0]
    eCST = cfg.times[-1]
    timeList = pd.date_range(sCST, eCST, freq='6T')  #6T 分钟 
    print(timeList)
    Mul_sub(GetMulData,[timeList],31)

"""
from shancx import crDir
import os
from shancx import loggers as logger
# Define the original and new filenames
original_file = "CR_20241117050600.npy"
new_file = "20241117050600.npy"
rootpath ="/root/autodl-tmp"
filepath = "data/radar" 
def GetMulData(conf):
    sCST = conf[0]
    # eCST = conf[0]
    sCSTstr = sCST.strftime("%Y%m%d%H%M%S")   
    outpath = os.path.join(rootpath,filepath,f"CR_{sCSTstr}00.npy")
    if os.path.exists(outpath):
        logger.info(f"outpath {outpath} is existsing ")
        print(f"outpath {outpath} existsing ")    
    crDir(outpath)
    array = np.load(f"./{original_file}")
    np.save(outpath,array)
    logger.info(f"outpath {outpath} done ")
    print(f"outpath {outpath} done ")
from shancx import Mul_sub
import argparse
import datetime
import pandas as pd
import numpy as np
def options():
    parser = argparse.ArgumentParser(description='examdatabasedata')
    parser.add_argument('--times', type=str, default='202411101000,202411150000') 
    config= parser.parse_args()
    print(config)
    config.times = config.times.split(",")
    if len(config.times) == 1:
        config.times = [config.times[0], config.times[0]]
    config.times = [datetime.datetime.strptime(config.times[0], "%Y%m%d%H%M"),
                    datetime.datetime.strptime(config.times[1], "%Y%m%d%H%M")]
    return config
if __name__ == '__main__':
    cfg = options()
    sCST = cfg.times[0]
    eCST = cfg.times[-1]
    timeList = pd.date_range(sCST, eCST, freq='6T')  #6T 分钟 
    print(timeList)
    Mul_sub(GetMulData,[timeList],48)

------------------------------------

import glob
import os
import numpy as np
import traceback
from shancx import Mul_sub
from shancx import loggers as logger

# 获取指定路径下所有文件
paths = glob.glob("/root//autodl-tmp/data/radar/*")  #E:\

# 遍历每个文件路径
def getMul_sub(conf):
    p = conf[0]
    print(p)
    try:
        # 尝试加载.npy文件
        data = np.load(p)
        print(f"Loaded {p} with shape {data.shape}")
    except Exception as e:
        # 如果读取失败，打印错误信息并删除文件
        print(f"Error loading {p}: {traceback.format_exc()}")
        logger.error(f"Error loading {p}: {traceback.format_exc()}")
        os.remove(p)
        print(f"Deleted file: {p}")
 
if __name__ == '__main__':
    paths1 = [i for i in paths if '.npy' in i]
    Mul_sub(getMul_sub,[paths1],20)

np.tile(np.load(basedata), (8, 1, 1)).reshape((8, 4200, 6200))
"""