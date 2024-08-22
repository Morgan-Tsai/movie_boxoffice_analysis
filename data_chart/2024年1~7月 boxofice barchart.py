import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 設定資料夾路徑
folder_path = r"C:\Users\user\Desktop\python專題\csv\data source\2024 janurary to july\country boxoffice"
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

country_boxoffice_df = {}

# 讀取和合併每月的數據
for file in files:
    month = file.split(" ")[1]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)

    if month not in country_boxoffice_df:
        country_boxoffice_df[month] = df
    else:
        country_boxoffice_df[month] = pd.concat([country_boxoffice_df[month],df],ignore_index=True)
        
top3_data_dict = {}

# 選擇每月票房前三高的出產國家
for month,df in country_boxoffice_df.items():
    top3_data = df.sort_values("總票房",ascending=False).head(3)
    top3_data_dict[month] = top3_data

# 初始化一個空的 DataFrame，用於存儲每個月的國家和總票房
plot_df = pd.DataFrame(columns=["month", "country", "boxxoffice"])

for month,df in top3_data_dict.items():
    # 為每個月份創建一個新的 DataFrame，包含該月份的前三個國家及其總票房
    temp_df = pd.DataFrame({"month":[month]*3,
                            "country":df["國家"].values,
                            "boxxoffice":df["總票房"].values})
    
    plot_df = pd.concat([plot_df,temp_df], ignore_index=True)
plot_df["boxxoffice"] = plot_df["boxxoffice"].astype(int)
plot_df["boxxoffice(millons)"] = np.round((plot_df["boxxoffice"]/1000000),2)

# 定義月份的順序
months_order = ["january", "february", "march", "april", "may", "june", "july"]

# 定義月份顯示的文字
month_display = ["1月","2月","3月","4月","5月","6月","7月"]

# 獲取plot_df的國家
countries = plot_df['country'].unique()

# 創建一個字典，用於將月份映射到其順序
month_order_dict = {month: i for i, month in enumerate(months_order)}

# 將每個月份映射到其對應的順序值
plot_df['month_order'] = plot_df['month'].map(month_order_dict)

# 根據 'month_order' 和 'times' 進行排序
# 先根據 'month_order' 升序排序，再根據 'times' 降序排序
plot_df = plot_df.sort_values(by=["month_order", "boxxoffice(millons)"], ascending=[True, False])

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"

# 設定畫布大小
plt.figure(figsize=(13,6))

# 設定長條圖的寬度
bar_width = 0.25

# 生成一個數組，包含從 0 到 months_order 長度的整數索引
month_indices = np.arange(len(months_order))

# 定義顏色
colors = ['#FA3620', '#FA74AF', '#137BFA']

# 繪製長條圖
for i in range(3):
    country_data = plot_df[plot_df.groupby('month').cumcount() == i]
    plt.bar(month_indices + i * bar_width, country_data['boxxoffice(millons)'], 
    bar_width, label=f'Top {i+1}',color=colors[i],zorder=2)
    
plt.ylim(0,370)
plt.ylabel("總票房(百萬元)",fontsize=16)
plt.title("2024年 1~7月 總票房前三高國家",fontsize=21)

plt.xticks(month_indices + bar_width, month_display,fontsize=14)
plt.yticks(fontsize=12)
plt.grid(axis="y",zorder=10)
plt.legend()

# for i in range(3):
#     country_data = plot_df[plot_df.groupby('month').cumcount() == i]
#     for j, (index, row) in enumerate(country_data.iterrows()):
#         plt.text(j + i * bar_width, row['boxxoffice(millons)'], f"{row['country']}\n{row['boxxoffice(millons)']}", 
#                   ha='center', va='bottom')

#plt.savefig("2024年1~7月總票房前三高國家.png")

plt.show()

