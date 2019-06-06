# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys

args=sys.argv
gramnumber=int(args[1])
gramname=""
if gramnumber == 1:
    gramname = "Uni"
elif gramnumber == 2:
    gramname = "Bi"
elif gramnumber == 3:
    gramname = "Tri"

basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfgram   = basepath.format("gram{}/words/{}.xlsx")
wfgram   = basepath.format("gram{}/other/grams/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

cvclists=[]
vcvlists=[]
alllists=[]

for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=None,header=0, index_col=0,dtype=str)
    for si,soutei in enumerate(titens):
        if gramnumber == 1:
            newcvclist=[" ".join(grams) for di,grams in enumerate(list(gramDf[soutei].values)) if di%2==0 and list(grams).count("-9")==0]
            newvcvlist=[" ".join(grams) for di,grams in enumerate(list(gramDf[soutei].values)) if di%2==1 and list(grams).count("-9")==0]
        else:
            newcvclist=[" ".join(grams) for di,grams in enumerate(list(gramDf[soutei].values)) if di%2==1 and list(grams).count("-9")==0]
            newvcvlist=[" ".join(grams) for di,grams in enumerate(list(gramDf[soutei].values)) if di%2==0 and list(grams).count("-9")==0]
        cvclists=cvclists+newcvclist
        cvclists=list(set(cvclists))
        vcvlists=vcvlists+newvcvlist
        vcvlists=list(set(vcvlists))
        alllists=alllists+newcvclist+newvcvlist
        alllists=list(set(alllists))

phonemes=["all","cvc","vcv"]
phlists=[alllists,cvclists,vcvlists]
for i in range(3):
    with pd.ExcelWriter(wfgram.format(gramname,phonemes[i]), engine='openpyxl') as writer:
        wdf=pd.DataFrame(phlists[i],index=list(range(len(phlists[i]))), columns=["grams"])
        wdf=wdf.sort_values("grams")
        wdf.to_excel(writer,sheet_name="{}grams".format(phonemes[i])) #シート名[地点名]


