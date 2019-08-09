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
currentpath=currentpath.split("/")
basepath="/".join(currentpath[0:currentpath.index("test")+1])
# basepath=basepath+"/data/ryukyu/{}"
basepath="/Users/kazuki/Documents/Study/test/data/ryukyu4/{}"
rfword   = basepath.format("parameter/sheetlist.xlsx")
rf= basepath.format("parameter/phs2.xlsx")
wf= basepath.format("gram{}/phoneme/{}.xlsx")

pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)
pages    = pageDf.iloc[:,0].tolist()

df=pd.read_excel(rf,sheet_name=None,header=0,index_col=0)
shNs=list(df.keys())
locs=list(df[shNs[0]].index)
locations=list(df[shNs[0]].index)
n=gramnumber
for si,shN in enumerate(shNs):
    tokenlist=[0 for j in locs]
    for j,loc in enumerate(locs):
        text=list(map(str,df[shN].iloc[j,:]))
        # print(text)
        # if n > 1:
        #     text = ["<b>"]+list(text)
        if "." not in text:
            text.append(".")
        saku=text.index(".")
        # if n > 1:
        #     text[saku]="<e>"
        # else:
        #     saku=saku-1
        tokenlist[j]=[" ".join(text[i:i+n*5]) for i in range(0,len(text),5) if saku+1 >= i+n*5]
    # print(shN,tokenlist[0])
    with pd.ExcelWriter(wf.format(gramname,pages[si])) as writer:
            wdf=pd.DataFrame(tokenlist,index=locations,columns=list(range(len(tokenlist[0]))))
            wdf=wdf.T
            wdf.to_excel(writer,sheet_name=pages[si])
