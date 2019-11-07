# t検定
import pandas as pd
import math
import numpy as np
from scipy import stats

import os
import sys


def t_kentei(A, B):
    """
    t_kentei(A, B) A,B:numpy_array型
    t検定の自作
    有意水準は0.05
    両側検定
    もらう引数はデータフレームのみで。
    データフレームにヘッダがあってもなくても動作は同じにしたい
    x_1 - x_2
    -----------------------
    s * sqrt(1/n_1 + 1/n_2)
    (n_1-1)s_1^2 + (n_2-1)s_2^2
    s = ----------------------------
    n_1 + n_2 -2
    """
    preP = 0.05  # 有意水準
    interval = stats.t.pdf(preP / 2, 1)
    # print("各平均A:{}   ,B:{}".format(np.mean(A), np.mean(B)))
    s1 = np.var(A)  # Aの不偏分散
    s2 = np.var(B)
    # print("不偏分散A:{}   ,   B:{}".format(s1, s2))
    n1 = A.size
    n2 = B.size
    # print("格配列のサイズ: {} , {}".format(n1, n2))
    s_n = (n1 - 1) * s1 + (n2 - 1) * s2
    s_d = n1 + n2 - 2
    s = s_n / s_d
    t_value = abs((np.mean(A) - np.mean(B)) / (s * math.sqrt(1 / n1 + 1 / n2)))
    # print("有意値:{}".format(interval))
    # print("t値:{}".format(t_value))
    flag = False
    if t_value >= interval:
        flag = True
    # print("t検定終了")
    print(flag)
    return flag


if __name__ == "__main__":
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
    rfpattern = basepath.format("gram{}/{}/{}.xlsx").format(gnumber, pattern, porder)

    locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
    wordDf = pd.read_excel(rfword, sheet_name=0, header=0, index_col=0)

    symbols = list(locateDf.iloc[:, 0])
    locates = list(locateDf.iloc[:, 2])
    hyouzi = list(locateDf.iloc[:, 1])
    words = list(wordDf.iloc[:, 0])

    ptDf = pd.read_excel(rfpattern, sheet_name=0, header=0, index_col=0)

    nonind = ptDf.index.str.contains("-9")
    ptDf = ptDf.loc[~nonind, :]
    ptDf2 = ptDf

    for i in range(0, 1):
        kaku_yuui = []
        for j in range(len(list(ptDf2.columns))):
            for k in range(j, len(list(ptDf2.columns))):
                A = np.array([ptDf2.iat[i, j], ptDf2.iat[i, j]])
                B = np.array([ptDf2.iat[i, k], ptDf2.iat[i, k]])
                yuui = t_kentei(A, B)
                kaku_yuui.append(yuui)
        print(list(ptDf2.index)[i])
        print(kaku_yuui.count(True))
    # print("結果:  {}".format(yuui))
