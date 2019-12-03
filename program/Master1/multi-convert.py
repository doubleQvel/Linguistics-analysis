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
pattern = "pattern"
porder = "all"
porder2 = "A"
rflocate = basepath.format("parameter/locations.xlsx")
rfword = basepath.format("parameter/sheetlist.xlsx")
rfpattern = basepath.format("gram{}/{}/{}_new.xlsx").format(gnumber, pattern, porder)

ptDf = pd.read_excel(rfpattern, sheet_name=0, header=0, index_col=0)

bases = []
nexts = []
for ind in list(ptDf.index):
    basepattern, nextpattern = ind.split("->")
    bases.append(basepattern)
    nexts.append(nextpattern)

tuples = list(zip(bases, nexts))
# MultiIndexの列の作成
index = pd.MultiIndex.from_tuples(tuples, names=["base", "next"])
newdf = pd.DataFrame(ptDf.values, index=index, columns=ptDf.columns)

wf = basepath.format("gram3/newPattern/all.xlsx")
with pd.ExcelWriter(wf, engine="openpyxl") as writer:
    newdf.to_excel(writer, sheet_name="gram{}".format(gnumber))  # シート名[地点名]
