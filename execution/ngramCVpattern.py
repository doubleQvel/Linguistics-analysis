# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys

args=sys.argv
gramnumber=int(args[1])
gramname=str(args[1])
#カレントディレクトリ
currentpath=os.getcwd()
basepath="/".join(currentpath[0:-1])
basepath=basepath+"/data/ryukyu/{}"
# basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfgram   = basepath.format("gram{}/words/{}.xlsx")
wfpattern= basepath.format("gram{}/pattern/{}/patternlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

cvclists=[]
vcvlists=[]
alllists=[]
for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=list(range(1,96)),header=0, index_col=0,dtype=str)
    for si,soutei in enumerate(titens):
        sgrams=list(gramDf[si+1].values)
        for ti,changed in enumerate(titens):
            cgrams=list(gramDf[ti+1].values)
            if gramnumber == 1:
                newcvclist=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==0 and (list(sgram).count("-9")==0 and list(cgram).count("-9")==0)]
                newvcvlist=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==1 and (list(sgram).count("-9")==0 and list(cgram).count("-9")==0)]
            else:
                newcvclist=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==1 and (list(sgram).count("-9")==0 and list(cgram).count("-9")==0)]
                newvcvlist=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==0 and (list(sgram).count("-9")==0 and list(cgram).count("-9")==0)]
            cvclists=cvclists+newcvclist
            cvclists=list(set(cvclists))
            vcvlists=vcvlists+newvcvlist
            vcvlists=list(set(vcvlists))
            alllists=alllists+newcvclist+newvcvlist
            alllists=list(set(alllists))

phonemes=["all","cvc","vcv"]
phlists=[alllists,cvclists,vcvlists]

for i in range(3):
    with pd.ExcelWriter(wfpattern.format(gramname,phonemes[i]), engine='openpyxl') as writer:
        wdf=pd.DataFrame(phlists[i],index=phlists[i], columns=["pattern"])
        wdf=wdf.sort_values("pattern")
        wdf.to_excel(writer,sheet_name="{}pattern".format(phonemes[i])) #シート名[地点名]

