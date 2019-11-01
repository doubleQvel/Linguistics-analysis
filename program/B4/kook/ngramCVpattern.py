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

cvclists=[[],[]]
vcvlists=[[],[]]
allpatterns=[[],[]]
for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    rf=basepath.format("data/gramTri/words/{}.xlsx")
    goiDf=pd.read_excel(rf.format(page),sheet_name=None,header=0, index_col=0)
    print(page)
    for si,soutei in enumerate(titens):
        for ti,changed in enumerate(titens):
            for i in range(len(goiDf[changed].index)):
                moto=" ".join(map(str,goiDf[soutei].iloc[i,].tolist()))
                hikaku=" ".join(map(str,goiDf[changed].iloc[i,].tolist()))
                if "-9" in moto or "-9" in hikaku:
                    break
                if i % 2 == 0:
                    tmplists=vcvlists
                else:
                    tmplists=cvclists
                tmpP=[moto+"->"hikaku for moto,hikaku in zip(tmplists[0],tmplists[1])]
                if moto+"->"+hikaku not in tmpP:
                    tmplists[0].append(moto)
                    tmplists[1].append(hikaku)

allpatterns=[[phoneme for phoneme in cvc] for cvc in cvclists]
tmpP=[moto+"->"hikaku for moto,hikaku in zip(allpatterns[0],allpatterns[1])]
for moto,hikaku in zip(vcvlists[0],vcvlists[1]):
    if moto+"->"+hikaku not in tmpP:
        allpatterns[0].append(moto)
        allpatterns[1].append(hikaku)

wfall=basepath.format("data/gramTri/other/allpatterns.xlsx")
wfcvc=basepath.format("data/gramTri/other/cvcpatterns.xlsx")
wfvcv=basepath.format("data/gramTri/other/vcvpatterns.xlsx")

with pd.ExcelWriter(wfall, engine='openpyxl') as writer:
    tmindex=[moto+"->"+hikaku for moto,hikaku in zip(allpatterns[0],allpatterns[1])]
    wdf=pd.DataFrame(allpatterns,index=["before","after"], columns=tmindex)
    wdf=wdf.T
    wdf=wdf.sort_values("before")
    wdf.to_excel(writer,sheet_name="allPatterns") #シート名[地点名]

with pd.ExcelWriter(wfcvc, engine='openpyxl') as writer:
    tmindex=[moto+"->"+hikaku for moto,hikaku in zip(cvclists[0],cvclists[1])]
    wdf=pd.DataFrame(cvclists,index=["before","after"], columns=tmindex)
    wdf=wdf.T
    wdf=wdf.sort_values("before")
    wdf.to_excel(writer,sheet_name="cvcPatterns") #シート名[地点名]

with pd.ExcelWriter(wfvcv, engine='openpyxl') as writer:
    tmindex=[moto+"->"+hikaku for moto,hikaku in zip(vcvlists[0],vcvlists[1])]
    wdf=pd.DataFrame(vcvlists,index=["before","after"], columns=tmindex)
    wdf=wdf.T
    wdf=wdf.sort_values("before")
    wdf.to_excel(writer,sheet_name="vcvPatterns") #シート名[地点名]


