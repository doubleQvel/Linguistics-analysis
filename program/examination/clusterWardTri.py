# coding: utf-8
import pandas as pd
import openpyxl
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hierarchy

basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rftri    = basepath.format("gramTri/cosSim/{}.xlsx")
rflocate = basepath.format("parameter/locations.xlsx")
rfwords  = basepath.format("parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordsDf  = pd.read_excel(rfwords , sheet_name=0, header=0, index_col=0)

hyouzi=list(locateDf.iloc[:,0])
locates = list(locateDf.iloc[:,2])
words   = list(wordsDf.iloc[:,0])

savefile=basepath.format("picture/png/cluster/{}.png")

for li,locate in enumerate(locates):
#図の生成
    triDf=pd.read_excel(rftri.format(locate), sheet_name=0, header=0, index_col=0)
    #figtitle='ウォード法の樹形図'
    figtitle="Dendrogram with Ward"
    xname="Locates"
    yname="Cluster Distance"
    labelname=tuple(hyouzi)
    himethod='ward'

    clusterdata=triDf.values
    clusterdata=clusterdata.T
    z = hierarchy.linkage(clusterdata, method=himethod)
    plt.figure(figsize=(60,30))
    #plt.rcParams['font.family'] = 'IPAexGothic'
    plt.rcParams['font.size'] = 50
    plt.title(figtitle, fontsize=60)
    plt.xlabel(xname, fontsize=55)
    plt.ylabel(yname, fontsize=55)
    # hierarchy.set_link_color_palette(['purple', 'lawngreen', 'green', 'blue', 'orange', 'red']) # ６クラスタまでの色を指定
    hierarchy.dendrogram(z, leaf_font_size=35., # 横軸の文字の大きさを指定
                        color_threshold=0., # ユークリッド平方距離が７以上を同色で表示
                        above_threshold_color='black',
                        labels=labelname) # ユークリッド平方距離が７以上を黒色に指定
    plt.tight_layout()
    plt.savefig(savefile.format(locate))
    #plt.show()
    plt.close()
