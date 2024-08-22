import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 設定資料夾路徑
folder_path = r"D:\Python\專題\data source\2017~2024 boxoffice\title boxoffice"
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

title_df_dict = {}

# 讀取和合併每年的數據
for file in files:
    year = file.split(" ")[0]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)
    
    if year not in title_df_dict:
        title_df_dict[year] = df
    else:
        title_df_dict[year] = pd.concat([title_df_dict[year],df],ignore_index=True)
        
top_data_dict = {}

# 選擇每年票房前三高的電影
for year,df in title_df_dict.items():
    top_data = df.sort_values("總票房",ascending=False).head(3)
    top_data_dict[year] = top_data
    
# 初始化一個空的 DataFrame，用於存儲每年的國家和總票房
plot_df = pd.DataFrame(columns=["year", "title", "boxoffice"])

for year,df in top_data_dict.items():
    temp_df = pd.DataFrame({"year":df["年份"],
                            "title":df["片名"],
                            "boxoffice":df["總票房"]
                            })
    
    plot_df = pd.concat([plot_df,temp_df],ignore_index=True)     

plot_df["year"] = plot_df["year"].astype(int)
plot_df["boxoffice"] = plot_df["boxoffice"].astype(int)
plot_df["boxoffice(million)"] = np.round((plot_df["boxoffice"]/1000000),2)

plot_df.to_csv("2018年~2024年 總票房前三高電影.csv",encoding = "utf-8-sig")

#取出年份
years = list(title_df_dict.keys()) 

# 根據 'year' 和 'boxoffice' 進行排序
# 先根據 'year' 升序排序，再根據 'boxoffice' 降序排序
plot_df = plot_df.sort_values(by=['year', 'boxoffice'], ascending=[True, False])  

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"

# 設定畫布大小
plt.figure(figsize=(13,6))

# 設定長條圖的高度
bar_height = 0.25

year_indices = np.arange(len(years))

# 定義顏色
colors = ['#FF9933', '#026E81', '#0099DD']

# 繪製長條圖
for i in range(3):
    title_data = plot_df[plot_df.groupby('year').cumcount() == i]
    plt.barh(year_indices + i * bar_height,title_data["boxoffice(million)"],
             bar_height,label=f'Top {i+1}',color=colors[i],zorder=2)
    
plt.xlim(0,760)
plt.xlabel("總票房(百萬元)",fontsize=16)
plt.title("2018年~2024年 總票房前三高電影",fontsize=21)

plt.yticks(year_indices + bar_height, years,fontsize=14)
plt.xticks(fontsize=12)
plt.grid(axis="x",zorder=10)
plt.legend()

plt.savefig("2018年~2024年7月總票房前三高電影.png")

plt.show()
