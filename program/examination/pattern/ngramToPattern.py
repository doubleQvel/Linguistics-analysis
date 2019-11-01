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
rfpatlist=basepath.format("gram{}/pattern/{}/patternlist.xlsx")
wfpattern= basepath.format("gram{}/pattern/{}/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[:,2].tolist()
titens   = locateDf.iloc[:,0].tolist()
pages    = pageDf.iloc[:,0].tolist()

phonemes=["all","cvc","vcv"]
phcounter=[[],[],[]]
phindex=[[],[],[]]
phlists=[[],[],[]]
for i in range(3):
    gramlistDf=pd.read_excel(rfpatlist.format(gramname,phonemes[i]),sheet_name=0,header=0, index_col=0,dtype=str)
    phindex[i]=list(gramlistDf.index)
    phcounter[i]=[[0 for phi in phindex[i]]for locate1 in locates]
del gramlistDf
#変遷前ごとで呼び出したほうが良さそうだ
for si,(soutei,locate) in enumerate(zip(titens,locates)):
    print(locate)
    for page in pages:
        gramDf=pd.read_excel(rfgram.format(gramname,page),sheet_name=None,header=0, index_col=0,dtype=str)
        # print(page)
        sgrams=gramDf[soutei].values
        if np.sum(sgrams == "-9") != 0:
            continue
        for ti,changed in enumerate(titens):
            # print(soutei,changed)
            cgrams=gramDf[changed].values
            if np.sum(cgrams == "-9") != 0:
                continue
            if gramnumber == 1:
                phlists[1]=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==0]
                phlists[2]=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==1]
            else:
                phlists[1]=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==1]
                phlists[2]=[" ".join(sgram)+"->"+" ".join(cgram) for di,(sgram,cgram) in enumerate(zip(sgrams,cgrams)) if di%2==0]
            phlists[0]=phlists[1]+phlists[2]
            for j in range(3):
                for gram in list(set(phlists[j])):
                    ind=phindex[j].index(gram)
                    phcounter[j][ti][ind]+=phlists[j].count(gram)
    for j in range(3):
        print("書き込み{}".format(j))
        with pd.ExcelWriter(wfpattern.format(gramname,phonemes[j],locate), engine='openpyxl') as writer:
            wdf=pd.DataFrame(phcounter[j],index=locates, columns=phindex[j])
            wdf=wdf.T
            wdf.to_excel(writer,sheet_name=locate) #シート名[地点名]
        phcounter[j]=[[0 for phi in phindex[j]]for locate1 in locates]

