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
rfgramlist=basepath.format("gram{}/grams/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[0:,2].tolist()
titens   = locateDf.iloc[0:,0].tolist()
pages    = pageDf.iloc[0:,0].tolist()

phonemes=["all","cvc","vcv"]
phcounter=[[],[],[]]
phindex=[[],[],[]]
phlists=[[],[],[]]
for i in range(3):
    gramlistDf=pd.read_excel(rfgramlist.format(gramname,phonemes[i]),sheet_name=0,header=0, index_col=0,dtype=str)
    phindex[i]=list(gramlistDf.iloc[:,0])
    phcounter[i]=[[0 for phi in phindex[i]] for locate in locates]

for pi,page in enumerate(pages): #各単語ごとにトライグラムの呼び出し
    gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=list(range(1,96)),header=0, index_col=0,dtype=str)
    for si,soutei in enumerate(titens):
        if gramnumber == 1:
            phlists[1]=[" ".join(grams) for di,grams in enumerate(list(gramDf[si+1].values)) if di%2==0 and list(grams).count("-9")==0]
            phlists[2]=[" ".join(grams) for di,grams in enumerate(list(gramDf[si+1].values)) if di%2==1 and list(grams).count("-9")==0]
        else:
            phlists[1]=[" ".join(grams) for di,grams in enumerate(list(gramDf[si+1].values)) if di%2==1 and list(grams).count("-9")==0]
            phlists[2]=[" ".join(grams) for di,grams in enumerate(list(gramDf[si+1].values)) if di%2==0 and list(grams).count("-9")==0]
        phlists[0]=phlists[1]+phlists[2]
        for j in range(3):
            for phi,gram in enumerate(phindex[j]):
                phcounter[j][si][phi]+=phlists[j].count(gram)
                # print(gram,phlists[j],phlists[j].count(gram),phlists[2],phlists[2].count(gram))

wfcounter=basepath.format("gram{}/counter/{}.xlsx")
for i in range(3):
    with pd.ExcelWriter(wfcounter.format(gramname,phonemes[i]), engine='openpyxl') as writer:
        wdf=pd.DataFrame(phcounter[i],index=locates, columns=phindex[i])
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name="{}counter".format(phonemes[i])) #シート名[地点名]

