# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 10:38:11 2018

@author: Administrator
"""
import pandas as pd
from scipy import spatial 
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

def beautify_result(x,y):
    return np.sum([(predict_byLab[i]==x and data.loc[i,'label']==y) for i in range(len(predict_byLab))])
    
#导入任务数据
task_filename="附件一：已结束项目任务数据.csv"
task_meta=pd.read_csv(open(task_filename))
task_xy=np.array(task_meta[['任务gps纬度','任务gps经度']])
price=np.array(task_meta['任务标价'])
tabel=np.array(task_meta['任务执行情况'])
task_tree=spatial.KDTree(task_xy)

#导入会员数据
member_filename="附件二：会员信息数据.csv"
member_meta=pd.read_csv(open(member_filename))
member_xy=np.array(member_meta[['x','y']].dropna())
member_tree=spatial.KDTree(member_xy)

#查询每一个任务附近最近的10个会员信息
mem_avedis=[]
mem_stddis=[]
task_avedis=[]
task_stddis=[]
task_aveprice=[]
mem_avevalue=[]
mem_avequato=[]
cross=[]

#plt.figure(figsize=(10,8),dpi=300)
with open('distance.csv','w') as f:
    f_csv=csv.writer(f)
    for i,task in enumerate(task_xy):
        dis,loc=member_tree.query(task,k=30)
        mem_avedis.append(np.mean(dis)*100)
        mem_stddis.append(np.std(dis)*100)
        mem_avequato.append(np.mean([i for i in member_meta.loc[loc,'预订任务限额']]))
        mem_avevalue.append(np.mean([i for i in member_meta.loc[loc,'信誉值']]))
        
        dis,loc=task_tree.query(task,k=30)
        task_avedis.append(np.mean(dis))
        task_stddis.append(np.std(dis))
        task_aveprice.append(np.mean([i for i in task_meta.loc[loc,'任务标价']])/task_meta.loc[i,'任务标价'])
        
        cross.append(task_aveprice[i]*task_avedis[i])
        #f_csv.writerow(dis)
        #sns.kdeplot(dis)
        #members=zip(dis,loc)
#print((tabel,price,mem_dis))

data=pd.DataFrame(np.concatenate(([tabel],[price],[mem_avedis],[mem_stddis],[task_avedis],[task_stddis],[task_aveprice],[cross],[mem_avevalue],[mem_avequato]),axis=0).T,columns=['label','price','ave_mem_distance','std_mem_distance','ave_task_distance','std_task_distance','ave_task_price','cross','mem_avevalue','mem_avequato'])
data['intercept']=1.0

#修复scipy1.0.0出现的错误
from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

train_cols=['price','ave_mem_distance','ave_task_distance','ave_task_price','intercept']
logit=sm.Logit(data['label'],data[train_cols])
result=logit.fit()
print(result.summary())

predict_byLab=[x>0.5 for x in result.predict(data[train_cols])]
predict_probit=pd.DataFrame(result.predict(data[train_cols]))
predict_probit.to_csv("F:\国赛论文\Logistics概率结果.csv")
#result=dict()
#result['00']=np.sum([(predict_byLab[i]==0 and data.loc[i,'label']==0) for i in range(len(predict_byLab))])
#result['01']=np.sum([(predict_byLab[i]==0 and data.loc[i,'label']==1) for i in range(len(predict_byLab))])
#result['10']=np.sum([(predict_byLab[i]==1 and data.loc[i,'label']==0) for i in range(len(predict_byLab))])
#result['11']=np.sum([(predict_byLab[i]==1 and data.loc[i,'label']==1) for i in range(len(predict_byLab))])
result=[]
result=[[beautify_result(0,0),beautify_result(0,1)],[beautify_result(1,0),beautify_result(1,1)]]
print(beautify_result(0,0),'||',beautify_result(0,1))
print('-'.center(10,'-'))
print(beautify_result(1,0),'||',beautify_result(1,1))
print('precision:',beautify_result(0,0)/(beautify_result(0,0)+beautify_result(0,1)))
print('recall:',beautify_result(0,0)/(beautify_result(0,0)+beautify_result(1,0)))
print('Accuracy:',np.mean(predict_byLab==data['label']))