# t検定
import pandas as pd
import math
import numpy as np
from scipy import stats

import os
import sys


def chi2_test(data):
    """
    一標本の分散の区間推定
    カイ2乗分布を使用した区間推定
    変化パターンごとに推定箇所が一標本であるとして
    分散にばらつきがないか(不偏分散ー母分散＝0　または　母分散＝0)
    を調べる
        x_1 - x_2
    -----------------------
    s * sqrt(1/n_1 + 1/n_2)
    不偏分散s^2 = (1/(n-1)) * sum((x_i - mean(x))^2)
    """
    preP = 0.05  # 有意水準

    n = data.size
    # print("各平均A:{}   ,B:{}".format(np.mean(A), np.mean(B)))
    interval_r = stats.chi2.ppf(1 - (preP / 2), n)  # カイ2乗分布の上側2.5%
    interval_l = stats.chi2.ppf(preP / 2, n)  # カイ2乗分布の下側2.5%
    # print("不偏分散A:{}   ,   B:{}".format(s1, s2))
    # print("格配列のサイズ: {} , {}".format(n1, n2)
    kenteiryou = np.var(data) / 0.010
    # print("有意値:{}".format(interval))
    # print("t値:{}".format(t_value))
    flag = False
    if interval_l < kenteiryou and kenteiryou < interval_r:
        flag = True
    # print("t検定終了")
    # print(flag)
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
    rfpattern = basepath.format("gram{}/{}/{}_new.xlsx").format(
        gnumber, pattern, porder
    )

    locateDf = pd.read_excel(rflocate, sheet_name=0, header=0, index_col=0)
    wordDf = pd.read_excel(rfword, sheet_name=0, header=0, index_col=0)

    symbols = list(locateDf.iloc[:, 0])
    locates = list(locateDf.iloc[:, 2])
    hyouzi = list(locateDf.iloc[:, 1])
    words = list(wordDf.iloc[:, 0])

    ptDf = pd.read_excel(rfpattern, sheet_name=0, header=0, index_col=0)

    # nonind = ptDf.index.str.contains("-9")
    # ptDf = ptDf.loc[~nonind, :]
    # ptDf2 = ptDf
    # 暫定的にファイルを保存しておく
    # newName = basepath.format("gram{}/{}/{}_new.xlsx").format(gnumber, pattern, porder)
    # with pd.ExcelWriter(newName, engine="openpyxl") as writer:
    #     ptDf2.to_excel(writer, sheet_name="-9抜きの全体")
    flags = []
    for i in range(8500, 9000):
        flag = chi2_test(ptDf.iloc[i, :].values)
        flags.append(flag)
    patternlist = list(ptDf.index)
    patternlist = patternlist[8500:9000]
    print(flags.count(False))
    trueind = [i for i, flag in enumerate(flags) if flag is True]
    for i in trueind:
        print(patternlist[i])
    # for i in range(8657, 8658):
    # tyushutu = []
    # for i in range(len(list(ptDf2.index))):
    #     kaku_yuui = []
    #     for j in range(len(list(ptDf2.columns))):
    #         for k in range(j, len(list(ptDf2.columns))):
    #             A = np.array([ptDf2.iat[i, j], ptDf2.iat[i, j]])
    #             B = np.array([ptDf2.iat[i, k], ptDf2.iat[i, k]])
    #             yuui = t_kentei(A, B)
    #             kaku_yuui.append(yuui)
    #     print(list(ptDf2.index)[i])
    #     print(kaku_yuui.count(True))
    #     if kaku_yuui.count(True) != 0:
    #         tyushutu.append(list(ptDf2.index)[i])
    # print("結果:  {}".format(yuui))
