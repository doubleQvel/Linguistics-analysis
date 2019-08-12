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
#カレントディレクトリ
currentpath=os.getcwd()
currentpath=currentpath.split("/")
basepath="/".join(currentpath[0:currentpath.index("test")+1])
# basepath=basepath+"/data/ryukyu/{}"
basepath="/Users/kazuki/Documents/Study/test/data/ryukyu4/{}"
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfgram   = basepath.format("gram{}/words2/{}.xlsx")
rfpt     = basepath.format("gram{}/pattern/patternlist.xlsx")
wfpattern= basepath.format("gram{}/pattern/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[:,2].tolist()
titens   = locateDf.iloc[:,0].tolist()
pages    = pageDf.iloc[:,0].tolist()

ph=["all","cvc","vcv"]
phc=[[],[],[]]
phi=[[],[],[]]
phl=[[],[],[]]
gramlistDf=pd.read_excel(rfpt.format(gramname),
                        sheet_name=None,header=0,
                        index_col=0,dtype=str)
for i in range(3):
    phi[i]=list(gramlistDf[ph[i]].index)
    phc[i]=[[0 for i in phi[i]]for locate1 in locates]

#1地点ごとにベクトルを作成する
grams=[0 for i in pages]
for pi,page in enumerate(pages):
    grams[pi]=pd.read_excel(rfgram.format(gramname,page),
                            sheet_name=0,header=0,
                            index_col=0,dtype=str)
    if "XXX" in list(grams[pi].columns):
        grams[pi]=grams[pi].drop(columns="XXX")
print("ファイル読み込み完了")

for si,(soutei,locate) in enumerate(zip(titens,locates)):
    phl=[[],[],[]]
    # phc[i]=[[0 for i in phi[i]]for locate1 in locates]
    for pi,page in enumerate(pages):
        sgrams=grams[pi][soutei].values
        cvtm=[]
        vctm=[]
        for ti,changed in enumerate(titens):
            cgrams=grams[pi][changed].str.cat(sgrams, sep='->')
            # print(set(newdf.iloc[0::2]))
            if gramnumber ==1:
                cvtm=cvtm + list(cgrams.iloc[0::2])
                vctm=vctm + list(cgrams.iloc[1::2])
            else:
                cvtm=cvtm + list(cgrams.iloc[1::2])
                vctm=vctm + list(cgrams.iloc[0::2])
            # print(cvtm)
        phl[1]=cvtm
        phl[2]=vctm
        phl[0]=cvtm+vctm
        # print(page)
        for j in range(3):
            for gram in list(set(phl[j])):
                # print(gram)
                ind=phi[j].index(gram)
                phc[j][si][ind]+=phl[j].count(gram)
    print(locate)
#変化語の特徴ベクトルの書き込み
for j in range(3):
    print("書き込み{}".format(j))
    with pd.ExcelWriter(wfpattern.format(gramname,ph[j]), engine='openpyxl') as writer:
        wdf=pd.DataFrame(phc[j],index=locates, columns=phi[j])
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name="vector")
