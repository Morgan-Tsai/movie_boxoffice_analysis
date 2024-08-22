import pandas as pd
import os

# 指定資料夾路徑
folder_path = r"C:\Users\user\Desktop\python專題\csv\data source\2017~2024 boxoffice\boxoffice"

# 列出資料夾中的所有 CSV 檔案
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

yearly_data_dict = {}

#讀取檔案並存在字典裡
for file in files:
    year = file.split(" ")[0]
    file_path = os.path.join(folder_path,file)
    df = pd.read_csv(file_path)
    
    if year not in yearly_data_dict:
        yearly_data_dict[year] = df
    else:
        yearly_data_dict[year] = pd.concat([yearly_data_dict[year], df], ignore_index=True)
  
#查看每一年dataframe的資訊
#for year,df in yearly_data_dict.items():
#    print(df.info())

#2017、2018的累計銷售票數和累計銷售金額 
yearly_data_dict["2018"]["銷售票數"] = yearly_data_dict["2018"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2018"]["銷售金額"] = yearly_data_dict["2018"]["銷售金額"].str.replace(",","").astype(int)
yearly_data_dict["2019"]["銷售票數"] = yearly_data_dict["2019"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2020"]["銷售票數"] = yearly_data_dict["2020"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2020"]["銷售金額"] = yearly_data_dict["2020"]["銷售金額"].astype(int)
yearly_data_dict["2021"]["銷售票數"] = yearly_data_dict["2021"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2021"]["銷售金額"] = yearly_data_dict["2021"]["銷售金額"].astype(int)
yearly_data_dict["2022"]["銷售票數"] = yearly_data_dict["2022"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2022"]["銷售金額"] = yearly_data_dict["2022"]["銷售金額"].astype(int)
yearly_data_dict["2023"]["銷售票數"] = yearly_data_dict["2023"]["銷售票數"].str.replace(",","").astype(int)
yearly_data_dict["2024"]["銷售票數"] = yearly_data_dict["2024"]["銷售票數"].str.replace(",","").astype(int)

#把每一年的上映日期轉成日期格式
for year,df in yearly_data_dict.items():
    df["上映日期"] = pd.to_datetime(df["上映日期"], errors='coerce')
    #print(f"{year} info：")
    #print(df.info())

yearly_data_dict2 = {}
country_df_dict = {}
total_boxoffice_df_dict = {}
total_tickets_df_dict = {}
movie_onscreen_df_dict={}
new_movie_df_dict={}
boxoffice_by_country_df_dict ={}

#排除每一年重複的電影並保留最後一筆
for year,df in yearly_data_dict.items():
    final_df = df.drop_duplicates(subset=["中文片名"], keep="last").reset_index()
    yearly_data_dict2[year] = final_df   


for year,df in yearly_data_dict2.items():
    #查看每一年dataframe的資訊
    #print(f"{year} info：")
    #print(df.info()) 
    
    #計算國家重複次數
    duplicate_country = df["國別地區"].value_counts().reset_index()
    duplicate_country.columns = ["產地","電影數量"]
    country_df_dict[year] = duplicate_country
    #csv_filename = ("%s country count.csv" %year)
    #duplicate_country.to_csv(csv_filename,encoding ="utf-8-sig")
    
    #計算每年的總上映片數
    movie_onscreen = len(df)
    movie_onscreen_df_dict[year] = movie_onscreen
    
    #計算每年的總新片上映片數
    new_movie = df[df["上映日期"].dt.year == int(year)]  
    new_movie_df_dict[year] = len(new_movie) 

boxoffice_by_titles_df_dict={}

for year,df in yearly_data_dict.items():
    #計算每年的總售票數
    total_tickets = df["銷售票數"].sum()
    total_tickets_df_dict[year] = total_tickets
    
    #計算每年的總票房
    total_boxoffice = df["銷售金額"].sum()
    total_boxoffice_df_dict[year] = total_boxoffice
    
    #
    boxoffice_by_country = df.groupby("國別地區")["銷售金額"].sum().reset_index()
    boxoffice_by_country.columns = ['國家', '總票房']
    boxoffice_by_country['年份'] = year
    boxoffice_by_country_df_dict[year] = boxoffice_by_country
    #csv_filename = ("%s country boxoffice.csv" %year)
    #boxoffice_by_country.to_csv(csv_filename,encoding ="utf-8-sig")
    
    #
    boxoffice_by_titles = df.groupby("中文片名")["銷售金額"].sum().reset_index()
    boxoffice_by_titles.columns = ['片名', '總票房']
    boxoffice_by_titles['年份'] = year
    boxoffice_by_titles_df_dict[year] = boxoffice_by_titles
    #csv_filename = ("%s title boxoffice.csv" %year)
    #boxoffice_by_titles.to_csv(csv_filename,encoding ="utf-8-sig")
    

year = ["2018","2019","2020","2021","2022","2023","2024"]
average_boxoffice_dict = {}

for y in year:
    average_boxoffice = total_boxoffice_df_dict[y] / movie_onscreen_df_dict[y]
    average_boxoffice_dict[y] = round(average_boxoffice,3)


average_boxoffice_df = pd.DataFrame(list(average_boxoffice_dict.items()),columns=["年份","平均票房"])
average_boxoffice_df.to_csv("2018~2024 average boxoffice.csv",encoding ="utf-8-sig")
   
#每年的總售票數和每年的總票房轉成Dataframe     
total_boxoffice_df = pd.DataFrame(list(total_boxoffice_df_dict.items()),columns=["年份","總票房"])
total_tickets_df = pd.DataFrame(list(total_tickets_df_dict.items()),columns=["年份","總售票數"])

#合併成新的Dataframe 
total_sales_df = pd.concat([total_tickets_df,total_boxoffice_df.iloc[:,1]],axis=1, ignore_index=True)
total_sales_df.columns = ["年份","總售票數","總票房"]
#total_sales_df.to_csv("2018~2024 total sales.csv",encoding ="utf-8-sig")

movie_onscreen_df = pd.DataFrame(list(movie_onscreen_df_dict.items()),columns=["年份","電影上映數"])
new_movie_df = pd.DataFrame(list(new_movie_df_dict.items()),columns=["年份","新片上映數"]) 

total_movie_onscreen_df = pd.concat([movie_onscreen_df,new_movie_df.iloc[:,1]],axis=1,ignore_index=True)
total_movie_onscreen_df.columns = ["年份","電影上映數","新片上映數"]
#total_movie_onscreen_df.to_csv("2018~2024 total movie onscreeen.csv",encoding ="utf-8-sig")

    