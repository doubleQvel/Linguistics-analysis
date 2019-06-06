import pandas as pd
import openpyxl
import numpy as np
#from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hierarchy

basepath="/home/kazukiq/Study/{}"
rftri    = basepath.format("data/gramTri/pattern/{}.xlsx")
rflocate = basepath.format("data/parameter/locations.xlsx")
rfwords  = basepath.format("data/parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordsDf  = pd.read_excel(rfwords , sheet_name=0, header=0, index_col=0)

locates = list(locateDf.iloc[0:,2])
words   = list(wordsDf.iloc[:,0])

wfcounter=basepath.format("data/gramTri/pattern/{}.xlsx")
tmpallcluster=[]
for i,locate in enumerate(locates):
    triDf=pd.read_excel(rftri.format(locate), sheet_name=0, header=0, index_col=0)
    print(locate,i)
    clusterdata=triDf.values
    clusterdata=clusterdata.T
    z=KMeans(n_clusters=5).fit_predict(clusterdata)
    z=np.insert(z,i,-1)
    #print(z)
    #print(z[0])
    tmpdata=z.to_list()
    #print(z)
    tmpallcluster.append(tmpdata)

tmpdata=np.array(tmpallcluster)

wf=basepath.format("data/gramTri/cluster/allK5.xlsx")
with pd.ExcelWriter(wf, engine='openpyxl') as writer:
    wdf=pd.DataFrame(tmpdata.T,index=locates, columns=locates)
    wdf.to_excel(writer,sheet_name="kmeans") #シート名[地点名]

