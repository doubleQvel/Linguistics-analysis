
# coding: utf-8

# # やること
#
# 音の変換
# 1. 子音または母音の認識
# 2. 分解
# 3. 変換

# In[1]:


import pandas as pd
import openpyxl
import numpy as np
import copy
import sys
import os
basepath="/Users/kazuki/Documents/Study/test/data/ryukyu4/{}"

rfcnsts=basepath.format("parameter/consonants-list.csv")
rfvws  =basepath.format("parameter/vowels-list.csv")
rforg  =basepath.format("狩俣調査票/{}.xlsx")

cnstsDf=pd.read_csv(rfcnsts,sep="\t",index_col=0)
vwsDf  =pd.read_csv(rfvws  ,sep="\t",index_col=0)
fileNames=["222_?? 票_第２伊江???? (1)","228_???_?????? ま市屋慶名 (1)",
            "260_???_?????? 味村阿嘉島 (1)","269_?? 票_第２宮古?? ?(1)",
            "273_?? 票_第２宮古伊良部島国仲 (1)","276_?? 票_第２石垣??? (1)",
            "277_?? 票_第２石垣???? (1)"]
for fn in fileNames:
    orgDf=pd.read_excel(rforg.format(fn),header=0,dtype=str)
    oninDf=orgDf.loc[ :, ["音韻表記１","表記２"]]

    # 音の認識をどう行う？


    splitOnin=[]
    for i in oninDf.index:
        bunkais=[]
        onin=oninDf.iat[i,0]
        print("{}の{}番目の音韻  >  {}".format(fn,i,onin))

        if onin=="NR" or onin=="3" or onin=="4" or onin=="5" or onin=="Y" or ("/" in onin) or (" " in onin) or ("　" in onin) or ("ɯ̈" in onin) or ("vː" in onin) or ("æː" in onin) or ("ɛ" in onin)or ("nː" in onin) or ("y" in onin) or ("ɭ" in onin) or ("uˑ" in onin) or ("ˀ" in onin) or ("ã" in onin):
            splitOnin.append(["-1"])
            continue
        new_onin=onin

        splitflag=True
        counter=1
        while splitflag:
            print("{}回目".format(counter))
            new_cnsts=[]
            new_vws =[]
            for ci,cnst in enumerate(cnstsDf.iloc[:,0].values):
                if cnst in new_onin:
                    new_cnsts.append(cnst)
    #                 print("{} 子音{}".format(ci,cnst))
            for vi,vw in enumerate(vwsDf.iloc[:,0].values):
                if vw in new_onin:
                    new_vws.append(vw)
    #                 print("{} 母音{}".format(vi,vw))

            print("子音   {}".format(new_cnsts))
            print("母音   {}".format(new_vws))

            new_cnstsInd=[new_onin.index(cnst) for cnst in new_cnsts]
            new_vwsInd =[new_onin.index(vw) for vw  in new_vws]
            print(new_cnstsInd)
            print(new_vwsInd)
            if len(new_cnsts)==0:
                new_cnstsInd=[-1]
            if len(new_vws)==0:
                new_vwsInd=[-1]
            if min(new_cnstsInd)==0 and min(new_vwsInd)==0:
                if len(new_cnsts[new_cnstsInd.index(0)]) > len(new_vws[new_vwsInd.index(0)]):
                    bunkai=new_cnsts[new_cnstsInd.index(0)]
                else:
                    bunkai=new_vws[new_vwsInd.index(0)]
            elif min(new_cnstsInd)==0:
                if new_cnstsInd.count(0) > 1:
                    zeroInd=[cnst for cnst,cnstInd in zip(new_cnsts,new_cnstsInd) if cnstInd == 0]
    #                 print("子音の変換{}".format(zeroInd))
                    symsize=[len(zero) for zero in zeroInd]
                    symind=symsize.index(max(symsize))
                    bunkai=zeroInd[symind]
    #                 if ("k̓" in new_cnsts) and bunkai=="k":
    #                     bunkai="k̓"
                else:
                     bunkai=new_cnsts[new_cnstsInd.index(0)]
            else:
                if new_vwsInd.count(0) > 1:
                    zeroInd=[vw for vw,vwInd in zip(new_vws,new_vwsInd) if vwInd == 0]
                    symsize=[len(zero) for zero in zeroInd]
                    symind=symsize.index(max(symsize))
                    bunkai=zeroInd[symind]
                else:
                     bunkai=new_vws[new_vwsInd.index(0)]
            print(bunkai)

            bunkais.append(new_onin[0:len(bunkai)])
            new_onin=new_onin[len(bunkai):]
            print("区切り>{}   残り>{}   文字数>{}".format(bunkais,new_onin,len(new_onin)))
            if len(new_onin) == 0:
                splitflag=False
            counter+=1
        splitOnin.append(bunkais)


    maxlength=max([len(bunkais) for bunkais in splitOnin])
    for i in range(len(splitOnin)):
        currlen=len(splitOnin[i])
        for j in range(maxlength-currlen):
            splitOnin[i].append(".")

    # for i in range(len(splitOnin)):
    #     print(splitOnin[i])
    symbols=["{}音".format(i+1) for i in range(maxlength)]
    # print(symbols)
    splitOninDf=pd.DataFrame(splitOnin,index=list(range(len(oninDf))),columns=symbols)
    newOninDf=pd.concat([oninDf["音韻表記１"], splitOninDf], axis=1)
    newOninDf
    wfonin=basepath.format("単語分解/{}.xlsx")
    with pd.ExcelWriter(wfonin.format(fn), engine='openpyxl') as writer:
        newOninDf.to_excel(writer,sheet_name="Sheet1")
wfIPA=basepath.format("IPA対応表.xlsx")
with pd.ExcelWriter(wfIPA, engine='openpyxl') as writer:
    cnstsDf.to_excel(writer,sheet_name="子音(consonants)")
    vwsDf.to_excel(writer,sheet_name="母音(vowels)")

