
# coding: utf-8

# ## やること
# ### ファイルを開く pandas
# ### データフレーム の生成 pandasにより、新規にデータの作成
# ### 作成したデータフレーム からデータ読み込み
# ### バイグラム、トライグラムに分解
# ### 各地点ごとにグラフ化
# #### 基本形との違いを眺めるには？　別データにする必要あり

# In[1]:


filename="/Users/kazuki/Documents/Study/data/6-20/テスト用数値一覧・配点表RK_琉球全体72語20180314.xlsm"
wfName="/Users/kazuki/Documents/Study/data/ryukyu/testword.xlsx"


# In[2]:


import pandas as pd
import openpyxl
import numpy as np


# In[3]:


#ファイル内のシート数の確認およびシート名の確認
df_sheet_index=pd.read_excel(filename,sheet_name=None)


# In[4]:


#必要データからシート抜き出し
sheetlists=[key for key in df_sheet_index.keys() if key not in ["音の型","母音入力数値一覧","母音配点","子音入力数値一覧","子音配点"]]


# ## 語形の分割

# In[115]:


#必要なデータ抽出 
df=pd.read_excel(filename,sheet_name=sheetlists,usecols=[0,1]+[8]+list(range(10,26)),skiprows=[0],header=0, index_col=0)
# print(df[sheetlists[0]])


# In[116]:


#データフレーム の作成
for shn in sheetlists:
    df[shn].fillna(value={'地点名記号': 'XXX'}, inplace=True) #欠損の修正
    #print(dfs.isnull().sum()) 欠損の確認
#print(df[sheetlists[0]]["地点名記号"])


# In[117]:


# print(df[sheetlists[0]].columns.values)


# In[118]:


#データフレームの作成:各フレームのリスト作成(共通のもの)
wshls=df[sheetlists[0]].地点名記号 #シートのリスト
winls=sheetlists #インデックスのリスト
cols=df[sheetlists[0]].columns.values#カラムのリスト
cols=cols[1:]


# In[120]:


# print(len(sols))
# print(len(winls))
# print(len(cols))
# print(type(wshls))


# In[121]:


datalists=[]
for i,wsh in enumerate(wshls):
    #データリストの連結
    datalist=[df[shn].iloc[i] for shn in sheetlists]
    datalists.append(datalist)


# In[123]:


with pd.ExcelWriter(wfName) as writer:
    for (datalist,wsheet) in zip(datalists,wshls):
        wdf=pd.DataFrame(datalist,index=winls, columns=cols)
        wdf.to_excel(writer,sheet_name=wsheet)


# # 音素ファイルの分割
# 1. 調音方式でのk-meansを行う
# 2. 調音のみを抜き出したものを使用
# 3. とりあえず各音素をベクトルとして使用(-1や9の場合は0にする)
# 4. 首の表記だけやればあとは繰り返しでなんとかなるだろ

# In[1]:


filename="/Users/kazuki/Documents/Study/data/6-20/テスト用数値一覧・配点表RK_琉球全体72語20180314.xlsm"
import pandas as pd
import openpyxl
import numpy as np


# In[2]:


#ファイル内のシート数の確認およびシート名の確認
df_sheet_index=pd.read_excel(filename,sheet_name=None)


# In[3]:


#必要データからシート抜き出し
sheetlists=[key for key in df_sheet_index.keys() if key not in ["音の型","母音入力数値一覧","母音配点","子音入力数値一覧","子音配点"]]


# In[5]:


#必要なデータ抽出 (10,26):子音、母音
df=pd.read_excel(filename,sheet_name=sheetlists,usecols=[0,1]+[8]+list(range(27,82)),skiprows=[0],header=0, index_col=0)
print(df[sheetlists[0]])


# In[6]:


for shn in sheetlists:
    df[shn].fillna(value={'地点名記号': 'XXX'}, inplace=True) #欠損の修正


# In[7]:


wshls=df[sheetlists[0]].地点名記号 #シートのリスト
winls=sheetlists #インデックスのリスト
cols=df[sheetlists[0]].columns.values#カラムのリスト
cols=cols[1:]


# In[8]:


datalists=[]
for i,wsh in enumerate(wshls):
    #データリストの連結
    datalist=[df[shn].iloc[i] for shn in sheetlists]
    datalists.append(datalist)


# In[9]:


wfName="/Users/kazuki/Documents/Study/data/ryukyu/tyou.xlsx"
with pd.ExcelWriter(wfName) as writer:
    for (datalist,wsheet) in zip(datalists,wshls):
        wdf=pd.DataFrame(datalist,index=winls, columns=cols)
        wdf.to_excel(writer,sheet_name=wsheet)


# ## ルールの分割

# In[3]:


#ルールシートの分割
rsheet=["音の型","母音入力数値一覧","母音配点","子音入力数値一覧","子音配点"]


# In[7]:


#音の型
df1=pd.read_excel(filename,sheet_name=rsheet[0],skiprows=[0],header=0, index_col=0)
# print(df1)


# In[10]:


#母音入力数値一覧
df2=pd.read_excel(filename,sheet_name=rsheet[1],usecols=list(range(1,6)),skiprows=[0],header=0, index_col=0)
# print(df2)
df2=df2.iloc[0:37,]
# print(df2)
#print(df2.iloc[0:37,])


# In[16]:


#母音配点
df3=pd.read_excel(filename,sheet_name=rsheet[2],header=0)
df3=df3.iloc[0:7,]
# print(df3)


# In[18]:


#子音入力数値一覧
df4=pd.read_excel(filename,sheet_name=rsheet[3],usecols=list(range(1,6)),skiprows=[0],header=0, index_col=0)
# print(df4)
df4=df4.iloc[0:81,]
print(df4)


# In[19]:


#子音配点
df5=pd.read_excel(filename,sheet_name=rsheet[4],header=0)
# df5=df3.iloc[0:7,]
print(df5)


# In[23]:


wfName="/Users/kazuki/Documents/Study/data/ryukyu/rule2.xlsx"
with pd.ExcelWriter(wfName) as writer:
    #音の型
    df1.to_excel(writer,sheet_name=rsheet[0])
    #母音入力数値一覧
    df2.to_excel(writer,sheet_name=rsheet[1])
    #母音配点
    df3.to_excel(writer,sheet_name=rsheet[2])
    #子音入力数値一覧
    df4.to_excel(writer,sheet_name=rsheet[3])
    #子音配点
    df5.to_excel(writer,sheet_name=rsheet[4])
#     wdf=pd.DataFrame(datalist,index=winls, columns=cols)
#     wdf.to_excel(writer,sheet_name=wsheet)


# # 地点名のみにファイル分割

# In[5]:


import pandas as pd
import openpyxl
import numpy as np


# In[6]:


filename="/Users/kazuki/Documents/Study/data/6-20/テスト用数値一覧・配点表RK_琉球全体72語20180314.xlsm"
wfilename="/Users/kazuki/Documents/Study/data/ryukyu/locations.xlsx"


# In[14]:


df=pd.read_excel(filename,sheet_name=5,skiprows=[0],usecols=list(range(4)),header=0,index_col=0)
print(df)


# In[17]:


df.fillna(value={'地点名記号': 'XXX'}, inplace=True) #欠損の修正
print(df.isnull().sum()) #欠損の確認
print(df["地点名記号"])


# In[18]:


#ファイル書き込み
with pd.ExcelWriter(wfilename) as writer:
        df.to_excel(writer,sheet_name="語形")

