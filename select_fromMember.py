# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 19:49:50 2018

@author: Administrator
"""

import pandas as pd
data=pd.read_csv(open("F:\国赛论文\各任务最近30个会员标号.csv"))
member=[]
for i in range(1877):
    member.append([])

for i in range(len(data)):
    for j in data.iloc[i].values:
        member[j].append(i)
member=pd.DataFrame(member).to_csv("F:\国赛论文\各会员最近30个会员标号.csv")