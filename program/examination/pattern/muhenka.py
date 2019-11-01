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
rfpatlist= basepath.format("gram{}/pattern/{}/patternlist.xlsx")
rfpattern= basepath.format("gram{}/pattern/{}/{}.xlsx")
wfmuhenka= basepath.format("gram{}/pattern/{}/muhenka.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[:,2].tolist()
titens   = locateDf.iloc[:,0].tolist()
pages    = pageDf.iloc[:,0].tolist()

phonemes=["all","cvc","vcv"]
phindex=[[],[],[]]
phlists=[[],[],[]]
for i in range(3):
    gramlistDf=pd.read_excel(rfpatlist.format(gramname,phonemes[i]),sheet_name=0,header=0, index_col=0,dtype=str)
    phindex[i]=list(gramlistDf.index)
    for j,ind in enumerate(phindex[i]):
        moto,hikaku=ind.split("->")
        if moto == hikaku:
            phlists[i].append(j)
del gramlistDf

for i in range(3):
    counters=[[0 for locate1 in locates] for locate in locates]
    print(phonemes[i])
    for si,soutei in enumerate(locates):
        print(soutei)
        patDf=pd.read_excel(rfpattern.format(gramname,phonemes[i],soutei),sheet_name=0,header=0, index_col=0)
        for ci,changed in enumerate(locates):
            counters[si][ci]=sum(patDf.iloc[phlists[i],ci].tolist())/sum(patDf.iloc[:,ci].tolist())
    with pd.ExcelWriter(wfmuhenka.format(gramname,phonemes[i]), engine='openpyxl') as writer:
        wdf=pd.DataFrame(counters,index=locates, columns=locates)
        wdf.to_excel(writer,sheet_name="muhenka") #シート名[地点名]
