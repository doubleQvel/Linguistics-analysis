# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np

basepath="/home/kazukiq/Study/{}"
rflocate = basepath.format("data/parameter/locations.xlsx")
rfword   = basepath.format("data/parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

rfall=basepath.format("data/gramTri/other/allpatterns.xlsx")
rfcvc=basepath.format("data/gramTri/other/allpatterns.xlsx")
rfvcv=basepath.format("data/gramTri/other/allpatterns.xlsx")

allDf = pd.read_excel(rfall, sheet_name=0, header=0, index_col=0)
cvcDf = pd.read_excel(rfcvc, sheet_name=0, header=0, index_col=0)
vcvDf = pd.read_excel(rfvcv, sheet_name=0, header=0, index_col=0)

allpattern=list(allDf.index)
cvcpattern=list(cvcDf.index)
vcvpattern=list(vcvDf.index)

allfeatureVector=[[[0 for pattern in allpattern] for locate in locates] for locate in locates]
cvcfeatureVector=[[[0 for pattern in cvcpattern] for locate in locates] for locate in locates]
vcvfeatureVector=[[[0 for pattern in vcvpattern] for locate in locates] for locate in locates]

for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    rf=basepath.format("data/gramTri/words/{}.xlsx")
    goiDf=pd.read_excel(rf.format(page),sheet_name=None,header=0, index_col=0)
    print(page)
    for si,soutei in enumerate(titens):
        for ti,titen in enumerate(tmtitens):
            for i in range(len(goiDf[changed].index)):
                moto=" ".join(map(str,goiDf[soutei].iloc[i,].tolist()))
                hikaku=" ".join(map(str,goiDf[changed].iloc[i,].tolist()))
                if "-9" in moto or "-9" in hikaku:
                    print("OK")
                    break
                pattern=moto+"->"hikaku
                if i%2 == 0:
                    vcvind=vcvpattern.index(pattern)
                    vcvfeatureVector[si][ti][vcvind]+=1
                else:
                    cvcind=cvcpattern.index(pattern)
                    cvcfeatureVector[si][ti][cvcind]+=1
                allind=allpattern.index(pattern)
                allfeatureVector[si][ti][allind]+=1

wfallfeature=basepath.format("data/gramTri/pattern/all/{}.xlsx")
wfcvcfeature=basepath.format("data/gramTri/pattern/cvc/{}.xlsx")
wfvcvfeature=basepath.format("data/gramTri/pattern/vcv/{}.xlsx")

for bi,bf in enumerate(locates):
    with pd.ExcelWriter(wfallfeature.format(bf), engine='openpyxl') as writer:
        wdf=pd.DataFrame(allfeatureVector[bi],index=locates, columns=allpattern)
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name=bf) #シート名[地点名]
    with pd.ExcelWriter(wfcvcfeature.format(bf), engine='openpyxl') as writer:
        wdf=pd.DataFrame(cvcfeatureVector[bi],index=locates, columns=cvcpattern)
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name=bf) #シート名[地点名]
    with pd.ExcelWriter(wfvcvfeature.format(bf), engine='openpyxl') as writer:
        wdf=pd.DataFrame(vcvfeatureVector[bi],index=locates, columns=vcvpattern)
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name=bf) #シート名[地点名]

