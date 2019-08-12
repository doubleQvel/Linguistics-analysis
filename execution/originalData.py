# coding: utf-8
import pandas as pd
import openpyxl
import numpy as np

basepath=basepath+"/data/ryukyu/{}"
rf= basepath.format("テスト用数値一覧・配点表RK_琉球全体72語20180314.xlsx")
wf= basepath.format("lpw.xlsx")
wfloc=basepath.format("locations.xlsx")

#ファイル内のシート数の確認およびシート名の確認
df_sheet_index=pd.read_excel(filename,sheet_name=None)
#必要データからシート抜き出し
sheetlists=[key for key in df_sheet_index.keys()
                if key not in
                ["音の型","母音入力数値一覧",
                 "母音配点","子音入力数値一覧",
                 "子音配点"]
            ]
Orgdf=pd.read_excel(rf,sheet_name=sheetlists,
                    usecols=[0,1]+[8]+list(range(10,26)),
                    skiprows=[0], header=0, index_col=0)
words=list(Orgdf.keys())
locs=list(Orgdf[words[0]].index)

for shn in sheetlists:
    df[shn].fillna(value={'地点名記号': 'XXX'}, inplace=True) #欠損の修正


