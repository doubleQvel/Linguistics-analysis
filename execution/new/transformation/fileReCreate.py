# coding: utf-8
#todo
#ディレクトリを支持
#ディレクトリ内のファイル名を取得
#1行ずつ読み込み、新しい配列に追加
#ファイルを単語ごとに作成(行は地点名)多分7地点ほど
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os

#カレントディレクトリ
import glob

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:-3])+"/data/ryukyu4/{}"
# print(basepath)
#ファイル名取得
oldFNs=glob.glob(basepath.format("狩俣調査票2/*"))
FNs=[]
for fn in oldFNs:
    FNs.append(fn.split("/")[-1])
print(FNs)
#地点名取得
locs=[fn.split(".")[0] for fn in FNs]
#ファイル読み込み
dfs=[0 for fn in FNs]
for i,fn in enumerate(FNs):
    dfs[i]=pd.read_excel(basepath.format("狩俣調査票2/"+fn), sheet_name=0, header=0, index_col=0)
#行数確認
wordsLen=len(list(dfs[0].index))
words=list(dfs[0].iloc[:,26+6-2])
# print(wordsLen)
# print(dfs[0].head)
# print(list(dfs[0].iloc[:,26+6-2]))
#1行ずつ読み込み変換
for iw,word in enumerate(words):
    wlist=[0 for fn in FNs]
    for i,fn in enumerate(FNs):
        wlist[i]=list(dfs[i].iloc[iw,[6-2,7-2]])
    #ファイル作成
    print(wlist)
    wfn="狩俣調査票単語別/{}.xlsx".format(word)
    print(wfn)
    with pd.ExcelWriter(basepath.format(wfn), engine='openpyxl') as writer:
        wdf=pd.DataFrame(wlist,index=locs, columns=["音韻表記1","音韻表記2"])
        wdf.to_excel(writer,sheet_name="発音") #シート名[地点名]