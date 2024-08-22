import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 設定資料夾路徑
folder_path = r"D:\Python\專題\data source\2024 janurary to july\title boxoffice"
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

title_df_dict = {}

# 讀取和合併每月的數據
for file in files:
    month = file.split(" ")[1]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)
    
    if month not in title_df_dict:
        title_df_dict[month] = df
    else:
        title_df_dict[month] = pd.concat([title_df_dict[month],df],ignore_index=True)
        
top_data_dict = {}

# 選擇每月票房前三高的電影
for month,df in title_df_dict.items():
    top_data = df.sort_values("總票房",ascending=False).head(3)
    top_data_dict[month] = top_data

# 初始化一個空的 DataFrame，用於存儲每個月的國家和總票房
plot_df = pd.DataFrame(columns=["month", "title", "boxoffice"])

for month,df in top_data_dict.items():
    temp_df = pd.DataFrame({"month":df["月份"],
                            "title":df["片名"],
                            "boxoffice":df["總票房"]
                            })
    
    plot_df = pd.concat([plot_df,temp_df],ignore_index=True) 
    
plot_df["boxoffice"] = plot_df["boxoffice"].astype(int)
plot_df["boxoffice(million)"] = np.round((plot_df["boxoffice"]/1000000),2) 

# 獲取plot_df的片名
titles = plot_df['title'].unique()

# 定義月份的順序
months_order = ["january", "february", "march", "april", "may", "june", "july"]

# 定義月份顯示的文字
month_display = ["1月","2月","3月","4月","5月","6月","7月"]

# 創建一個字典，用於將月份映射到其順序
month_order_dict = {month: i for i, month in enumerate(months_order)}

# 將每個月份映射到其對應的順序值
plot_df['month_order'] = plot_df['month'].map(month_order_dict)

# 根據 'month_order' 和 'boxoffice(million)' 進行排序
# 先根據 'month_order' 升序排序，再根據 'boxoffice(million)' 降序排序
plot_df = plot_df.sort_values(by=["month_order", "boxoffice(million)"], ascending=[True, False])

plot_df.to_csv("2024年1~7月總票房前三高電影.csv",encoding="utf-8-sig")

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"

# 設定畫布大小
plt.figure(figsize=(13,6))

# 設定長條圖的高度
bar_height = 0.25

# 生成一個數組，包含從 0 到 months_order 長度的整數索引
month_indices = np.arange(len(months_order))

# 定義顏色
colors = ['#F26C50', '#E3C859', '#59B2E3']

# 繪製長條圖
for i in range(3):
    title_data = plot_df[plot_df.groupby('month').cumcount() == i]
    plt.barh(month_indices + i * bar_height,title_data["boxoffice(million)"],
             bar_height,label=f'Top {i+1}',color=colors[i],zorder=2)

plt.xlim(0,250)
plt.xlabel("總票房(百萬元)",fontsize=16)
plt.title("2024年1~7月 總票房前三高電影",fontsize=21)

plt.yticks(month_indices + bar_height, month_display,fontsize=14)
plt.xticks(fontsize=12)
plt.grid(axis="x",zorder=10)
plt.legend()

plt.savefig("2024年1~7月總票房前三高電影.png")

plt.show()

