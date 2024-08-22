import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

file_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~2024 total sales.csv"
file2_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~2024 total movie onscreeen.csv"
file3_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~2024 average boxoffice.csv"

total_sales_df = pd.read_csv(file_path)
total_onscreeen_df = pd.read_csv(file2_path)
avg_boxoffice_df = pd.read_csv(file3_path)

avg_boxoffice_df["平均票房"] = avg_boxoffice_df["平均票房"].astype(int)
total_sales_df["總售票數(萬)"] = np.round((total_sales_df["總售票數"]/10000),2)
total_sales_df["總票房(億)"] = np.round((total_sales_df["總票房"]/100000000),2)
avg_boxoffice_df["平均票房(萬)"] = np.round((avg_boxoffice_df["平均票房"]/10000),2)
total_onscreeen_df["舊片上映數"] = total_onscreeen_df["電影上映數"] - total_onscreeen_df["新片上映數"]

year=["2018","2019","2020","2021","2022","2023","2024"]

plt.rcParams["font.family"] = "Microsoft JhengHei"

plt.figure(figsize=(11, 6),num=1)
plt.bar(year,total_onscreeen_df["舊片上映數"],width=0.5,label="舊片上映數",color="#105DEB",zorder=10)
plt.bar(year,total_onscreeen_df["新片上映數"],width=0.5,label="新片上映數",bottom=total_onscreeen_df["舊片上映數"],color="#34A5EA",zorder=10)
plt.legend()

plt.ylim(0,1200)
plt.grid(axis="y",zorder=0)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.ylabel("電影上映數(部)",fontsize=17)
plt.title("2018年~2024年7月 電影上映數",fontsize=20)
#plt.savefig("2018年~2024年7月電影上映數.png")

plt.figure(figsize=(11, 6),num=2)
plt.plot(year,total_sales_df["總票房(億)"],marker="o",lw=4,markersize=11,c="#EA721A")
plt.ylim(0,90)
plt.grid(axis="y")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("總票房(億元)",fontsize=14)
plt.title("2018年~2024年7月 總票房",fontsize=21)
#plt.savefig("2018年~2024年7月總票房.png")

plt.figure(figsize=(11, 6),num=3)
plt.plot(year,total_sales_df["總售票數(萬)"],marker="o",lw=4,markersize=11,c="#F04D7E")
plt.ylim(750,3500)
plt.grid(axis="y")
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.ylabel("總售票數(萬張)",fontsize=14)
plt.title("2018年~2024年7月 總售票數",fontsize=21)
#plt.savefig("2018年~2024年7月總售票數.png")

plt.figure(figsize=(11, 6),num=4)
plt.plot(year,avg_boxoffice_df["平均票房(萬)"],marker="o",lw=4,markersize=11,c="#F056C1")
plt.ylim(300,900)
plt.grid(axis="y")
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.ylabel("平均票房(萬元)",fontsize=14)
plt.title("2018年~2024年7月 平均票房",fontsize=20)
#plt.savefig("2018年~2024年7月平均票房.png")

plt.show()

