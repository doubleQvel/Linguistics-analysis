# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np

import os
import sys

from myPMosule import wordProcess
#Example wordSpread.py gramnumber=1
args=sys.argv

gramnumber=int(args[1])
gramname=str(args[1])
#カレントディレクトリ
currentpath=os.getcwd()
basepath="/".join(currentpath[0:-1])
basepath=basepath+"/data/ryukyu/{}"
# basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rf=basepath.format("rule2.xlsx")
wf=basepath.format("gram{}/wordsList.xlsx".format(gramnumber))
wf2=basepath.format("gram{}/patternList.xlsx".format(gramnumber))

cdf=pd.read_excel(rf,sheet_name=3)
vdf=pd.read_excel(rf,sheet_name=1)

clist=list(cdf.index)+"<e>"
vlist=list(vdf.index)+"<b>"
cn=len(clist)
vn=len(vlist)
cdf=pd.DataFrame(clist,index=list(range(cn)),columns=[0])
vdf=pd.DataFrame(vlist,index=list(range(vn)),columns=[0])

p=[clist,vlist]
numbers=[cn,vn]
cvci=[[1 for i in range(2)] for i in range(gramnumber)]
vcvi=[[1 for i in range(2)] for i in range(gramnumber)]
for i in range(gramnumber):
    #repeat -> 右側へ数える
    for j in range(i+1,gramnumber):
        cvci[i][0]=cvci[i][0]*p[j%2]
        vcvi[i][0]=vcvi[i][0]*p[(j+1)%2]
    #array -> 左がわへ数える
    for j in range((i-1)-1,-1,-1):
        cvci[i][1]=cvc[i][1]*p[j%2]
        vcvi[i][1]=vcv[i][1]*p[(j+1)%2]
#cvc,vcvリストの作成
cvcs=[0 for i in range(gramnumber)]
vcvs=[0 for i in range(gramnumber)]
for i in range(gramnumber):
    #増やす
    a=np.repeat(p[i%2],cvci[i][0])
    b=np.array(a*cvci[i][1])
    cvcs[i]=b
    a=np.repeat(p[(i+1)%2],vcvi[i][0])
    b=np.array(a*vcvi[i][1])
    vcvs[i]=b
cdf=pd.DataFrame(cvcs)
vdf=pd.DataFrame(vcvs)
for i in range(gramnumber):
    if i == 0:
        cvclist=cdf.iloc[:,i]
        vcvlist=vdf.iloc[:,i]
    else:
        cvclist=cvclist+" "+cdf.iloc[:,i]
        vcvlist=vcvlist+" "+vdf.iloc[:,i]
with pd.ExcelWriter(wf.format(gramname,shN)) as writer:
    wdf1=pd.DataFrame(cvclist)
    # wdf=wdf.T
    wdf.to_excel(writer,sheet_name="cvc")
    wdf2=pd.DataFrame(vcvlist)
    wdf2.to_excel(writer,sheet_name="vcv")

#パターン作成
# cvcpattern=[]
# vcvpattern=[]
# for i in list(wdf.values):
