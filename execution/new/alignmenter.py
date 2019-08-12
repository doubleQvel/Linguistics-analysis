# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os
#Example wordSpread2.py

#カレントディレクトリ

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

rf= basepath.format("parameter/lpw2.xlsx")
wf= basepath.format("alignment.xlsx")


df=pd.read_excel(rf,sheet_name=None,header=0,index_col=0)
shNs=list(df.keys())
# locs=list(df[shNs[0]].index)
locates=list(df[shNs[0]].iloc[:,0])
if "XXX" in locates:
    # locs=locs.remove("XXX")
    locates.remove("XXX")
    for shN in shNs:
        df[shN]=df[shN].drop(0,axis=0)
print(shNs)
# print(locs)
print(locates)
print("ファイル読み込み完了")
wordlist=set()
for si,soutei in enumerate(locates):
    for pi,shN in enumerate(shNs):
        # print(pi)
        sgrams=list(df[shN].iloc[si,3:])
        periodind=sgrams.index(".")
        # print(periodind)
        sgrams=" ".join(list(df[shN].iloc[si,3:3+periodind]))
        # print(shN,periodind,list(df[shN].iloc[si,3:3+periodind]))
        for ti,changed in enumerate(locates):
            cgrams=" ".join(list(df[shN].iloc[ti,3:3+periodind]))
            wordlist=wordlist | set([cgrams+"->"+sgrams])
            # newdf=df[shN].iloc[ti,3:perio].str.cat(sgrams, sep='->')
            # wordlist=wordlist | set(list(newdf.iloc[1:]))
wordlist=sorted(list(wordlist))
print(wordlist)
print("リスト完成")
# print(len(wordlist))
# print("dz2 i r o p a t a->dz2 i r o p a t a" in wordlist)
phc=[[0 for i in wordlist] for j in locates]
for si,soutei in enumerate(locates):
    phl=[]
    for pi,shN in enumerate(shNs):
        # print(pi)
        sgrams=list(df[shN].iloc[si,3:])
        periodind=sgrams.index(".")
        # print(periodind)
        sgrams=" ".join(list(df[shN].iloc[si,3:3+periodind]))
        cvtm=[]
        for ti,changed in enumerate(locates):
            cgrams=" ".join(list(df[shN].iloc[ti,3:3+periodind]))
            cvtm.append(cgrams+"->"+sgrams)
        # print(cvtm)
        phl=phl+cvtm
    for gram in list(set(phl)):
        # print(gram)
        ind=wordlist.index(gram)
        phc[si][ind]+=phl.count(gram)
#変化語の特徴ベクトルの書き込み
with pd.ExcelWriter(wf, engine='openpyxl') as writer:
    wdf=pd.DataFrame(phc,index=locates, columns=wordlist)
    wdf=wdf.T
    wdf.to_excel(writer,sheet_name="vector")



