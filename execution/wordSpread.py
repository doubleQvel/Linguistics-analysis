# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np

import os
import sys

from myPMosule import wordProcess

args=sys.argv

gramnumber=int(args[1])
gramname=str(args[1])
#カレントディレクトリ
currentpath=os.getcwd()
basepath="/".join(currentpath[0:-1])
basepath=basepath+"/data/ryukyu/{}"
# basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rf= basepath.format("parameter/lpw.xlsx")
wf= basepath.format("gram{}/words/{}.xlsx")

allData=wordProcess.WordSpreader(rf)

columname=list(range(gramnumber))
for i,shN in enumerate(allData.shNs):
    allData.tokener(i,gramnumber)
    #ファイル書き込み
    with pd.ExcelWriter(wf.format(gramname,shN)) as writer:
        for j,raw in enumerate(allData.raws):
            indexname=index=list(range(len(allData.tokenlist[j])))
            wdf=pd.DataFrame(allData.tokenlist[j],index=indexname, columns=columname)
            wdf.to_excel(writer,sheet_name=raw)
