import pandas as pd
from matplotlib import pyplot as plt

file_positon = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~2024 國片總票房.csv"
file2_position = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~2024 國片與非國片上映數.csv"

tw_boxoffice_df = pd.read_csv(file_positon)
onscreen_df = pd.read_csv(file2_position)

year=["2018","2019","2020","2021","2022","2023","2024"]

plt.rcParams["font.family"] = "Microsoft JhengHei"

plt.figure(figsize=(11, 6),num=1)
plt.bar(year,onscreen_df["非國片上映數"],width=0.5,label="非國片上映數",color="#E06216",zorder=10)
plt.bar(year,onscreen_df["國片上映數"],width=0.5,label="國片上映數",bottom=onscreen_df["非國片上映數"],color="#E09861",zorder=10)
plt.legend()

plt.ylim(0,1200)
plt.grid(axis="y",zorder=0)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.ylabel("電影上映數(部)",fontsize=17)
plt.title("2018年~2024年 國片和非國片上映數",fontsize=20)
plt.savefig("2018年~2024年國片和非國片上映數.png")

plt.figure(figsize=(11, 6),num=2)
plt.plot(year,tw_boxoffice_df["國片票房(億)"],marker="o",lw=4,markersize=11,c="#164FE0")
plt.ylim(0,11)
plt.grid(axis="y")
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.ylabel("總票房(億元)",fontsize=14)
plt.title("2018年~2024年 國片總票房",fontsize=20)
plt.savefig("2018年~2024年國片總票房.png")

plt.show()