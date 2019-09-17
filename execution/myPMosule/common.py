#coding: utf-8

import math
import pandas as pd
import openpyxl
import numpy as np
import sys
import os

class commonInfo:
    def __init__(self):
        self.currentpath=os.getcwd()
        spliterPath=self.currentpath.split("/")
        packageIndex=spliterPath.index("Linguistics-analysis")+1
        self.packagePath="/".join(spliterPath[0:packageIndex])
        datapath="/data/ryukyu4/{}"
        self.basepath=self.packagePath+datapath

if __name__ == "__main__":
    test=commonInfo()
    print(test.packagePath)
    print(test.basepath)
