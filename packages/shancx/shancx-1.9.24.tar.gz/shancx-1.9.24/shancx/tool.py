
import netCDF4 as nc
import numpy as np
def getPoint(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[...,latIdx, lonIdx].round(decimals=decimal)
def Get_Lat_Lon_QPF(path,Lon_data,Lat_data):
    with nc.Dataset(path) as dataNC:
        latArr = dataNC["lat"][:]
        lonArr = dataNC["lon"][:]
        if "AIW_QPF" in  path:
            pre = dataNC[list(dataNC.variables.keys())[3]][:]    
        elif "AIW_REF" in path:
            pre = dataNC[list(dataNC.variables.keys())[4]][:]   
    data = getPoint(pre , {"Lon":Lon_data,"Lat":Lat_data} , latArr[0], lonArr[0], 0.01)
    data = getPoint(pre , {"Lon":Lon_data,"Lat":Lat_data} , latArr[0], lonArr[0], 0.01)
    return data

"""   pip index  设置
mkdir .pip 进入文件夹  vim pip.conf  粘贴保存
[global]
index_url=https://pypi.tuna.tsinghua.edu.cn/simple
"""
###用于回算
"""
from main import makeAll,options
from multiprocessing import Pool
import datetime
from config import logger,output
import time
import pandas as pd
import os
from itertools import product
import threading
from shancx import Mul_sub
def excuteCommand(conf):
    cmd = conf[0]
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    cfg = options()
    isPhase = cfg.isPhase
    isDebug = cfg.isDebug
    sepSec = cfg.sepSec
    gpu = cfg.gpu
    pool = cfg.pool
    isOverwrite = cfg.isOverwrite
    timeList = pd.date_range(cfg.times[0], cfg.times[-1], freq=f"{sepSec}s")
    logger.info(f"时间段check {timeList}")
    gpuNum = 2
    eachGPU = 4
    makeListUTC = []
    for UTC in timeList:
        UTCStr = UTC.strftime("%Y%m%d%H%M")
        outpath = f"{output}/{UTCStr[:4]}/{UTCStr[:8]}/MSP2_WTX_AIW_QPF_L88_CHN_{UTCStr}_00000-00300-00006.nc"
        if not os.path.exists(outpath) or isOverwrite:
            makeListUTC.append(UTC)
    [print(element) for element in makeListUTC]
    phaseCMD = "--isPhase" if isPhase else ""
    debugCMD = "--isDebug" if isDebug else ""
    OverwriteCMD = "--isOverwrite"
    gpuCMD = f"--gpu={gpu}"
    # cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {OverwriteCMD} {gpuCMD}",makeListUTC))
    cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {gpuCMD}",makeListUTC))
    if cmdList:
        Mul_sub(excuteCommand, [cmdList], pool)
    else: 
        print("cmdList is empty, skipping the call.")
        raise ValueError("cmdList is empty, cannot execute command.")
CUDA_LAUNCH_BLOCKING=1 python makeHis.py --times 202410010042,202410110042 --gpu=0 --isDebug --sepSec 3600 --pool 5
CUDA_LAUNCH_BLOCKING=1 python makeHis1.py --times 202410010042,202410110042 --gpu=0 --isDebug --sepSec 3600 --pool 5
"""
###用于循环出日报
"""
#!/bin/bash
start_date="20241001"
end_date="20241101"
tag="scx/MQPF_Gan5_default_1112N"
current_date=$(date -d "$start_date" +%Y%m%d)
end_date=$(date -d "$end_date" +%Y%m%d)
while [ "$current_date" != "$end_date" ]; do
    start_time="$current_date"0000
    end_time="$current_date"2359
    python makeDOC_newv2.py --times $start_time,$end_time --tag $tag
    current_date=$(date -d "$current_date + 1 day" +%Y%m%d)
done
python makeDOC_newv2.py --times $end_date"0000",$end_date"2359" --tag $tag
"""
"""
frile name :launch.json
args:
{
    "version": "0.2.0",
    "configurations": [   
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
            "purpose": ["debug-in-terminal"],
            "justMyCode": false,
            "args": [  
                "--times", "202409160000,202409180000" 
            ]
        }
    ]
}

{
    "version": "0.2.0",
    "configurations": [   

        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
            "purpose": ["debug-in-terminal"],
            "justMyCode": false,
            "args": [
            "--times", "202410010042,202410020042",
            "--isDebug" ,
            "--isOverwrite", 
            "--sepSec", "3600",
            "--gpu", "0"
            ]
        }
    ]
}

"""

"""
import importlib

def get_obj_from_str(class_path: str):
    # 分割类路径，提取模块和类名
    module_name, class_name = class_path.rsplit('.', 1)
    
    # 导入模块
    module = importlib.import_module(module_name)
    
    # 获取类并返回
    return getattr(module, class_name)

# 配置字典
config = {
    "target": "torch.nn.Linear",  # 类路径
    "params": {                  # 参数字典
        "in_features": 128,
        "out_features": 64
    }
}

# 使用配置字典动态实例化对象
target_class = get_obj_from_str(config["target"])  # 获取类（torch.nn.Linear）
model = target_class(**config.get("params", dict()))  # 使用解包的参数实例化

# 打印结果
print(model)


import torch
import torch.nn as nn

# 创建一个线性层
linear = nn.Linear(in_features=128, out_features=64, bias=True)配置字典动态传参
"""