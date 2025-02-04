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
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

rf= basepath.format("parameter/lpw.xlsx")
wf=basepath.format("parameter/lpw2.xlsx")

df=pd.read_excel(rf,sheet_name=None)
shNs=list(df.keys())
# print(shNs)
raws=list(df[shNs[0]].index)
columns=list(df[shNs[0]].columns)
columns[0]="地点"
# print(raws)
# print(columns)
# print(columns)
for si,shN in enumerate(shNs):
    df[shN]=df[shN].astype("str")
    for j in range(3,8*2+3):
        if (j%2)==1:
            # 条件 (df[:,j]=="-1")
            # print(df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]])
            df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]]="-c"
        else:
            # df.iloc[(df.iloc[:,j]=="-1"),j]="-v"
            # print(df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]])
            df[shN].loc[(df[shN].iloc[:,j]=="-1"),columns[j]]="-v"
    tmp=list(df[shN].iloc[0,:])
    # print(tmp)
    tmpa=tmp.index(".")
    df[shN].loc[(df[shN].iloc[:,1]=="-9"),columns[3:tmpa]]="-9"
    df[shN].loc[(df[shN].iloc[:,1]=="-9"),columns[1]]=df[shN].iat[0,1]
    df[shN].loc[(df[shN].iloc[:,2]=="-9"),columns[2]]=df[shN].iat[0,2]
    # print(shN)
    for j in range(3,tmpa):
        # print(df[shN].loc[df[shN].iloc[:,j]==".",columns[j]])
        df[shN].loc[df[shN].iloc[:,j]==".",columns[j]]="-9"
    # df[shN][df[shN]==" "]="."
    for j in range(tmpa,8*2+3):
        df[shN].iloc[:,j]="."
with pd.ExcelWriter(wf) as writer:
    for si,shN in enumerate(shNs):
        df[shN].to_excel(writer,sheet_name=shN)
