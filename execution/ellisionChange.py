# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os

#Example wordSpread.py gramnumber=1
args=sys.argv
gramnumber=int(args[1])
gramname=str(args[1])

#カレントディレクトリ
currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"data/ryukyu4/{}"

rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfgram   = basepath.format("gram{}/words/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=None,header=0, index_col=0,dtype=str)
    for si,soutei in enumerate(titens):
        for di,grams in enumerate(gramDf[soutei].values):
            grams = list(map(str,list(grams)))
            if grams.count("-1") !=0:
                if gramnumber == 1:
                    if   di%2 == 0 and "-1" in grams:
                        gramDf[soutei].iat[di,0]="-c"
                    elif di%2 == 1  and "-1" in grams:
                        gramDf[soutei].iat[di,0]="-v"
                else:
                    ellisons=[gj for gj,gram in enumerate(grams) if gram == "-1"]
                    for gj in ellisons:
                        if   di%2==0: #v-c-v
                            if   gj%2==0:#v
                                gramDf[soutei].iat[di,gj]="-v"
                            elif gj%2==1:#c
                                gramDf[soutei].iat[di,gj]="-c"
                        elif di%2 ==1:#c-v-c
                            if   gj%2==0:#c
                                gramDf[soutei].iat[di,gj]="-c"
                            elif gj%2==1:#v
                                gramDf[soutei].iat[di,gj]="-v"
    with pd.ExcelWriter(rfgram.format(gramname,page), engine='openpyxl') as writer:
        for si,soutei in enumerate(titens):
            gramDf[soutei].to_excel(writer,sheet_name=soutei) #シート名[地点名]
