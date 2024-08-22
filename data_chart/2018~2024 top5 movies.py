import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\other\2018~202407 total boxoffice.csv"

total_boxoffice_df = pd.read_csv(file_path)

#區分國片和非國片
taiwan_movies = total_boxoffice_df[total_boxoffice_df["國家"] == "中華民國"]
foreign_movies = total_boxoffice_df[total_boxoffice_df["國家"] != "中華民國"]

#依片名加總票房
total_boxoffice2 = total_boxoffice_df.groupby("片名")["總票房"].sum().reset_index()
taiwan_movies2 = taiwan_movies.groupby("片名")["總票房"].sum().reset_index()
foreign_movies2 = foreign_movies.groupby("片名")["總票房"].sum().reset_index()


#票房前五高的電影(整體)
top5_boxoffice_total = total_boxoffice2.sort_values("總票房",ascending=False).head(5)

#票房前五高的電影(國片)
taiwan_top5 = taiwan_movies2.sort_values("總票房",ascending=False).head(5)

#票房前五高的電影(非國片)
foreign_top5 = foreign_movies2.sort_values("總票房",ascending=False).head(5)


top5_boxoffice_total.to_csv("2018~202407 票房前五名電影.csv",encoding="utf-8-sig")
taiwan_top5.to_csv("2018~202407 票房前五名台灣電影.csv",encoding="utf-8-sig")
foreign_top5.to_csv("2018~202407 票房前五名非國片.csv",encoding="utf-8-sig")






