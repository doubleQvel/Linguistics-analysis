#coding: utf-8
#単語分割

import math
import pandas as pd
import openpyxl
import numpy as np

class WordSpreader:
    def __init__(self,file):
        self.df=pd.read_excel(file,sheet_name=None)
        self.shNs=list(self.df.keys())
        self.raws=list(self.df[self.shNs[0]].index)
        self.tokenlist=[]
        self.tokenum=0
    def tokener(self,shnum,ng):
        sheet=self.df[self.shNs[shnum]]
        # raws=list(sheet.index)
        self.tokenlist=[]
        for i,locate in enumerate(self.raws):
            text=list(map(str,sheet.iloc[i,2:]))
            data=self.ngramize(text,ng) #発音記号をN-グラムに分解
            self.tokenlist.append(data)
    def ngramize(self,text, n):
        text_list = list(text)
        if n > 1:
            text_list = ["<s>"]+list(text)
        if "." not in text_list:
            text_list.append(".")
        saku=text_list.index(".")
        if n > 1:
            text_list[saku]="<e>"
        else:
            saku=saku-1
        return [text_list[i:i + n] for i, char in enumerate(text_list) if saku+1 >= i+n]
