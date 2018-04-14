# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:24:50 2018

@author: Administrator
"""
import pandas as pd
import matplotlib.pyplot as plt

def clean(filename,del_column,check_column):
    data=pd.read_csv(open(filename))
    #data.columns=['number','x','y','price','label']
    del data[del_column]
    Q1=data.describe().iloc[4]
    Q3=data.describe().iloc[6]
    Q_min=Q1-1.5*(Q3-Q1)
    Q_max=Q3+1.5*(Q3-Q1)
    del_labels=[]
    for i in check_column:
        del_labels.extend(data.index[data.loc[:,i]<Q_min.loc[i]].values)
        del_labels.extend(data.index[data.loc[:,i]>Q_max.loc[i]].values)
    del_labels=list(set(del_labels))
    print(del_labels)
    data=data.drop(del_labels)
    data.to_csv("F:\国赛论文\data"+'\\'+filename.split('\\')[-1],encoding='gbk',index=False)
    
clean("F:\国赛论文\附件一：已结束项目任务数据.csv","任务号码",['任务gps纬度','任务gps经度','任务标价'])
clean("F:\国赛论文\附件二：会员信息数据.csv","会员编号",['x','y'])