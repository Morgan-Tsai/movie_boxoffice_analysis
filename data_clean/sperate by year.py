import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect("Movie.db")
print("Connect to database succesfully")

cur = conn.cursor()

other_path = r"C:\Users\user\Desktop\Python movie data\csv_output\TWmovie_combined_data.csv"
new_data_path = r"C:\Users\user\Desktop\Python movie data\source\2024年07月15日至2024年07月21日全國電影票房統計數據.csv"
new_data2_path = r"C:\Users\user\Desktop\Python movie data\source\2024年07月22日至2024年07月28日全國電影票房統計數據.csv"

other = pd.read_csv(other_path,encoding="utf-8-sig")
new_data = pd.read_csv(new_data_path,encoding="utf-8-sig")
new_data2 = pd.read_csv(new_data2_path,encoding="utf-8-sig")

#去除全是nan的col
other2 = other.dropna(axis=0,how="all")


#在全是nan中的有效數據
non_nan_in_column_A = other2[other2["累計金額"].notna()]
non_nan_in_column_B = other2[other2["累計票數"].notna()]

#顯示有效數據的row
#print(non_nan_in_column_B)
#print(non_nan_in_column_A)

#修改前的row(全是nan)
#print(other2.iloc[4625:4678,9])
#print(other2.iloc[4625:4677,10])

#替換原本是nan的數據，數據位置偏移
other2.iloc[4625:4677,9] = other2.iloc[4625:4677,14]
other2.iloc[4625:4677,10] = other2.iloc[4625:4677,15]

#修改後的row
#print(other2.iloc[4625:4677,9])
#print(other2.iloc[4625:4677,10])

#找col中nan的位置
nan_in_column_A = other2['國別地區'].isna()
# 使用 np.where() 找到 NaN 值的位置索引
nan_indices_in_column_A = np.where(nan_in_column_A)[0] #取出row
other2.iloc[list(nan_indices_in_column_A),1] = ["巴基斯坦","希臘","希臘","澳洲","摩洛哥","葉門"]

other2.iloc[23840:23938,8] = other2.iloc[23840:23938,17]

#挑出所需的資料
boxoffice_df = other2.iloc[:,0:11]
#加入最新票房資料
total_boxoffice_df = pd.concat([boxoffice_df,new_data,new_data2],ignore_index=True)

#total_boxoffice_df.to_csv("clean boxoffice.csv",encoding="utf-8-sig",index=False)

total_boxoffice_df["銷售金額"] = total_boxoffice_df["銷售金額"].str.replace(",","").astype(float)
# total_boxoffice_df["銷售票數"] = total_boxoffice_df["銷售票數"].str.replace(",","").astype(float)
total_boxoffice_df["累計銷售票數"] = total_boxoffice_df["累計銷售票數"].str.replace(",","").astype(float)
total_boxoffice_df["累計銷售金額"] = total_boxoffice_df["累計銷售金額"].str.replace(",","").astype(float)

list1 = []

boxoffice_2019 = total_boxoffice_df.iloc[2111:6766,1:]
list1.append(boxoffice_2019)
#print(boxoffice_2019.info())
boxoffice_2020 = total_boxoffice_df.iloc[6766:12615,1:]
list1.append(boxoffice_2020)
#print(boxoffice_2020.info())
boxoffice_2021 = total_boxoffice_df.iloc[12615:16508,1:]
list1.append(boxoffice_2021)
#print(boxoffice_2021.info())
boxoffice_2022 = total_boxoffice_df.iloc[16508:21370,1:]
list1.append(boxoffice_2022)
#print(boxoffice_2022.info())
boxoffice_2023 = total_boxoffice_df.iloc[21370:26359,1:]
list1.append(boxoffice_2023)
#print(boxoffice_2023.info())
boxoffice_2024 = total_boxoffice_df.iloc[26359:,1:]
list1.append(boxoffice_2024)
#print(boxoffice_2024.info())

# boxoffice_2019.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2019 boxoffice.csv",encoding="utf-8-sig",index=False)
# boxoffice_2020.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2020 boxoffice.csv",encoding="utf-8-sig",index=False)
# boxoffice_2021.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2021 boxoffice.csv",encoding="utf-8-sig",index=False)
# boxoffice_2022.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2022 boxoffice.csv",encoding="utf-8-sig",index=False)
# boxoffice_2023.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2023 boxoffice.csv",encoding="utf-8-sig",index=False)
#boxoffice_2024.to_csv(r"C:\Users\user\Desktop\python專題\csv\data source\2024 boxoffice.csv",encoding="utf-8-sig",index=False)

list2 = []

for df in list1:
    #print(df.info())
    df["銷售票數"] = df["銷售票數"].str.replace(",","").astype(int)
    df["銷售金額"] = df["銷售金額"].astype(int)
    df["上映日期"] = pd.to_datetime(df["上映日期"],errors='coerce')
    df["中文片名"] = df["中文片名"].str.replace("'","")
    # df['上映日期'] = df['上映日期'].where(df['上映日期'].notna(), None)
    country = df['國別地區']
    title = df["中文片名"]
    date = df["上映日期"].dt.date
    ticket = df["銷售票數"]
    boxoffice = df["銷售金額"]
    
    new_df = pd.DataFrame({
        "國家": country,
        "中文片名": title,
        "上映日期": date,
        "銷售票數": ticket,
        "銷售金額": boxoffice
    })
    
    list2.append(new_df)
    

    
for year in range(2019,2025):
    table_name = f"boxoffice_{year}"
    sqlstr1 = ("""
                 CREATE TABLE IF NOT EXISTS %s
                 (country TEXT,
                  title TEXT,
                  onscreen_date DATE,
                  ticket_sale INT,
                  boxoffice_sale INT);""") %table_name
    
    cur.execute(sqlstr1)
    
print("Create table successfully")    

for year, df in zip(range(2019, 2025), list2):
    table_name = f"boxoffice_{year}"
    for _,row in df.iterrows():
        sqlstr2 = ("""INSERT INTO {}(country,title,onscreen_date,ticket_sale,boxoffice_sale) 
                    VALUES ('{}','{}','{}',{},{})""")
        sqlstr2 = sqlstr2.format(table_name,row["國家"],row["中文片名"],row["上映日期"],row["銷售票數"],row["銷售金額"])
        cur.execute(sqlstr2)

conn.commit()
print("Insert data successfully")
conn.close()
print("Connect of database has closed")


