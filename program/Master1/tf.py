# tf.py
# 各パターンの構成割合と変化割合を見る。
# マルチインデックスにより変化前と変化後の計算が容易となった
import pandas as pd
import openpyxl
import numpy as np

import os

currentpath = os.getcwd()
basepath = currentpath.split("/")
basepath = (
    "/".join(basepath[: basepath.index("Linguistics-analysis") + 1])
    + "/data/ryukyu4/{}"
)
gnumber = 3
dORe = "D"
pattern = "newPattern"
porder = "all"
porder2 = "A"
rflocate = basepath.format("parameter/locations.xlsx")
rfword = basepath.format("parameter/sheetlist.xlsx")
rfpattern = basepath.format("gram{}/{}/{}.xlsx").format(gnumber, pattern, porder)

ptDf = pd.read_excel(rfpattern, sheet_name=0, header=0, index_col=[0, 1])

# index名：base, next

baseInd = list(ptDf.index.levels[0])
# print(baseInd)
# nextInd = ptDf.index.levels[1]
# print(nextInd)

# 全体の頻度を計算
allS = np.sum(ptDf.values.flatten())
basesS = []
for ind in baseInd:
    baseDf = ptDf.loc[(ind,)]
    baseS = np.sum(baseDf.values.flatten())
    basesS.append(baseS / allS)
    # tf: 各変化前の全頻度 / 全体の頻度数

# newdf = pd.DataFrame(basesS, index=baseInd, columns=["base-tf"])
# wf = basepath.format("gram{}/{}/{}-tf.xlsx").format(gnumber, pattern, porder)
# with pd.ExcelWriter(wf, engine="openpyxl") as writer:
#     newdf.to_excel(writer, sheet_name="gram{}".format(gnumber))  # シート名[地点名]

# 変化後の割合を計算
nextsS = []
for ind in baseInd:
    baseDf = ptDf.loc[(ind,)]
    baseS = np.sum(baseDf.values.flatten())
    nextS = baseDf.sum(axis=1)
    print(nextS)
    for s in nextS:
        nextsS.append(s / baseS)
newdf = pd.DataFrame(nextsS, index=ptDf.index, columns=["next-tf"])
wf = basepath.format("gram{}/{}/{}-next-tf.xlsx").format(gnumber, pattern, porder)
with pd.ExcelWriter(wf, engine="openpyxl") as writer:
    newdf.to_excel(writer, sheet_name="gram{}".format(gnumber))  # シート名[地点名]
