
import glob
import numpy as np
from hjnwtx.colormap import cmp_hjnwtx
PathList = glob.glob("/mnt/wtx_weather_forecast/scx/testDBscan/2024_p/20240312/*")
path = PathList[0]
print(path) 

import numpy as np 
import matplotlib.pyplot as plt
x = np.load(path)
# for i in range(35):
    # plt.imshow(x[i])
    # plt.savefig(f"./image/a{str(i)}.png")
    # plt.show()


from hjnwtx.colormap import cmp_hjnwtx
import matplotlib.pyplot as plt
import datetime
def drawpic_com(base_up,base_down,shape_len, name="temp"): 
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    Count = shape_len
    data_all = np.concatenate([base_up,base_down], axis=0)
    fig, axs = plt.subplots(2, Count, figsize=(10*shape_len, 10))
    # data_all = data_all * 70
    for i in range(2):
        for j in range(Count):
            index = i * Count + j
            axs[i, j].imshow(data_all[index, :, :],vmax=70,vmin=0,cmap=cmp_hjnwtx["radar_nmc"])
            axs[i, j].axis('off')
    plt.tight_layout()
    plt.savefig(name +now_str + '.png')
    plt.close() 
#drawpic(x,x,35)
print("done")