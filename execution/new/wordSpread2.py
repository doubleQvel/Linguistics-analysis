# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os
#Example wordSpread2.py gramnumber=1
args=sys.argv
gramnumber=int(args[1])
gramname=str(args[1])

#カレントディレクトリ

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

rf= basepath.format("parameter/lpw2.xlsx")
wf= basepath.format("gram{}/words2/{}.xlsx")


df=pd.read_excel(rf,sheet_name=None,header=0,index_col=0)
shNs=list(df.keys())
locs=list(df[shNs[0]].index)
locations=list(df[shNs[0]].iloc[:,0])
n=gramnumber
for si,shN in enumerate(shNs):
    tokenlist=[0 for j in locs]
    for j,loc in enumerate(locs):
        text=list(map(str,df[shN].iloc[j,3:]))
        # print(text)
        if n > 1:
            text = ["<b>"]+list(text)
        if "." not in text:
            text.append(".")
        saku=text.index(".")
        if n > 1:
            text[saku]="<e>"
        else:
            saku=saku-1
        tokenlist[j]=[" ".join(text[i:i + n]) for i, char in enumerate(text) if saku+1 >= i+n]
    print(shN,tokenlist[0])
    with pd.ExcelWriter(wf.format(gramname,shN)) as writer:
            wdf=pd.DataFrame(tokenlist,index=locations,columns=list(range(len(tokenlist[0]))))
            wdf=wdf.T
            wdf.to_excel(writer,sheet_name=shN)




