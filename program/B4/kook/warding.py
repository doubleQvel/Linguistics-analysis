
# coding: utf-8

# In[2]:


import pandas as pd
import openpyxl
import numpy as np
#from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hierarchy
import scipy.spatial.distance as dist


# In[3]:


basepath ="/Users/kazuki/Documents/Study/data/ryukyu/{}"
basepath2="/Users/kazuki/Downloads/{}"
rftri    = basepath2.format("gramTri/pattern/{}/{}.xlsx")
rfcos    = basepath2.format("gramTri/cosSim/{}/distanceMatrix.xlsx")
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")


# In[4]:


locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordDf  = pd.read_excel(rfword , sheet_name=0, header=0, index_col=0)


# In[5]:


symbols=list(locateDf.iloc[:,0])
locates = list(locateDf.iloc[:,2])
hyouzi = list(locateDf.iloc[:,1])
words   = list(wordDf.iloc[:,0])


# In[5]:


cosDf    = pd.read_excel(rfcos.format("cvc/"), sheet_name=10, header=0, index_col=0)
triDf=pd.read_excel(rftri.format("cvc/",locates[10]), sheet_name=0, header=0, index_col=0)


# In[6]:


similar=[0 for locate in locates]
for si,locate in enumerate(locates):
    tmd=cosDf.sort_values(locate, ascending=False)
    tmdind=list(tmd.index)
    tmddata=list(tmd.iloc[:,si])
    similar[si]=[tmddata,tmdind]


# In[58]:


print(similar[0][0])


# In[59]:


wf=basepath2.format("testsim.xlsx")
with pd.ExcelWriter(wf, engine='openpyxl') as writer:
    for si,locate in enumerate(locates):
        wdf=pd.DataFrame(similar[si],index=range(2), columns=range(len(locates)))
        wdf=wdf.T
        wdf.to_excel(writer,sheet_name=locate) #シート名[地点名]


# # 地点ごとの発音

# In[ ]:


rftri=basepath.format("gramTri/counter/all.xlsx")
triDf=pd.read_excel(rftri, sheet_name=0, header=0, index_col=0)


# In[ ]:


#図の生成
figtitle='Dendrogram for pronunciation features in each region'
himethod='ward'
savefile=basepath.format("gramTri/pic/dendAE.png")
newdata=triDf.values
newdata=newdata.T
pdis=dist.pdist(newdata,'cosine')
z = hierarchy.linkage(pdis, method=himethod,metric="cosine")

plt.figure(figsize=(60,25))
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['font.size'] = 50
plt.title(figtitle, fontsize=60)
plt.xlabel('Regions', fontsize=55)
plt.ylabel('Intercluster distance', fontsize=55)
# hierarchy.set_link_color_palette(['purple', 'lawngreen', 'green', 'blue', 'orange', 'red']) # ６クラスタまでの色を指定
hierarchy.dendrogram(z, leaf_font_size=35., # 横軸の文字の大きさを指定
                        color_threshold=0., # ユークリッド平方距離が７以上を同色で表示
                        above_threshold_color='black',
                        labels=tuple(locates)) # ユークリッド平方距離が７以上を黒色に指定
plt.tight_layout()
plt.savefig(savefile)
plt.show()
plt.close()

# z = hierarchy.linkage(newdata, method=himethod,metric="cosine")
# linkage_result = linkage(iris_df, method='ward', metric='euclidean')
# # クラスタ分けするしきい値を決める
# threshold = 0.7 * np.max(linkage_result[:, 2])
# # 階層型クラスタリングの可視化
# plt.figure(num=None, figsize=(16, 9), dpi=200, facecolor='w', edgecolor='k')
# dendrogram(linkage_result, labels=iris_labels, color_threshold=threshold)
# plt.show()
# # クラスタリング結果の値を取得
# clustered = fcluster(linkage_result, threshold, criterion='distance')


# In[9]:


threshold = 0.3 * np.max(z[:, 2])
c = hierarchy.fcluster(z, threshold, criterion='distance')
print(c)
wf=basepath.format("gramTri/counter/AE.csv")
wdf=pd.DataFrame(hyouzi,index=hyouzi, columns=["市町村"])
wdf["グループ"]=c
wdf.to_csv(wf,header=False, index=False) #シート名[地点名]


# # 地域間の音のずれ

# In[12]:


rftri=basepath.format("gramTri/pattern2/all/{}.xlsx")
distanceMatrix=[0 for i in locates]
for i,locate in enumerate(locates):
    triDf=pd.read_excel(rftri.format(locate), sheet_name=0, header=0, index_col=0)
    tmp=triDf.values
    distanceMatrix[i]=tmp.flatten()
    print(i)


# In[14]:


#図の生成
figtitle='Dendrogram for misalignment of sound between regions'
himethod='ward'
savefile=basepath.format("gramTri/pic/dendAD.png")
pdis=dist.pdist(distanceMatrix,'cosine')
z = hierarchy.linkage(pdis, method=himethod,metric="cosine")

plt.figure(figsize=(60,25))
plt.rcParams['font.family'] = 'IPAexGothic'
plt.rcParams['font.size'] = 50
plt.title(figtitle, fontsize=60)
plt.xlabel('Regions', fontsize=55)
plt.ylabel('Intercluster distance', fontsize=55)
# hierarchy.set_link_color_palette(['purple', 'lawngreen', 'green', 'blue', 'orange', 'red']) # ６クラスタまでの色を指定
hierarchy.dendrogram(z, leaf_font_size=35., # 横軸の文字の大きさを指定
                        color_threshold=0., # ユークリッド平方距離が７以上を同色で表示
                        above_threshold_color='black',
                        labels=tuple(locates)) # ユークリッド平方距離が７以上を黒色に指定
plt.tight_layout()
plt.savefig(savefile)
plt.show()
plt.close()


# In[15]:


threshold = 0.3 * np.max(z[:, 2])
c = hierarchy.fcluster(z, threshold, criterion='distance')
print(c)
wf=basepath.format("gramTri/pattern2/AD.csv")
wdf=pd.DataFrame(hyouzi,index=hyouzi, columns=["市町村"])
wdf["グループ"]=c
wdf.to_csv(wf,header=False, index=False) #シート名[地点名]


# In[ ]:


# 距離のまとめ
wfdistance=basepath.format("data/gramTri/pattern2/distanceA.xlsx")
with pd.ExcelWriter(wfdistance, engine='openpyxl') as writer:
    wdf=pd.DataFrame(distanceMatrix,index=locates, columns=range(len(distanceMatrix[0])))
    wdf.to_excel(writer,sheet_name="distance")#シート名[地点名]

