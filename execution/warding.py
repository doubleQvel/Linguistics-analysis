
# coding: utf-8

# In[2]:

import sys
import math
import pandas as pd
import openpyxl
import numpy as np
#from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hierarchy
import scipy.spatial.distance as dist


args=sys.argv
gramnumber=int(args[1])
gramname=str(args[1])

gramp=str(args[2])
if gramp == "all":
    gramp2="A"
else if gramp == "cvc":
    gramp2="C"
else if gramp == "vcv":
    gramp2="V"
else:
    eixt()

#カレントディレクトリ
currentpath=os.getcwd()
basepath="/".join(currentpath[0:-1])
basepath=basepath+"/data/{}"
# basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordDf  = pd.read_excel(rfword , sheet_name=0, header=0, index_col=0)

symbols=list(locateDf.iloc[:,0])
locates = list(locateDf.iloc[:,2])
hyouzi = list(locateDf.iloc[:,1])
words   = list(wordDf.iloc[:,0])

color_set=["#000000","#800000",
    "#ff0000","#800080",
    "#ff8c00","#ff00ff",
    "#008000","#808000",
    "#000080","#ff6633"]

rfcount=basepath.format("gram{}/counter/{}.xlsx".format(gramnumber,gramp))
countDf=pd.read_excel(rftri, sheet_name=0, header=0, index_col=0)

himethod='ward'
newdata=triDf.values
newdata=newdata.T
pdis=dist.pdist(newdata,'cosine')
z = hierarchy.linkage(pdis, method=himethod,metric="cosine")


#図の生成
figtitle='Dendrogram for pronunciation features in each region'
savefile=basepath.format("gram{}/pic/dend{}E.png".format(gramnumber,gramp2))

plt.figure(figsize=(60,25))
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['font.size'] = 50
plt.title(figtitle, fontsize=60)
plt.xlabel('Regions', fontsize=55)
plt.ylabel('Intercluster distance', fontsize=55)
hierarchy.set_link_color_palette(color_set) # ６クラスタまでの色を指定
hierarchy.dendrogram(z, leaf_font_size=35., # 横軸の文字の大きさを指定
                        color_threshold=0.3 * np.max(z[:, 2]), # ユークリッド平方距離が７以上を同色で表示
                        above_threshold_color='black',
                        labels=tuple(locates)) # ユークリッド平方距離が７以上を黒色に指定
plt.tight_layout()
plt.savefig(savefile)
plt.show()
plt.close()

threshold = 0.3 * np.max(z[:, 2])
c = hierarchy.fcluster(z, threshold, criterion='distance')
wf=basepath.format("gram{}/counter/{}E.csv".format(gramnumber,gramp2))
wdf=pd.DataFrame(hyouzi,index=hyouzi, columns=["市町村"])
wdf["グループ"]=c
wdf.to_csv(wf,header=False, index=False) #シート名[地点名]


# # 地域間の音のずれ

rftri=basepath.format("gram{}/pattern/{}/{}.xlsx")
distanceMatrix=[0 for i in locates]
for i,locate in enumerate(locates):
    triDf=pd.read_excel(rftri.format(gramnumber,gramp,locate), sheet_name=0, header=0, index_col=0)
    tmp=triDf.values
    distanceMatrix[i]=tmp.flatten()

pdis=dist.pdist(distanceMatrix,'cosine')
himethod='ward'
z = hierarchy.linkage(pdis, method=himethod,metric="cosine")#metric="cosine"


#図の生成
figtitle='Dendrogram for misalignment of sound between regions'
savefile=basepath.format("gram{}/pic/dend{}D.png".format(gramnumber,gramp2))

plt.figure(figsize=(60,25))
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['font.size'] = 50
plt.title(figtitle, fontsize=60)
plt.xlabel('Regions', fontsize=55)
plt.ylabel('Intercluster distance', fontsize=55)
hierarchy.set_link_color_palette(color_set) # ６クラスタまでの色を指定
hierarchy.dendrogram(z, leaf_font_size=35., # 横軸の文字の大きさを指定
                        color_threshold=0.3 * np.max(z[:, 2]), # ユークリッド平方距離が７以上を同色で表示
                        above_threshold_color='black',
                        labels=tuple(locates)) # ユークリッド平方距離が７以上を黒色に指定
plt.tight_layout()
plt.savefig(savefile)
plt.show()
plt.close()

threshold = 0.3 * np.max(z[:, 2])
c = hierarchy.fcluster(z, threshold, criterion='distance')
wf=basepath.format("gram{}/pattern/{}D.csv".format(gramnumber,gramp))
wdf=pd.DataFrame(hyouzi,index=hyouzi, columns=["市町村"])
wdf["グループ"]=c
wdf.to_csv(wf,header=False, index=False) #シート名[地点名]
