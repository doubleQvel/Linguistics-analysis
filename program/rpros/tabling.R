library(Hmisc)
library(gdata)
library(xtable)
filename<-"/Users/kazuki/Documents/Study/data/ryukyu/kclus.xlsx"
df <- read.xls(filename,sheet=1)
print(xtable(df))

