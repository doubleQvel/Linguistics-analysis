
# coding: utf-8

# # やること
#
# 1.IPA認識した発音の読み込み
# 2.変換

# In[31]:


import pandas as pd
import openpyxl
import numpy as np
import copy
import sys
import os

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

# rfcnsts=basepath.format("parameter/consonants-list.csv")
# rfvws  =basepath.format("parameter/vowels-list.csv")
rfconvert=basepath.format("IPA組み合わせ変換.xlsx")
rforg  =basepath.format("単語分解/{}.xlsx")

convertDf=pd.read_excel(rfconvert,sheet_name=None,header=0)
cnstsDf=convertDf["子音・代替文字対応表"]
vwsDf=convertDf["母音・代替文字対応表"]
espectDf=convertDf["特別変換"]

for i in list(cnstsDf.loc[cnstsDf["代替文字"].isnull(),"代替文字"].keys()):
    cnstsDf.iloc[i,1]=cnstsDf.iloc[i-1,1]

fileNames=["222_?? 票_第２伊江???? (1)","228_???_?????? ま市屋慶名 (1)",
            "260_???_?????? 味村阿嘉島 (1)","269_?? 票_第２宮古?? ?(1)",
            "273_?? 票_第２宮古伊良部島国仲 (1)","276_?? 票_第２石垣??? (1)",
            "277_?? 票_第２石垣???? (1)"]
for fn in fileNames:
    orgDf=pd.read_excel(rforg.format(fn),header=0,index_col=0)
    maxlength=len(orgDf.iloc[0,1:])
    conphs=[["." for j in range(maxlength)] for  i in orgDf.index]
    ipas=list(cnstsDf.iloc[:,0].values)+list(vwsDf.iloc[:,0].values)
    trans=list(cnstsDf.iloc[:,1].values)+list(vwsDf.iloc[:,1].values)
    for i in orgDf.index:
        onin=list(orgDf.iloc[i,1:])
    #     print(onin)
        print(fn,onin)
        if "-1" in onin:
            conphs[i][0]="-1"
            continue
        for j,oto in enumerate(onin):
            if oto == ".":
                break
    #         for comb in zip(combinations):
    #             if oto == comb:
    #                 conphs[i][j]=
    #                 print(oto,comb)
    #                 continue
            IPAind=ipas.index(oto)
            conphs[i][j]=trans[IPAind]
    #         print(oto,conphs[i][j])
        if "無し" in conphs[i]:
            conphs[i].remove("無し")
            conphs[i].append(".")
        print(onin,conphs[i])

    symbols=["{}音".format(i+1) for i in range(maxlength)]
    convertDf=pd.DataFrame(conphs,index=list(range(len(orgDf))),columns=symbols)

    newOninDf=pd.concat([orgDf, convertDf], axis=1)

    wfonin=basepath.format("真単語分解/{}.xlsx")
    with pd.ExcelWriter(wfonin.format(fn), engine='openpyxl') as writer:
        newOninDf.to_excel(writer,sheet_name="Sheet1")

