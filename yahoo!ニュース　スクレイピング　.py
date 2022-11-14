#!/usr/bin/env python
# coding: utf-8

# In[4]:


# 流れ
# ヤフーニュースのURLをseleniumとbeautifulsoupを使って取得
# 主要・経済・ITのトピックスのそれぞれのURLを取得
# その中でタイトルとそれぞれの記事の詳細情報のURLを取得
# 取得した情報をCSV・Excel・Googleスプレットシート・Lineに出力


# In[40]:


pip install webdriver-manager


# In[41]:


from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# In[42]:


def get_driver():
 
    # ヘッドレスモードを付与
    options = Options()
    options.add_argument("--headless")
 
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
 
    # 今回のスクレイピング対象サイト(Yahoo)
    url = 'https://www.yahoo.co.jp/'
 
    # SeleniumでURLを起動する
    driver.get(url)
 
    time.sleep(2)
 
    return driver


# In[43]:


def get_data_from_source_topic(driver):
 
    # 表示しているWebサイトのHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(driver.page_source,'lxml')
 
    # URLに news.yahoo.co.jp/pickup が含まれるものを抽出する。
    news_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
 
    # 見出しのURLをリスト形式にして返す
    news_link_lists = [data.attrs["href"] for data in news_list]
    title_detail = []
    i = 0
 
    # 見出しのYahooNewsをリストで持っているので、1件ずつ確認する
    for news_link in news_link_lists:
 
        # YahooNewsの見出し記事を1つずつクリックする
        driver.get(news_link)
        time.sleep(2)
      
        # 記事全文を読むボタンの要素
        search_btn = driver.find_element(By.XPATH,'//*[@id="uamods-pickup"]/div[2]/div/p/a')
 
        # 記事全文を読むボタンをクリック
        search_btn.click()
        time.sleep(2)
 
        # 記事全文を読むボタンをクリックした後の画面
        # 取得した要約ページをBeautifulSoupで解析できるようにする
        summary_soup = BeautifulSoup(driver.page_source,'html.parser')
 
        # class属性の中で「Direct」が含まれる行(ニュースの本文)を取得する
        detail = summary_soup.find(class_=re.compile("Direct"))
        
        # metaタグの中からURLを探す
        detail_Url = summary_soup.find_all('meta',content=re.compile("https://news.yahoo.co.jp/articles"))
 
        # 取得した内容をリスト変数へ書き込む
        if detail is not None:
            i = i + 1
            title_detail.append([i,summary_soup.title.text,detail.text,detail_Url[0]["content"]])
 
    return title_detail


# In[44]:


def get_data_from_source_country(driver):
    # 表示しているWebサイトのHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(driver.page_source,'lxml')
    
    #国内トピックのボタンの要素
    country_btn = driver.find_element(By.XPATH,'//*[@id="snavi"]/ul[1]/li[2]/a')
    
    #国内トピックのボタンをクリック
    country_btn.click()
    time.sleep(2)
    
    # 国内トピックのボタンをクリックした後の画面
    # 取得したページをBeautifulSoupで解析できるようにする
    country_soup = BeautifulSoup(driver.page_source,'lxml')
 
    # URLに news.yahoo.co.jp/pickup が含まれるものを抽出する。
    news_list = country_soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
 
    # 見出しのURLをリスト形式にして返す
    news_link_lists = [data.attrs["href"] for data in news_list]
    country_detail = []
    i = 0
 
    # 見出しのYahooNewsをリストで持っているので、1件ずつ確認する
    for news_link in news_link_lists:
 
        # YahooNewsの見出し記事を1つずつクリックする
        driver.get(news_link)
        time.sleep(2)
      
        # 記事全文を読むボタンの要素
        search_btn = driver.find_element(By.XPATH,'//*[@id="uamods-pickup"]/div[2]/div/p/a')
 
        # 記事全文を読むボタンをクリック
        search_btn.click()
        time.sleep(2)
 
        # 記事全文を読むボタンをクリックした後の画面
        # 取得した要約ページをBeautifulSoupで解析できるようにする
        summary_soup = BeautifulSoup(driver.page_source,'html.parser')
 
        # class属性の中で「Direct」が含まれる行(ニュースの本文)を取得する
        detail = summary_soup.find(class_=re.compile("Direct"))
        
        # metaタグの中からURLを探す
        detail_Url = summary_soup.find_all('meta',content=re.compile("https://news.yahoo.co.jp/articles"))
 
        # 取得した内容をリスト変数へ書き込む
        if detail is not None:
            i = i + 1
            country_detail.append([i,summary_soup.title.text,detail.text,detail_Url[0]["content"]])
 
    return country_detail


# In[45]:


def get_data_from_source_it(driver):
    # 表示しているWebサイトのHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(driver.page_source,'lxml')
    
    #itトピックのボタンの要素
    it_btn = driver.find_element(By.XPATH,'//*[@id="snavi"]/ul[1]/li[7]/a')
    
    #itトピックのボタンをクリック
    it_btn.click()
    time.sleep(2)
    
    # 国内トピックのボタンをクリックした後の画面
    # 取得したページをBeautifulSoupで解析できるようにする
    it_soup = BeautifulSoup(driver.page_source,'lxml')
 
    # URLに news.yahoo.co.jp/pickup が含まれるものを抽出する。
    news_list = it_soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
 
    # 見出しのURLをリスト形式にして返す
    news_link_lists = [data.attrs["href"] for data in news_list]
    it_detail = []
    i = 0
 
    # 見出しのYahooNewsをリストで持っているので、1件ずつ確認する
    for news_link in news_link_lists:
 
        # YahooNewsの見出し記事を1つずつクリックする
        driver.get(news_link)
        time.sleep(2)
      
        # 記事全文を読むボタンの要素
        search_btn = driver.find_element(By.XPATH,'//*[@id="uamods-pickup"]/div[2]/div/p/a')
 
        # 記事全文を読むボタンをクリック
        search_btn.click()
        time.sleep(2)
 
        # 記事全文を読むボタンをクリックした後の画面
        # 取得した要約ページをBeautifulSoupで解析できるようにする
        summary_soup = BeautifulSoup(driver.page_source,'html.parser')
 
        # class属性の中で「Direct」が含まれる行(ニュースの本文)を取得する
        detail = summary_soup.find(class_=re.compile("Direct"))
        
        # metaタグの中からURLを探す
        detail_Url = summary_soup.find_all('meta',content=re.compile("https://news.yahoo.co.jp/articles"))
 
        # 取得した内容をリスト変数へ書き込む
        if detail is not None:
            i = i + 1
            it_detail.append([i,summary_soup.title.text,detail.text,detail_Url[0]["content"]])
 
    return it_detail


# In[46]:


def get_data_from_source_economy(driver):
    # 表示しているWebサイトのHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(driver.page_source,'lxml')
    
    #itトピックのボタンの要素
    economy_btn = driver.find_element(By.XPATH,'//*[@id="snavi"]/ul[1]/li[4]/a')
    
    #itトピックのボタンをクリック
    economy_btn.click()
    time.sleep(2)
    
    # 国内トピックのボタンをクリックした後の画面
    # 取得したページをBeautifulSoupで解析できるようにする
    economy_soup = BeautifulSoup(driver.page_source,'lxml')
 
    # URLに news.yahoo.co.jp/pickup が含まれるものを抽出する。
    news_list = economy_soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
 
    # 見出しのURLをリスト形式にして返す
    news_link_lists = [data.attrs["href"] for data in news_list]
    economy_detail = []
    i = 0
 
    # 見出しのYahooNewsをリストで持っているので、1件ずつ確認する
    for news_link in news_link_lists:
 
        # YahooNewsの見出し記事を1つずつクリックする
        driver.get(news_link)
        time.sleep(2)
      
        # 記事全文を読むボタンの要素
        search_btn = driver.find_element(By.XPATH,'//*[@id="uamods-pickup"]/div[2]/div/p/a')
 
        # 記事全文を読むボタンをクリック
        search_btn.click()
        time.sleep(2)
 
        # 記事全文を読むボタンをクリックした後の画面
        # 取得した要約ページをBeautifulSoupで解析できるようにする
        summary_soup = BeautifulSoup(driver.page_source,'html.parser')
 
        # class属性の中で「Direct」が含まれる行(ニュースの本文)を取得する
        detail = summary_soup.find(class_=re.compile("Direct"))
        
        # metaタグの中からURLを探す
        detail_Url = summary_soup.find_all('meta',content=re.compile("https://news.yahoo.co.jp/articles"))
 
        # 取得した内容をリスト変数へ書き込む
        if detail is not None:
            i = i + 1
            economy_detail.append([i,summary_soup.title.text,detail.text,detail_Url[0]["content"]])
 
    return economy_detail


# In[47]:


driver  = get_driver()


# In[48]:


topics = get_data_from_source_topic(driver)


# In[49]:


countries = get_data_from_source_country(driver)


# In[50]:


its = get_data_from_source_it(driver)


# In[51]:


economys = get_data_from_source_economy(driver)


# In[82]:


import datetime
date = datetime.date.today()
import os 
os.chdir(r"C:\Users\natsu\OneDrive\ドキュメント\portfolio\ニュース")


# In[104]:


df1 = pd.DataFrame(topics,columns=["id","title","detail","url"])
filename1 = 'topic_' + date.strftime('%Y%m%d') +'.csv'
filename1_1 = 'topic_' + date.strftime('%Y%m%d') +'.xlsx'
df1.to_csv(filename1)
df1.to_excel(filename1_1)
df1=df1.astype(({"id": object}))


# In[90]:


df2 =  pd.DataFrame(countries,columns=["id","title","detail","url"])
filename2 = 'country_' + date.strftime('%Y%m%d') +'.csv'
filename2_1 = 'country_' + date.strftime('%Y%m%d') +'.xlsx'
df2.to_csv(filename2)
df2.to_excel(filename2_1)


# In[91]:


df3 =  pd.DataFrame(its,columns=["id","title","detail","url"])
filename3 = 'it_' + date.strftime('%Y%m%d') +'.csv'
filename3_1 = 'it_' + date.strftime('%Y%m%d') +'.xlsx'
df3.to_csv(filename3)
df3.to_excel(filename3_1)


# In[92]:


df4 =  pd.DataFrame(economys,columns=["id","title","detail","url"])
filename4 = 'economy_' + date.strftime('%Y%m%d') +'.csv'
filename4_1 = 'economy_' + date.strftime('%Y%m%d') +'.xlsx'
df4.to_csv(filename4)
df4.to_excel(filename4_1)


# In[94]:


get_ipython().system('pip install gspread')
get_ipython().system('pip install oauth2client')


# In[101]:


import gspread
from google.oauth2.service_account import Credentials


# お決まりの文句
# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = Credentials.from_service_account_file(r"C:\Users\natsu\OneDrive\ドキュメント\portfolio\profound-saga-367723-a12267a900e3.json", scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログイン。
gc = gspread.authorize(credentials)

#スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = '1AdBiKhnYhTide-pCYCQgAvDmkMpKeGR0NlorwgLuGgo'
# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)


# In[105]:


# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

# シートの一覧を取得する。（リスト形式）
worksheets = workbook.worksheets()
print(worksheets)

# シートを開く
worksheet = workbook.worksheet('シート1')

cell_list = worksheet.range('A1:D8')
for cell in cell_list:
    val = df1.iloc[cell.row-1][cell.col-1]
    cell.value = val

# スプレッドシートに書き出す
worksheet.update_cells(cell_list)

