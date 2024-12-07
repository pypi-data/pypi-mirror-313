from postsql.baseconfig import *
from shancx import loggers as logger
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
    querystr = databasequerystr(sCST, eCST)
    df1d = pd.read_sql(querystr, con=engine) 
    print()