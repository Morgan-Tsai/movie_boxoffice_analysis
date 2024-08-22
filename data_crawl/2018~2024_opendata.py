from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import time
import chardet

#全國電影票房統計數據 資料來源
url = "https://data.gov.tw/dataset/94224"

try:
    response = requests.get(url) #發送請求
    response.raise_for_status() #請求失敗的異常處理
    soup = BeautifulSoup(response.text,"lxml") #解析HTML
    
    #第一層搜尋：找到主要的表格區塊
    data1 = soup.find("div",class_="table table--fixed od-table od-table--bordered print-table")
    
    #初始化一個列表來存儲所有找到的 CSV 檔案連結
    link_list =[] 
    
    if data1:
        #第二層搜尋：在主要表格區塊中找到所有包含 href 屬性的 <a> 標籤
        for row in data1.find_all("a",href=True):
           #獲取 <a> 標籤中的 href 屬性值，即連結地址
           csv_link = row.get("href")
           
           #檢查連結是否以 ".csv" 結尾
           if csv_link.endswith(".csv"):
               #如果是 CSV 檔案連結，將其添加到 link_list 列表中
               csv_url = csv_link 
               link_list.append(csv_url)
       
               #確保連結是完整 URL
               if not csv_url.startswith('http'):
                  csv_url = 'https://data.gov.tw' + csv_url
    
    # 初始化一個空的 DataFrame 用於合併所有 CSV
    combined_df = pd.DataFrame()
    # 開始計時
    start_time = time.time()
    # 迭代所有找到的 CSV 檔案連結
    for i, csv_url in enumerate(link_list, start=1):
        try:
             # 讀取 CSV 內容到內存中
             csv_response = requests.get(csv_url)
             csv_response.raise_for_status()
                  
             # 使用 chardet 檢測編碼
             raw_data = csv_response.content
             result = chardet.detect(raw_data)
             encoding = result['encoding'] 
             
             # 使用 StringIO 讀取內存中的 CSV 內容
             csv_data = StringIO(raw_data.decode(encoding))
                   
             # 讀取 CSV 到 DataFrame
             df = pd.read_csv(csv_data, encoding=encoding)
                   
             # 合併到主 DataFrame 中
             combined_df = pd.concat([combined_df, df], ignore_index=True)
                   
             # 打印當前處理完成的檔案編號
             print(f"第 {i} 個檔案處理完成")

        except requests.exceptions.RequestException as e:
             print(f"檔案 {i} 讀取失敗:", e.reason)
        except pd.errors.ParserError as e:
             print(f"檔案 {i} 解析失敗:", e.reason)  
         
         # 每處理完一個檔案，暫停一段時間
        time.sleep(2)  # 暫停2秒
     
     # 停止計時
    end_time = time.time()
    total_time = end_time - start_time
     
     # 保存合併後的 DataFrame 為 CSV 文件
    combined_df.to_csv('TWmovie_combined_data.csv', index=False)
         
    print("所有 DataFrame 已合併並保存為 TWmovie_combined_data.csv")
    print(combined_df.head())  # 顯示前幾行資料
    print(f"處理總時間: {total_time} 秒")
    
    
               
except requests.exceptions.RequestException as e:
    print("網頁讀取失敗"+ e.reason)
