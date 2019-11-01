# coding: utf-8
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
rflocate = basepath.format("data/parameter/locations.xlsx")
rfwords  = basepath.format("data/parameter/sheetlist.xlsx")

locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
wordsDf  = pd.read_excel(rfwords , sheet_name=0, header=0, index_col=0)

locates = list(locateDf.iloc[:,2])
words   = list(wordsDf.iloc[:,0])

rfall=basepath.format("data/gramTri/pattern/all/{}.xlsx")
rfcvc=basepath.format("data/gramTri/pattern/cvc/{}.xlsx")
rfvcv=basepath.format("data/gramTri/pattern/vcv/{}.xlsx")

allDf = pd.read_excel(rfall, sheet_name=0, header=0, index_col=0)
cvcDf = pd.read_excel(rfcvc, sheet_name=0, header=0, index_col=0)
vcvDf = pd.read_excel(rfvcv, sheet_name=0, header=0, index_col=0)

allpattern=list(allDf.index)
cvcpattern=list(cvcDf.index)
vcvpattern=list(vcvDf.index)

distanceMatrix=[[] for locate in locates]
for i,locate in enumerate(locates):
    allDf=pd.read_excel(rfall.format(locate), sheet_name=0, header=0, index_col=0)
    featurevector=[[0 for l2 in locates] for l in locates]
    for si,li in enumerate(locates):
        a=allDf.iloc[:,si]
        for sj,lj in enumerate(locates):
            b=allDf.iloc[:,sj]
            featurevector[si][sj]cos_sim(a,b)
    # with pd.ExcelWriter(wfcounter.format(locate), engine='openpyxl') as writer:
    #     wdf=pd.DataFrame(featurevector,index=locates, columns=locates)
    #     wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]
    distanceMatrix[i]=featurevector
wfdistance=basepath.format("data/gramTri/cosSim/all/distanceMatrix.xlsx")
with pd.ExcelWriter(wfdistance, engine='openpyxl') as writer:
    for i,locate in enumerate(locates):
        wdf=pd.DataFrame(distanceMatrix[i],index=locates, columns=locates)
        wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]

distanceMatrix=[[] for locate in locates]
for i,locate in enumerate(locates):
    cvcDf=pd.read_excel(rfcvc.format(locate), sheet_name=0, header=0, index_col=0)
    featurevector=[[0 for l2 in locates] for l in locates]
    for si,li in enumerate(locates):
        a=cvcDf.iloc[:,si]
        for sj,lj in enumerate(locates):
            b=cvcDf.iloc[:,sj]
            featurevector[si][sj]cos_sim(a,b)
    distanceMatrix[i]=featurevector
wfdistance=basepath.format("data/gramTri/cosSim/cvc/distanceMatrix.xlsx")
with pd.ExcelWriter(wfdistance, engine='openpyxl') as writer:
    for i,locate in enumerate(locates):
        wdf=pd.DataFrame(distanceMatrix[i],index=locates, columns=locates)
        wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]

distanceMatrix=[[] for locate in locates]
for i,locate in enumerate(locates):
    vcvDf=pd.read_excel(rfvcv.format(locate), sheet_name=0, header=0, index_col=0)
    featurevector=[[0 for l2 in locates] for l in locates]
    for si,li in enumerate(locates):
        a=vcvDf.iloc[:,si]
        for sj,lj in enumerate(locates):
            b=vcvDf.iloc[:,sj]
            featurevector[si][sj]cos_sim(a,b)
    distanceMatrix[i]=featurevector
wfdistance=basepath.format("data/gramTri/cosSim/vcv/distanceMatrix.xlsx")
with pd.ExcelWriter(wfdistance, engine='openpyxl') as writer:
    for i,locate in enumerate(locates):
        wdf=pd.DataFrame(distanceMatrix[i],index=locates, columns=locates)
        wdf.to_excel(writer,sheet_name=locate)#シート名[地点名]
