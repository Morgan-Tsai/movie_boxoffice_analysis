import pandas as pd
from matplotlib import pyplot as plt

file1_path = r"C:\Users\user\Desktop\python專題\csv\data source\2024 janurary to july\other\2024 total movie onscreeen.csv"

onscreeen_df = pd.read_csv(file1_path)

# print(onscreeen_df.info())

onscreeen_df["舊片上映數"] = onscreeen_df["電影上映數"] - onscreeen_df["新片上映數"]

plt.rcParams["font.family"] = "Microsoft JhengHei"

plt.figure(figsize=(10, 6))

month = ["1月","2月","3月","4月","5月","6月","7月"]

plt.bar(month,onscreeen_df["舊片上映數"],width=0.5,label="舊片上映數",color="#E85946",zorder=10)
plt.bar(month,onscreeen_df["新片上映數"],width=0.5,label="新片上映數",bottom=onscreeen_df["舊片上映數"],color="#E8AB46",zorder=10)
plt.legend()

plt.ylim(0,220)
plt.grid(axis="y",zorder=0)
plt.ylabel("電影上映數(部)",fontsize=17)
plt.title("2024年 1~7月上映電影數",fontsize=21)

plt.savefig("2024 1~7月 onscreen.png")

plt.show()


