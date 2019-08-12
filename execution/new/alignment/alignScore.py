# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os
#Example wordSpread2.py gramnumber=1
# args=sys.argv
# gramnumber=int(args[1])
# gramname=str(args[1])

#カレントディレクトリ
currentpath=os.getcwd()
currentpath=currentpath.split("/")
basepath="/".join(currentpath[0:currentpath.index("test")+1])

rf= basepath.format("parameter/lpw2.xlsx")
wf= basepath.format("alignment/{}.xlsx")


df=pd.read_excel(rf,sheet_name=None,header=0,index_col=0)
shNs=list(df.keys())
locs=list(df[shNs[0]].index)
locations=list(df[shNs[0]].iloc[:,0])

for shN in shNs:
    scores=np.zeros((len(locs),len(locs)))
    wordDf=df[shN]
    for si,soutei in enumerate(locations):
        stext=list(wordDf.iloc[si,3:].values)
        if "-9" in stext:
            continue
        for tj,change in enumerate(locations):
            ctext=list(wordDf.iloc[tj,3:].values)
            if "-9" in ctext:
                continue
            for s,c in zip(stext,ctext):
                # print(s,c)
                if s != c:
                    print(s,c)
                    scores[si][tj]+=1
    with pd.ExcelWriter(wf.format(shN)) as writer:
            wdf=pd.DataFrame(scores,index=locations,columns=locations)
            wdf=wdf.T
            wdf.to_excel(writer,sheet_name=shN)
