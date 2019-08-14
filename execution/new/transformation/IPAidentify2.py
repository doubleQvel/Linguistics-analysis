
# coding: utf-8

# # やること
#
# 音の変換
# 1. 子音または母音の認識
# 2. 分解
# 3. 変換

# In[1]:

import math
import pandas as pd
import openpyxl
import numpy as np
import copy
import sys
import os
#カレントディレクトリ
import glob

currentpath=os.getcwd()
basepath=currentpath.split("/")
basepath="/".join(basepath[0:basepath.index("test")+1])+"/data/ryukyu4/{}"

rfcnsts=basepath.format("parameter/consonants-list.csv")
rfvws  =basepath.format("parameter/vowels-list.csv")
rforg  =basepath.format("狩俣調査票単語別/{}.xlsx")

cnstsDf=pd.read_csv(rfcnsts,sep="\t",index_col=0)
vwsDf  =pd.read_csv(rfvws  ,sep="\t",index_col=0)
oldFNs=glob.glob(basepath.format("狩俣調査票単語別/*"))
FNs=[]
for fn in oldFNs:
    FNs.append(fn.split("/")[-1])
# print(FNs)
FNs=[fn.split(".")[0] for fn in FNs]
# print(FNs)
# print(type(FNs))
if "nan" in FNs:
    FNs.remove("nan")
# for fn in FNs:
#     print(fn)

for fn in FNs:

    # print("ファイル名:{}".format(fn))

    orgDf=pd.read_excel(rforg.format(fn),sheet_name=0,header=0,index_col=0,dtype=str)

    # print(orgDf.head)

    oninDf=orgDf.iloc[:, [0,1]]

    # 音の認識をどう行う？
    splitOnin=[]
    # 備考ランのリスト
    bikou=["" for i in range(len(oninDf.index))]
    for i in range(len(oninDf.index)):
        bunkais=[]
        onin=oninDf.iat[i,0]

        # print("{}の{}番目の音韻  >  {}".format(fn,i,onin))

        # if onin=="NR" or onin=="3" or onin=="4" or onin=="5" or onin=="Y" or ("/" in onin) or (" " in onin) or ("　" in onin) or ("ɯ̈" in onin) or ("vː" in onin) or ("æː" in onin) or ("ɛ" in onin)or ("nː" in onin) or ("y" in onin) or ("ɭ" in onin) or ("uˑ" in onin) or ("ˀ" in onin) or ("ã" in onin):
        #     splitOnin.append(["-1"])
        #     continue
        if onin=="NR":
            bikou[i]="応答なし"
            splitOnin.append(["-1"])
            continue
        new_onin=onin
        if " " in new_onin or "/" in new_onin or "　" in new_onin:
            if " " in new_onin:
                kugiri=" "
            elif "/" in new_onin:
                kugiri="/"
            elif "　"in new_onin:
                kugiri="　" #全角スペース
            new_onin=new_onin.split(kugiri)[0]
        splitflag=True
        counter=1
        while splitflag:
            # print("{}回目".format(counter))
            # 子音と母音の確認
            new_cnsts=[]
            new_vws =[]
            for ci,cnst in enumerate(cnstsDf.iloc[:,0].values):
                if cnst in new_onin:
                    new_cnsts.append(cnst)
            for vi,vw in enumerate(vwsDf.iloc[:,0].values):
                if vw in new_onin:
                    new_vws.append(vw)

            # print("子音   {}".format(new_cnsts))
            # print("母音   {}".format(new_vws))

            new_cnstsInd=[new_onin.index(cnst) for cnst in new_cnsts]
            new_vwsInd =[new_onin.index(vw) for vw  in new_vws]

            # print("新しい子音の位置: {}".format(new_cnstsInd))
            # print("新しい母音の位置: {}".format(new_vwsInd))

            if len(new_cnsts) == 0 and len(new_vws) == 0:
                # 鼻腔にチェック
                bikou[i]="認識可: {}  , 認識不可部分: {}".format(onin[0:len(onin)-len(new_onin)],new_onin)
                bunkais=["-1"]
                splitflag=False
                break
            if len(new_cnsts)==0:
                new_cnstsInd=[-1]
            if len(new_vws)==0:
                new_vwsInd=[-1]
            if (0 in new_cnstsInd) and (0 in new_vwsInd):
            # if min(new_cnstsInd)==0 and min(new_vwsInd)==0:
                if len(new_cnsts[new_cnstsInd.index(0)]) > len(new_vws[new_vwsInd.index(0)]):
                    bunkai=new_cnsts[new_cnstsInd.index(0)]
                else:
                    bunkai=new_vws[new_vwsInd.index(0)]
            elif 0 in new_cnstsInd:
            # elif min(new_cnstsInd)==0:
                if new_cnstsInd.count(0) > 1:
                    zeroInd=[cnst for cnst,cnstInd in zip(new_cnsts,new_cnstsInd) if cnstInd == 0]
                    symsize=[len(zero) for zero in zeroInd]
                    symind=symsize.index(max(symsize))
                    bunkai=zeroInd[symind]
                else:
                     bunkai=new_cnsts[new_cnstsInd.index(0)]
            elif 0 in new_vwsInd:
                if new_vwsInd.count(0) > 1:
                    zeroInd=[vw for vw,vwInd in zip(new_vws,new_vwsInd) if vwInd == 0]
                    symsize=[len(zero) for zero in zeroInd]
                    symind=symsize.index(max(symsize))
                    bunkai=zeroInd[symind]
                else:
                     bunkai=new_vws[new_vwsInd.index(0)]
            # print(bunkai)

            bunkais.append(new_onin[0:len(bunkai)])
            new_onin=new_onin[len(bunkai):]
            # print("区切り>{}   残り>{}   文字数>{}".format(bunkais,new_onin,len(new_onin)))
            if len(new_onin) == 0:
                splitflag=False
            counter+=1
        splitOnin.append(bunkais)

    maxlength=max([len(bunkais) for bunkais in splitOnin])
    for i in range(len(splitOnin)):
        currlen=len(splitOnin[i])
        for j in range(maxlength-currlen):
            splitOnin[i].append(".")

    symbols=["{}音".format(i+1) for i in range(maxlength)]
    # print(symbols)
    splitOninDf=pd.DataFrame(splitOnin,index=oninDf.index,columns=symbols)
    bikouDf=pd.DataFrame(bikou,index=oninDf.index,columns=["備考"])
    newOninDf=pd.concat([oninDf, splitOninDf, bikouDf], axis=1)
    newOninDf
    wfonin=basepath.format("狩俣調査票単語分割/{}.xlsx")
    with pd.ExcelWriter(wfonin.format(fn), engine='openpyxl') as writer:
        newOninDf.to_excel(writer,sheet_name="Sheet1")

