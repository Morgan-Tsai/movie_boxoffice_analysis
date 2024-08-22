from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import BytesIO
import time
import sqlite3

url = "https://www.tfai.org.tw/boxOffice/weekly"

try:
    response = requests.get(url) #發送請求
    response.raise_for_status() #請求失敗的異常處理
    soup = BeautifulSoup(response.text,"lxml") #解析HTML
    
    data1 = soup.find("section",class_="box-office-frame")
    
    data2 = data1.find_all("div",class_="download-link")
    
    link_list = []
    total_boxoffice_df = pd.DataFrame()
    
    for row in data2:
        sibling = row.find_previous_sibling("span",class_="title")
        
        if sibling and "2018" in sibling.text:
            links = row.find("a",class_="xls")
            if links and 'href' in links.attrs:
                href = links['href']
                
                if not href.startswith('http'):
                    href = 'https://www.tfai.org.tw/' + href
                    
                link_list.append(href)        
    
    
    link_list.reverse()      
    #link_list = link_list[50:]
    
    for i,link in enumerate(link_list,start=1):
        try:     
            time.sleep(2)
            
            xlsx_response = requests.get(link)
            xlsx_response.raise_for_status()
       
            file_content = BytesIO(xlsx_response.content)
       
            boxoffice_df = pd.read_excel(file_content)
       
            total_boxoffice_df = pd.concat([total_boxoffice_df,boxoffice_df],ignore_index=True)
            
            print(f"第 {i} 個檔案處理完成") 
            
            
        except requests.exceptions.RequestException as e:
          print(f"檔案 {i} 讀取失敗:", e.reason)
        
    #total_boxoffice_df.to_csv("2018 movie boxoffice.csv",index=False,encoding="utf-8")
    
    
    print("所有 DataFrame 已合併並保存為 2018 movie boxoffice.csv")
    
    
    #print(len(link_list))
    print(link_list)
    #print(total_boxoffice_df.head())  # 顯示前幾行資料
    
except requests.exceptions.RequestException as e:
    print("網頁讀取失敗"+ e.reason)
    







