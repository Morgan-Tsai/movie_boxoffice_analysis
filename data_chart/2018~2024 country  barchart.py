import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 設定資料夾路徑
folder_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\country"
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

country_df2_dict={}

# 讀取和合併每月的數據
for file in files:
    year = file.split(" ")[0]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)
    
    if year not in country_df2_dict:
        country_df2_dict[year] = df
    else:
        country_df2_dict[year] = pd.concat([country_df2_dict[year],df],ignore_index=True)

#取出年份
years = list(country_df2_dict.keys())        
top_data_df_dict = {}

# 選擇每年上映片數前三高的出產國家
for year,df in country_df2_dict.items():
    df["年份"] = year
    top_data = df.sort_values("電影數量",ascending=False).head(3)
    top_data_df_dict[year] = top_data
    
# 初始化一個空的 DataFrame，用於存儲每個月的國家和電影數量
plot_df = pd.DataFrame(columns=["year", "country", "num"])

for year,df in top_data_df_dict.items():
    # 為每個月份創建一個新的 DataFrame，包含該年份的前三個國家及其電影數量
    temp_df = pd.DataFrame({"year":df["年份"],
                            "country":df["產地"],
                            "num":df["電影數量"]})
    
    plot_df = pd.concat([plot_df,temp_df],ignore_index=True)
    
plot_df["year"] = plot_df["year"].astype(int)
plot_df["num"] = plot_df["num"].astype(int)


# 根據 'year' 和 'num' 進行排序
# 先根據 'year' 升序排序，再根據 'num' 降序排序
plot_df = plot_df.sort_values(by=['year', 'num'], ascending=[True, False])

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"

# 設定畫布大小
plt.figure(figsize=(12,6))

# 設定長條圖的寬度
bar_width = 0.25

# 生成一個數組，包含從 0 到 year 長度的整數索引
year_indices = np.arange(len(years))

# 定義顏色
colors = ['#FA3A31', '#FA9720', '#207BFA']

# 繪製長條圖
for i in range(3):
    country_data = plot_df[plot_df.groupby('year').cumcount() == i]
    plt.bar(year_indices + i * bar_width, country_data['num'], 
            bar_width, label=f'Top {i+1}',color=colors[i],zorder=2)
    
plt.ylim(0,300)
plt.ylabel("電影上映數(部)",fontsize=14)
plt.title("2018年~2024年7月 上映片數前三高國家",fontsize=21)

plt.xticks(year_indices + bar_width, years,fontsize=14)
plt.yticks(fontsize=12)
plt.grid(axis="y",zorder=10)
plt.legend()

plt.savefig("2018年~2024年7月上映片數前三高國家.png")

plt.show()

