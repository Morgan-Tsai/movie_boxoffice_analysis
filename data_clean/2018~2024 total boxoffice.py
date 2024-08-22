import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os

folder_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\boxoffice"

files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

boxoffice_df_dict={}
boxoffice_df2_dict={}


# 讀取和合併每月的數據
for file in files:
    year = file.split(" ")[0]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)

    if year not in boxoffice_df_dict:
        boxoffice_df_dict[year] = df
    else:
        boxoffice_df_dict[year] = pd.concat([boxoffice_df_dict[year],df],ignore_index=True)

boxoffice_df_dict["2018"]["銷售金額"] = boxoffice_df_dict["2018"]["銷售金額"].str.replace(",","").astype(int)

# for year,df in boxoffice_df_dict.items():
#     df["銷售票數"] = df["銷售票數"].str.replace(",","").astype(int)

taiwan_movies_dict={}
foreign_movies_dict={}
taiwan_boxoffice_dict={}
taiwan_onscreen_dict={}
foreign_onscreen_dict={}

for year,df in boxoffice_df_dict.items():
    df["年份"] = year
    taiwan_movies = df[df["國別地區"] == "中華民國"]
    taiwan_movies_dict[year] = taiwan_movies
    
    foreign_movies = df[df["國別地區"] != "中華民國"]
    foreign_movies_dict[year] = foreign_movies
    
for year,df in taiwan_movies_dict.items():
    #df["年份"] = year
    boxoffice = df["銷售金額"].sum()
    taiwan_boxoffice_dict[year]=boxoffice
    
    onscreen = df.drop_duplicates(subset=["中文片名"], keep="last").reset_index()
    taiwan_onscreen_dict[year] = len(onscreen)
 
taiwan_boxoffice_dict["2020"] = taiwan_boxoffice_dict["2020"].astype(int)
taiwan_boxoffice_dict["2021"] = taiwan_boxoffice_dict["2021"].astype(int)
taiwan_boxoffice_dict["2022"] = taiwan_boxoffice_dict["2022"].astype(int)

for year,df in foreign_movies_dict.items():
    onscreen1 = df.drop_duplicates(subset=["中文片名"], keep="last").reset_index()
    foreign_onscreen_dict[year] = len(onscreen1)
       
onscreen_df = pd.DataFrame({"年份":list(taiwan_onscreen_dict.keys()),
                            "國片上映數":list(taiwan_onscreen_dict.values()),
                            "非國片上映數":list(foreign_onscreen_dict.values())}) 
onscreen_df.to_csv("2018~2024 國片與非國片上映數.csv",encoding="utf-8-sig") 

taiwan_boxoffice_df = pd.DataFrame({"年份":list(taiwan_boxoffice_dict.keys()),
                                    "國片票房":list(taiwan_boxoffice_dict.values())})

taiwan_boxoffice_df["國片票房(億)"] = np.round((taiwan_boxoffice_df["國片票房"]/100000000),2)

taiwan_boxoffice_df.to_csv("2018~2024 國片總票房.csv",encoding="utf-8-sig") 

for year,df in boxoffice_df_dict.items():
  
    # 檢查欄位是否存在，若存在則提取
    if all(col in df.columns for col in ["國別地區", "中文片名", "銷售金額"]):
        boxoffice_df2_dict[year] = df[["國別地區", "中文片名", "銷售金額"]]
    else:
        missing_cols = [col for col in ["國別地區", "中文片名", "銷售金額"] if col not in df.columns]
        print(f"Year {year} is missing columns: {missing_cols}")
        
   
boxoffice_df3 = pd.DataFrame(columns=["國家", "片名", "總票房"])

for year,df in boxoffice_df2_dict.items():
    # print("%d dataframe:" %int(year))
    # print(df.info())
    
    temp_df = df.rename(columns={"國別地區": "國家", "中文片名": "片名", "銷售金額": "總票房"})
    boxoffice_df3 = pd.concat([boxoffice_df3, temp_df], ignore_index=True)
    
boxoffice_df3["總票房"] = boxoffice_df3["總票房"].astype(int)        
#boxoffice_df3.to_csv("2018~202407 total boxoffice.csv",encoding="utf-8-sig")
    