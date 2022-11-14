#!/usr/bin/env python
# coding: utf-8

# In[96]:


from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin


# In[ ]:


# ターゲットURLからdriverの設定
# データの格納先
#①（URL、アドレス、名称、家賃、敷金、構造、礼金、管理費、築年数、間取り、面積、アクセス）を抽出
# 次ページにアクセス
# ①を繰り返す


# In[144]:


def get_driver():
 
    # ヘッドレスモードを付与
    options = Options()
    options.add_argument("--headless")
 
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
 
    # 今回のスクレイピング対象サイト(Yahoo)
    url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=050&bs=040&ta=23&sa=01&sngz=&po1=25&pc=50'
 
    # SeleniumでURLを起動する
    driver.get(url)
 
    time.sleep(2)
 
    return driver


# In[145]:


def get_data(driver):
    time.sleep(1)
    # 表示しているWebサイトのHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(driver.page_source,'lxml')
    # ヘッダーのテーブルから建物ひとつひとつのデータ
    header_table = soup.find_all(class_ = "cassetteitem_content")
    info = []
    for header_data in header_table:
        # ヘッダーの中の名前、住所、最寄り駅、築年数、建物高さ    
        name = header_data.find(class_ = "cassetteitem_content-title").text
        address = header_data.find(class_ = "cassetteitem_detail-col1").text
        stations = header_data.find(class_ = "cassetteitem_detail-col2").find_all(class_ = "cassetteitem_detail-text")
        station = [station.text for station in stations]
        station = '--'.join(station)
        Col3 = header_data.find(class_ = "cassetteitem_detail-col3").find_all("div")
        age = Col3[0].text
        hight = Col3[1].text
        header_data=[name,address,station,age,hight]
        #アイテムのテーブルから部屋ひとつひとつのデータ
        item_table = soup.find(class_ = "cassetteitem_other")
        room_table = []
        for room in item_table.find_all("tbody"):
            rooms_table =[]
            append = rooms_table.append
            append(room.find_all("td")[2].text.replace('\t','').replace('\n',''))
            append(room.find(class_ = "cassetteitem_other-emphasis ui-text--bold").text)
            append(room.find(class_ = "cassetteitem_price cassetteitem_price--administration").text)
            append(room.find(class_ = "cassetteitem_price cassetteitem_price--deposit").text)
            append(room.find(class_ = "cassetteitem_price cassetteitem_price--gratuity").text)
            append(room.find(class_ = "cassetteitem_madori").text)
            append(room.find(class_ = "cassetteitem_menseki").text)
            url = room.find(class_="js-cassette_link_href cassetteitem_other-linktext").get("href")
            full_url = urljoin("https://suumo.jp/",url)
            append(full_url)
            rooms_table.extend(header_data)
            room_table.append(rooms_table)
            info.extend(room_table)
    time.sleep(2)
    return info


# In[146]:


def next_page(driver):
    data = []
    # 1ページ目の次のページ（2ページ目）のURLを取得
    next_page_url = driver.find_element(By.XPATH,'//*[@id="js-leftColumnForm"]/div[11]/div[2]/p/a').get_attribute("href")
    
    # 2ページ目から最終ページまでをループ処理する
    while len(next_page_url) > 0:
        driver.get(next_page_url)
        #要素がロードされるまでの待ち時間を10秒に設定
        driver.implicitly_wait(10)
        next_page_html = driver.page_source.encode('utf-8')

        data.extend(get_data(driver))
        try:
            next_page_url = driver.find_element(By.XPATH,'//*[@id="js-leftColumnForm"]/div[11]/div[2]/p[2]/a').get_attribute("href")
        except:
            break
    print("\n\n最後のページの処理が終わりました。\n\n")
    df = pd.DataFrame(data,columns = ['階','賃料','管理費','敷金','礼金','間取り','専有面積','URL','名称','住所','最寄り駅','築年数','建物の高さ'])
    df = df[['名称','住所','最寄り駅','築年数','建物の高さ','階','賃料','管理費','敷金','礼金','間取り','専有面積','URL']]
    return df


# In[147]:


driver = get_driver()


# In[149]:


df=next_page(driver)


# In[161]:


import re 
 
def get_number(value):
    n = re.findall(r"[0-9.]+", value)
    
    if len(n)!=0:
        return float(n[0])
    else:
        return 0
    
df["賃料"] = df["賃料"].apply(get_number)
df["管理費"] = df["管理費"].apply(get_number)
df["管理費"] = df["管理費"] / 10000
df["敷金"] = df["敷金"].apply(get_number)
df["礼金"] = df["礼金"].apply(get_number)
df["専有面積"] = df["専有面積"].apply(get_number)
df["築年数"] = df["築年数"].apply(get_number)


# In[163]:





# In[ ]:




