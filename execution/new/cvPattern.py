# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os

args=sys.argv
gramnumber=int(args[1])
gramname=str(args[1])

#カレントディレクトリ

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfgram   = basepath.format("gram{}/words2/{}.xlsx")
wfpattern= basepath.format("gram{}/pattern/patternlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

cvclists=set()
vcvlists=set()
alllists=set()
if "XXX" in titens:
    titens=titens.remove("XXX")
for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=0,header=0, index_col=0,dtype=str)
    if "XXX"in list(gramDf.columns):
        gramDf=gramDf.drop(columns="XXX")
    for si,soutei in enumerate(titens):
        sgrams=gramDf[soutei]
        # print(sgrams)
        for ti,changed in enumerate(titens):
            # newdf=gramDf+"->"+sgrams
            newdf=gramDf[changed].str.cat(sgrams, sep='->')
            # print(set(newdf.iloc[0::2]))
            if gramnumber ==1:
                cvclists=cvclists | set(newdf.iloc[0::2])
                vcvlists=vcvlists | set(newdf.iloc[1::2])
            else:
                cvclists=cvclists | set(newdf.iloc[1::2])
                vcvlists=vcvlists | set(newdf.iloc[0::2])
    print(pi)

phonemes=["all","cvc","vcv"]
phlists=[list(cvclists | vcvlists),list(cvclists),list(vcvlists)]

with pd.ExcelWriter(wfpattern.format(gramname), engine='openpyxl') as writer:
    for i in range(3):
        wdf=pd.DataFrame(phlists[i],index=phlists[i], columns=["pattern"])
        wdf=wdf.sort_values("pattern")
        wdf.to_excel(writer,sheet_name="{}".format(phonemes[i])) #シート名[地点名]
