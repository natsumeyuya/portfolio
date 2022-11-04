#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas_datareader')


# In[2]:


from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


start = '2019-06-01'
end = '2022-11-01'

df = data.DataReader('^N225','yahoo',start,end)


# In[4]:


df.head(10)


# In[5]:


df.index


# In[6]:


date = df.index
price = df['Adj Close']


# In[7]:


plt.plot(date,price)#(x軸、y軸)


# In[8]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.plot(date,price)#(x軸、y軸)


# In[9]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.plot(date,price,label = 'Nikkei225')#(x軸、y軸)
plt.legend()#ラベルを表示させる(線の名前)


# In[10]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.plot(date,price,label = 'Nikkei225')#(x軸、y軸)
plt.title('N225',color = 'blue',backgroundcolor = 'white',size = 40,loc = 'center')
#title('タイトル'、'フォントカラー'、'タイトルの背景'、'タイトルのサイズ'、'タイトルの位置')
plt.legend()#ラベルを表示させる(線の名前)


# In[11]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.plot(date,price,label = 'Nikkei225')#(x軸、y軸)
#title('タイトル'、'フォントカラー'、'タイトルの背景'、'タイトルのサイズ'、'タイトルの位置')
plt.title('N225',color = 'blue',backgroundcolor = 'white',size = 40,loc = 'center')
plt.xlabel('date',color = 'black',size = 30)
plt.ylabel('price',color = 'black',size = 30)
plt.legend()#ラベルを表示させる(線の名前)


# In[12]:


span01 = 5
span02 = 25
span03 = 50

df['sma01']=price.rolling(window=span01).mean()
df['sma02']=price.rolling(window=span02).mean()
df['sma03']=price.rolling(window=span03).mean()


# In[13]:


pd.set_option('display.max_rows',None)
df.head(100)


# In[14]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.plot(date,price,label = 'Nikkei225')#(x軸、y軸)
plt.plot(date,df['sma01'],label="sma01")
plt.plot(date,df['sma02'],label="sma02")
plt.plot(date,df['sma03'],label="sma03")
#title('タイトル'、'フォントカラー'、'タイトルの背景'、'タイトルのサイズ'、'タイトルの位置')
plt.title('N225',color = 'blue',backgroundcolor = 'white',size = 40,loc = 'center')
plt.xlabel('data',color = 'black',size = 30)
plt.ylabel('price',color = 'black',size = 30)
plt.legend()#ラベルを表示させる(線の名前)


# In[15]:


plt.figure(figsize=(30,15))
plt.bar(date,df['Volume'],label='volume',color='grey')

plt.legend()


# In[16]:


plt.figure(figsize = (30,10))#figsize = (横のサイズ、縦のサイズ)
plt.subplot(2,1,1)#(縦方向を分割する数、横方向に分割する数、グラフを配置する位置)

plt.plot(date,price,label = 'Nikkei225')#(x軸、y軸)
plt.plot(date,df['sma01'],label="sma01")
plt.plot(date,df['sma02'],label="sma02")
plt.plot(date,df['sma03'],label="sma03")
plt.legend()#ラベルを表示させる(線の名前)

plt.subplot(2,1,2)
plt.bar(date,df['Volume'],label='Volume',color='grey')
plt.legend()


# In[17]:


df = data.DataReader('6098.jp','stooq')


# In[18]:


df.head()


# In[19]:


df.index.min()


# In[20]:


df.index.max()


# In[21]:


df = df.sort_index()#インデックスの並び替え


# In[22]:


df.head()


# In[23]:


df.tail()


# In[24]:


df.index>='2019-06-01 00:00:00'


# In[25]:


df[df.index>='2019-06-01 00:00:00']


# In[26]:


df[df.index<='2022-11-01 00:00:00']


# In[28]:


df[(df.index>='2019-06-01 00:00:00')&(df.index<='2020-11-01 00:00:00')]


# In[30]:


#リクルートホールディングス
df = data.DataReader('6098.JP','stooq')

date = df.index
price=df['Close']

span01 = 5
span02 = 25
span03 = 50

df['sma01']=price.rolling(window=span01).mean()
df['sma02']=price.rolling(window=span01).mean()
df['sma03']=price.rolling(window=span01).mean()

plt.figure(figsize = (30,15))
plt.subplot(2,1,1)

plt.plot(date,price,label='Close',color='#99b898')
plt.plot(date,df['sma01'],label='sma01',color='#e84a5f')
plt.plot(date,df['sma02'],label='sma02',color='#ff847c')
plt.plot(date,df['sma03'],label='sma03',color='#feceab')
plt.legend()

plt.subplot(2,1,2)
plt.bar(date,df['Volume'],label='Volume',color='grey')
plt.legend()


# In[38]:


start ='2019-06-01'
end = '2022-10-01'
company_code = '6502.JP'


# In[53]:


def company_stock(start,end,company_code,company_name):
    df = data.DataReader(company_code,'stooq')
    df = df[(df.index>=start)&(df.index<=end)]
    date =df.index
    price=df['Close']

    span01 = 5
    span02 = 25
    span03 = 50

    df['sma01']=price.rolling(window=span01).mean()
    df['sma02']=price.rolling(window=span01).mean()
    df['sma03']=price.rolling(window=span01).mean()

    plt.figure(figsize = (20,10))
    plt.subplot(2,1,1)

    plt.plot(date,price,label='Close',color='#99b898')
    plt.plot(date,df['sma01'],label='sma01',color='#e84a5f')
    plt.plot(date,df['sma02'],label='sma02',color='#ff847c')
    plt.plot(date,df['sma03'],label='sma03',color='#feceab')
    plt.title(company_name,color = 'blue',backgroundcolor = 'white',size = 40,loc = 'center')

    plt.legend()

    plt.subplot(2,1,2)
    plt.bar(date,df['Volume'],label='Volume',color='grey')
    plt.legend()


# In[49]:


company_stock('2019-06-01','2022-11-01','6502.JP')


# In[55]:


company_stock('2019-06-01','2022-11-01','7203.JP','toyota')


# In[ ]:




