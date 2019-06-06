import pandas as pd
import openpyxl
import numpy as np
#from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.spatial.distance as dis
from sklearn.cluster import KMeans
import scipy.cluster.hierarchy as hierarchy

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

basepath="/home/kazukiq/Study/{}"
rftri    = basepath.format("data/gramTri/pattern/{}.xlsx")
rflocate = basepath.format("data/parameter/locations.xlsx")
rfwords  = basepath.format("data/parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordsDf  = pd.read_excel(rfwords , sheet_name=0, header=0, index_col=0)

locates = list(locateDf.iloc[:,2])
words   = list(wordsDf.iloc[:,0])

wfcounter=basepath.format("data/gramTri/cosSim/{}.xlsx")

distanceMatrix=[[] for locate in locates]
for i,locate in enumerate(locates):
    #allhindovector=[[] for locate in locates]
    triDf=pd.read_excel(rftri.format(locate), sheet_name=0, header=0, index_col=0)
    print(locate)
    tmplocates=list(triDf.keys())
    allhindovector=[[] for l in tmplocates]
    for si,li in enumerate(tmplocates):
        a=triDf.iloc[:,si]
        for sj,lj in enumerate(tmplocates):
            b=triDf.iloc[:,sj]
            allhindovector[si].append(cos_sim(a,b))
    with pd.ExcelWriter(wfcounter.format(locate), engine='openpyxl') as writer:
        wdf=pd.DataFrame(allhindovector,index=tmplocates, columns=tmplocates)
        wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]
    distanceMatrix[i]=allhindovector

wfdistance=basepath.format("data/gramTri/cosSim/distanceMatrix.xlsx")
with pd.ExcelWriter(wfdistance, engine='openpyxl') as writer:
    for i,locate in enumerate(locates):
        tmplocates=[locate for locate in locates if locate != locates[i]]
        wdf=pd.DataFrame(distanceMatrix[i],index=tmplocates, columns=tmplocates)
        wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]
