# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 13:43:12 2018

@author: Administrator
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
import matplotlib.cm as cm
import numpy as np
import pandas as pd
opt_result=pd.read_csv(open("暴力搜索结果.csv"))
x=np.linspace(1,100,num=10)
y=np.linspace(1,100,num=10)
x,y=np.meshgrid(x,y)
newfunc=interpolate.Rbf(x,y,opt_result,function='multiquadric')
xnew=np.linspace(1,100,num=100)
ynew=np.linspace(1,100,num=100)
xnew,ynew=np.meshgrid(xnew,ynew)
fnew=newfunc(xnew,ynew)
ax=plt.subplot(111,projection = '3d')  
surf = ax.plot_surface(xnew, ynew, fnew, rstride=2, cstride=2, cmap=cm.coolwarm,linewidth=0.5, antialiased=True)  
ax.scatter(x,y,opt_result,c='r',marker='^')
plt.show()