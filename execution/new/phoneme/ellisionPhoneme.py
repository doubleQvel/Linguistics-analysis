# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os

#Example wordSpread.py gramnumber=1
# args=sys.argv
# gramnumber=int(args[1])
# gramname=str(args[1])

#カレントディレクトリ
currentpath=os.getcwd()
currentpath=currentpath.split("/")
basepath="/".join(currentpath[0:currentpath.index("test")+1])
# print(basepath)
# basepath=basepath+"/data/ryukyu/{}"
basepath="/Users/kazuki/Documents/Study/test/data/ryukyu4/{}"
rf= basepath.format("parameter/phs.xlsx")
wf= basepath.format("parameter/phs2.xlsx")

df=pd.read_excel(rf,sheet_name=None,header=0,index_col=0)
shNs=list(df.keys())
# print(shNs)
raws=list(df[shNs[0]].index)
columns=list(df[shNs[0]].columns)
# columns[0]="地点"
# print(raws)
# print(columns)
# print(columns)
for si,shN in enumerate(shNs):
    df[shN]=df[shN].astype("str")
    # for j in range(3,8*2+3):
    #     if (j%2)==1:
    #         df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]]="-c"
    #     else:
    #         df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]]="-v"
    tmp=list(df[shN].iloc[0,:])
    # print(tmp)
    tmpa=tmp.index(".")
    df[shN].loc[(df[shN].iloc[:,1]=="-9"),columns[:tmpa]]="-9"
    # df[shN].loc[(df[shN].iloc[:,1]=="-9"),columns[1]]=df[shN].iat[0,1]
    # df[shN].loc[(df[shN].iloc[:,2]=="-9"),columns[2]]=df[shN].iat[0,2]
    # print(shN)
    for j in range(tmpa):
        # print(df[shN].loc[df[shN].iloc[:,j]==".",columns[j]])
        df[shN].loc[df[shN].iloc[:,j]==".",columns[j]]="-9"
    # df[shN][df[shN]==" "]="."
    df[shN].iloc[:,tmpa:]="."
    # for j in range(tmpa,8*2+3):
    #     df[shN].iloc[:,j]="."
with pd.ExcelWriter(wf) as writer:
    for si,shN in enumerate(shNs):
        df[shN].to_excel(writer,sheet_name=shN)