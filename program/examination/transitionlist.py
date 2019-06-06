# coding: utf-8
import math
import pandas as pd
import openpyxl
import numpy as np
import sys

args=sys.argv
gramnumber=int(args[1])
gramname=""
if gramnumber == 1:
    gramname = "Uni"
elif gramnumber == 2:
    gramname = "Bi"
elif gramnumber == 3:
    gramname = "Tri"

basepath="/Users/kazuki/Documents/Study/data/ryukyu/{}"
rflocate = basepath.format("parameter/locations.xlsx")
rfword   = basepath.format("parameter/sheetlist.xlsx")
rfpattern= basepath.format("gram{}/pattern/{}/patternlist.xlsx")

phonemes=["all","cvc","vcv"]
phpattern=[[],[],[]]

for i in range(3):
    phpattern[i]=pd.read_excel(rfpattern.format(gramname,phonemes[i]),sheet_name=0,header=0, index_col=0,dtype=str)

for i in range(3):
    motos,hikaus=[patterns.split("->") for patterns in list(phpattern[i].index)]
    phpattern[i]["before"]=motos
    phpattern[i]["after"]=hikakus
    for patterns in list(phpattern[i].index):
        


