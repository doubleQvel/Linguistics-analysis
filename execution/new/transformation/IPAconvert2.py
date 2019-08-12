
# coding: utf-8

# # やること
#
# 1.IPA認識した発音の読み込み
# 2.変換

# In[31]:


import math
import pandas as pd
import openpyxl
import numpy as np
import copy
import sys
import os
import glob

#カレントディレクトリ
currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:-3])+"/data/ryukyu4/{}"

# rfcnsts=basepath.format("parameter/consonants-list.csv")
# rfvws  =basepath.format("parameter/vowels-list.csv")
rfconvert=basepath.format("IPA組み合わせ変換.xlsx")
rforg  =basepath.format("狩俣調査票単語分割/{}.xlsx")

convertDf=pd.read_excel(rfconvert,sheet_name=None,header=0)
cnstsDf=convertDf["子音・代替文字対応表"]
vwsDf=convertDf["母音・代替文字対応表"]
espectDf=convertDf["特別変換"]

for i in list(cnstsDf.loc[cnstsDf["代替文字"].isnull(),"代替文字"].keys()):
    cnstsDf.iloc[i,1]=cnstsDf.iloc[i-1,1]

oldFNs=glob.glob(basepath.format("狩俣調査票単語分割/*"))
FNs=[]
for fn in oldFNs:
    FNs.append(fn.split("/")[-1])
# print(FNs)
FNs=[fn.split(".")[0] for fn in FNs]
# print(FNs)
# print(type(FNs))

for fn in FNs:
    orgDf=pd.read_excel(rforg.format(fn),header=0,index_col=0,dtype=str)
    print(orgDf.head)
    maxlength=len(orgDf.iloc[0,2:])
    conphs=[["." for j in range(maxlength)] for  i in orgDf.index]
    ipas=list(cnstsDf.iloc[:,0].values)+list(vwsDf.iloc[:,0].values)
    trans=list(cnstsDf.iloc[:,1].values)+list(vwsDf.iloc[:,1].values)
    for i in range(len(orgDf.index)):
        onin=list(orgDf.iloc[i,2:])
    #     print(onin)
        print(fn,onin)
        if "-1" in onin:
            conphs[i][0]="-9"
            continue
        for j,oto in enumerate(onin):
            if oto == ".":
                break
            IPAind=ipas.index(oto)
            conphs[i][j]=trans[IPAind]
    #         print(oto,conphs[i][j])
        if "無し" in conphs[i]:
            conphs[i].remove("無し")
            conphs[i].append(".")
        print(onin,conphs[i])

    symbols=["{}音".format(i+1) for i in range(maxlength)]
    convertDf=pd.DataFrame(conphs,index=orgDf.index,columns=symbols)

    newOninDf=pd.concat([orgDf.iloc[:,[0,1]], convertDf], axis=1)

    wfonin=basepath.format("狩俣調査票単語分割2/{}.xlsx")
    with pd.ExcelWriter(wfonin.format(fn), engine='openpyxl') as writer:
        newOninDf.to_excel(writer,sheet_name="Sheet1")

