# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:25:16 2018

@author: Administrator
"""

import numpy as np
from math import exp
import pandas as pd

def MLE(a,b):    
    #z=np.sum([(a*price[i]-b*distance[i,j])/dominators[i] for j in range(columns_size)])
    l=np.sum([(np.log(1+exp(np.sum([(a*price.iloc[i]-b*distance.iloc[i,s])/dominators[j] for s,j in enumerate(series.iloc[i].values)])))-labels[i]*np.sum([(a*price.iloc[i]-b*distance.iloc[i,s])/dominators[j] for s,j in enumerate(series.iloc[i].values)])) for i in range(indexs_size)])
    return l

#装载数据
task_filename="F:\国赛论文\附件一：已结束项目任务数据.csv"
task_meta=pd.read_csv(open(task_filename))
price=task_meta['任务标价']
distance=pd.read_csv(open('F:\国赛论文\各任务最近30个会员距离.csv'))
labels=task_meta['任务执行情况']
member_meta=pd.read_csv(open("F:\国赛论文\附件二：会员信息数据.csv"))
values=member_meta['信誉值']
quatos=member_meta['预订任务限额']
series=pd.read_csv(open("F:\国赛论文\各任务最近30个会员标号.csv"))

indexs_size=len(distance)
columns_size=distance.columns.size
opt_result=[]



a=0
b=0
for a in np.linspace(1,200,10):
    tem_result=[]
    for b in np.linspace(1,200,10):
        dominators=[]
        for j in range(len(values)):
            dominators.append(np.sum([a*price.iloc[k]-b*distance.iloc[k,j] for k in range(indexs_size)]))
        tem_result.append(MLE(a,b))
    opt_result.append(tem_result)
    print("Finish: ",a)
opt_result=pd.DataFrame(opt_result).to_csv("F:\国赛论文\暴力搜索结果.csv")