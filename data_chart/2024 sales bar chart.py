import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

file2_path = r"C:\Users\user\Desktop\python專題\csv\data source\2024 janurary to july\other\2024 total sales2.csv"
file3_path = r"C:\Users\user\Desktop\python專題\csv\data source\2024 janurary to july\other\2024 averge boxoffice.csv"
sales_df = pd.read_csv(file2_path)
avg_boxoffice = pd.read_csv(file3_path)
# print(sales_df.info())
sales_df["總售票數"]= sales_df["總售票數"].astype(int)
avg_boxoffice["平均票房"] = avg_boxoffice["平均票房"].astype(int)
sales_df["總票房(億)"] = np.round((sales_df["總票房"]/100000000),2)
sales_df["總售票數(萬)"] = np.round((sales_df["總售票數"]/10000),2)
avg_boxoffice["平均票房(萬)"] = np.round((avg_boxoffice["平均票房"]/10000),2)

plt.rcParams["font.family"] = "Microsoft JhengHei"

plt.figure(figsize=(11,6),num=1)

month = ["1月","2月","3月","4月","5月","6月","7月"]

plt.plot(month,sales_df["總票房(億)"],marker="o",lw=4,markersize=11,c="#107DEB")
plt.ylim(0,6)
plt.grid(axis="y")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("總票房(億元)",fontsize=14)
plt.title("2024年 1~7月總票房",fontsize=21)
#plt.savefig("2024 1~7月 total boxoffice.png")

plt.figure(figsize=(11,6),num=2)

plt.plot(month,sales_df["總售票數(萬)"],marker="o",lw=4,markersize=11,c="#EB5B10")
plt.ylim(60,200)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.grid(axis="y")
plt.ylabel("總售票數(萬張)",fontsize=14)
plt.title("2024年 1~7月總售票數",fontsize=21)
#plt.savefig("2024年1~7月總售票數.png")

plt.figure(figsize=(11,6),num=3)
plt.plot(month,avg_boxoffice["平均票房(萬)"],marker="o",lw=4,markersize=11,c="#EB81A5")
plt.ylim(100,400)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.grid(axis="y")
plt.ylabel("平均票房(萬元)",fontsize=14)
plt.title("2024年 1~7月平均票房",fontsize=21)
#plt.savefig("2024 1~7月 average boxoffice.png")

plt.show()

"""
plt.bar(month,sales_df["總票房(百萬)"],width=0.5)
plt.ylabel("總票房(百萬)",fontsize=14)
plt.title("2024年 1~7月電影票房",fontsize=17)
#plt.ylim(2000,4000)

plt.figure(figsize=(12, 6),num=2)
plt.bar(month,sales_df["總售票數(萬)"],width=0.5)
plt.ylabel("總售票數(萬)",fontsize=14)
plt.title("2024年 1~7月電影售票數",fontsize=17)
#plt.ylim(850,1500)
plt.show()
"""