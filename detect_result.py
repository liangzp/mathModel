# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:26:15 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
from math import exp

def beautify_result(x,y):
    return np.sum([(predict[i]==x and labels[i]==y) for i in range(len(predict))])

#装载数据
task_filename="F:\国赛论文\附件一：已结束项目任务数据.csv"
task_meta=pd.read_csv(open(task_filename))
price=task_meta['任务标价']
distance=pd.read_csv(open('F:\国赛论文\各任务最近30个会员距离.csv'))
labels=task_meta['任务执行情况']
quatos=pd.read_csv(open('F:\国赛论文\各任务最近30个会员额度.csv'))
values=pd.read_csv(open('F:\国赛论文\各任务最近30个会员信誉值.csv'))

indexs_size=len(distance)
columns_size=distance.columns.size
opt_result=[]

a=89
b=23
dominators=[]
probis=[]
for j in range(columns_size):
    dominators.append(np.sum([a*price.iloc[k]-b*distance.iloc[k,j] for k in range(indexs_size)]))

predict=[]
for i in range(indexs_size):
    z=np.sum([(a*price.iloc[i]-b*distance.iloc[i,j])/dominators[j] for j in range(columns_size)])
    probi=exp(z)/(1+exp(z))
    predict.append(probi>0.5)
    probis.append(probi)
    
result=[[beautify_result(0,0),beautify_result(0,1)],[beautify_result(1,0),beautify_result(1,1)]]
print(beautify_result(0,0),'||',beautify_result(0,1))
print('-'.center(10,'-'))
print(beautify_result(1,0),'||',beautify_result(1,1))
print('precision:',beautify_result(0,0)/(beautify_result(0,0)+beautify_result(0,1)))
print('recall:',beautify_result(0,0)/(beautify_result(0,0)+beautify_result(1,0)))
print('Accuracy:',np.mean(predict==labels))
probis=pd.DataFrame(probis)
probis.to_csv("F:\国赛论文\非线性模型概率结果.csv")
