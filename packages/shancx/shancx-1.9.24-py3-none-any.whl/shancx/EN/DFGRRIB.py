
from hjnwtx.examMeso import getPointIdx
import numpy as np
class envelope():
    def __init__(self,n,s,w,e):
        self.n,self.s,self.w,self.e=n,s,w,e
    def __str__(self):
        return ("n:%s,s:%s,w:%s,e:%s"%(self.n,self.s,self.w,self.e))

def cropDF(df,evn):
    return df[(df["Lat"]>evn.s)&(df["Lat"]<evn.n)&(df["Lon"]>evn.w)&(df["Lon"]<evn.e)]

def DFGTORIB(df_Station,col_flg = "PRE1",env_Range=[85.05112877980659, -85.09887122019342,-179.56702040954826,179.63297959045173],shape_v =[3404,7186] ):  
    """
    将数据框 df_Station 中的某列数据转化为一个 NumPy 数组。
    参数:
    - df_Station (pd.DataFrame): 包含气象数据的 pandas 数据框。
    - shape_v (list): 输出数组的形状，默认为 [3404, 7186]。
    - col_flg (str): 指定的数据列名称，默认为 "PRE1"。
    返回:
    - CHNMAt (np.ndarray): 具有指定形状的 NumPy 数组，表示数据的矩阵。
    """
    
    env_Range = envelope(env_Range[0],env_Range[1],env_Range[2],env_Range[3])  
    df_Station_C = cropDF(df_Station, env_Range)
    df_Station_C = df_Station_C[df_Station_C[f"{col_flg}"]<9999]
    CHNMAt = np.full(shape_v,np.nan)
    latIdx, lonIdx = getPointIdx(df_Station_C, env_Range.n,env_Range.w, 0.05)
    CHNMAt[latIdx,lonIdx] = df_Station_C[f"{col_flg}"]
    return CHNMAt
