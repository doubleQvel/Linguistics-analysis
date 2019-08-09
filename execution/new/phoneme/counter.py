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
rfgram   = basepath.format("gram{}/phoneme/{}.xlsx")
wfpattern= basepath.format("gram{}/phcounter/{}.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
pageDf   = pd.read_excel(rfword,sheet_name=0,header=0, index_col=0)

locates  = locateDf.iloc[:,2].tolist()
titens   = locateDf.iloc[:,0].tolist()
pages    = pageDf.iloc[:,0].tolist()

connum=[14+1,7+1,5+1,2+1,1+1]
vownum=[7+1,5+1,4+1,2+1,2+1]

grams=[0 for i in pages]
for pi,page in enumerate(pages):
    grams[pi]=pd.read_excel(rfgram.format(gramname,page),
                            sheet_name=0,header=0,
                            index_col=0,dtype=str)
    if "XXX" in list(grams[pi].columns):
        grams[pi]=grams[pi].drop(columns="XXX")
print("ファイル読み込み完了")

# 1地点ごとにベクトルを作成する
counter=np.zeros((len(locates),sum(connum)+sum(vownum)))

for si,(soutei,locate) in enumerate(zip(titens,locates)):
    for pi,page in enumerate(pages):
        sgrams=list(grams[pi][soutei].values)
        print(soutei,page,sgrams)
        for cv in range(len(sgrams)):
            cvs=sgrams[cv].split(" ")
            if cv%2==0:
                for onsonum,onso in enumerate(cvs):
                    if int(float(onso)) == -1 or int(float(onso))==-9:
                        continue
                    else:
                        indo=sum(connum[0:onsonum])+1+int(float(onso))
                        # print(indo)
                        if onsonum==0:
                            indo-=1
                        counter[si][indo]+=1
            else:
                for onsonum,onso in enumerate(cvs):
                    if int(float(onso)) == -1 or int(float(onso))==-9:
                        continue
                    else:
                        indo=sum(connum)+sum(vownum[0:onsonum])+1+int(float(onso))
                        counter[si][indo]+=1
#変化語の特徴ベクトルの書き込み
with pd.ExcelWriter(wfpattern.format(gramname,"counter"), engine='openpyxl') as writer:
    wdf=pd.DataFrame(counter,index=locates, columns=list(range(sum(connum)+sum(vownum))))
    wdf=wdf.T
    wdf.to_excel(writer,sheet_name="vector")