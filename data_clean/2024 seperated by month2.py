import pandas as pd
import sqlite3

file_path = r"C:\Users\user\Desktop\Python movie data\csv_output\2018~2024 boxoffice\yearly boxoffice\2024 boxoffice.csv"

data = pd.read_csv(file_path,encoding="utf-8-sig")

#轉成數值型態
data["銷售票數"] = data["銷售票數"].str.replace(",","").astype(int)
data["上映日期"] = pd.to_datetime(data["上映日期"])
#print(data.info())

#按月份拆分數據
months = {
    'january': data.iloc[:524, :],
    'february': data.iloc[524:908, :],
    #'march': data.iloc[908:1295, :],
    'march': data.iloc[908:1303, :],
    #'april': data.iloc[1295:1749, :],
    'april': data.iloc[1303:1749, :],
    #'may': data.iloc[1749:2124, :],
    'may': data.iloc[1749:2132, :],
    #'june': data.iloc[2124:2493, :],
    'june': data.iloc[2132:2503, :],
    #'july': data.iloc[2493:, :]
    'july': data.iloc[2503:, :]
}

jan_df = months['january'].reset_index(drop=True)
feb_df = months['february'].reset_index(drop=True)
mar_df = months['march'].reset_index(drop=True)
apr_df = months['april'].reset_index(drop=True)
m_df = months['may'].reset_index(drop=True)
jun_df = months['june'].reset_index(drop=True)
jul_df = months['july'].reset_index(drop=True)


#feb_df的第5列移到jan_df，並從feb_df刪除
jan_new = pd.DataFrame([feb_df.iloc[4, :]], columns=jan_df.columns)
jan_df2 = pd.concat([jan_df,jan_new],axis=0,ignore_index=True)
feb_df2 = feb_df.drop(4,axis=0).reset_index(drop=True)

#mar_df的第3、14列移到feb_df，並從mar_df刪除
feb_new1 = pd.DataFrame([mar_df.iloc[3, :]], columns=feb_df.columns)
feb_new2 = pd.DataFrame([mar_df.iloc[14, :]], columns=feb_df.columns)
feb_df3 = pd.concat([feb_df2,feb_new1,feb_new2],axis=0,ignore_index=True)
mar_df2 = mar_df.drop([3,14],axis=0).reset_index(drop=True)

#apr_df的第8列移到mar_df，並從apr_df刪除
mar_new = pd.DataFrame([apr_df.iloc[8, :]], columns=mar_df.columns)
mar_df3 = pd.concat([mar_df2,mar_new],axis=0,ignore_index=True)
apr_df2 = apr_df.drop(8,axis=0).reset_index(drop=True)

#m_df的第4列移到apr_df，並從m_df刪除
apr_new = pd.DataFrame([m_df.iloc[4, :]], columns=apr_df.columns)
apr_df3 = pd.concat([apr_df2,apr_new],axis=0,ignore_index=True)
m_df2 = m_df.drop(4,axis=0).reset_index(drop=True)

months2 = {
    'january': jan_df2,
    'february': feb_df3,
    'march': mar_df3,
    'april': apr_df3,
    'may': m_df2,
    'june': jun_df,
    'july': jul_df
}



#確認每月份的資料數量
# for mon in months:
#     print(months[mon].info())

#空字典
boxoffice_df_dict = {}

#迴圈找出每月重複的片名，並取最後一筆
for month,df in months2.items():
    final_df = df.drop_duplicates(subset=["中文片名"], keep="last").reset_index()
    boxoffice_df_dict[month] = final_df
    #csv_filename = ("2024 %s boxoffice.csv" %month)
    #final_df.to_csv(csv_filename,encoding ="utf-8-sig")
    

#找出產國家的重複次數
country_df_dict = {}

for month,df in boxoffice_df_dict.items():
    duplicate_country1 = df["國別地區"].value_counts()
    duplicate_country2 = duplicate_country1.reset_index()
    duplicate_country2.columns = ["產地","重複次數"]
    country_df_dict[month] = duplicate_country2
    #csv_filename = ("2024 %s country count.csv" %month)
    #duplicate_country2.to_csv(csv_filename,encoding ="utf-8-sig")

total_boxoffice_df_dict = {}

for month,df in months2.items():
    total_boxoffice = df["銷售金額"].sum()
    total_boxoffice_df_dict[month] = total_boxoffice


total_boxoffice_df = pd.DataFrame(list(total_boxoffice_df_dict.items()),columns=["月份","總票房"])

total_tickets_df_dict = {}

for month,df in months2.items():
    total_tickets = df["銷售票數"].sum()
    total_tickets_df_dict[month] = total_tickets
    
total_tickets_df = pd.DataFrame(list(total_tickets_df_dict.items()),columns=["月份","總售票數"])

total_sales_df = pd.concat([total_boxoffice_df,total_tickets_df.iloc[:,1]],axis=1, ignore_index=True)
total_sales_df.columns = ["月份","總票房","總售票數"]
#total_sales_df.to_csv("2024 total sales2.csv",encoding ="utf-8-sig")
#total_sales_df.to_csv("2024 total sales.csv",encoding ="utf-8-sig")

movie_onscreen_df_dict={}
new_movie_df_dict={} 
new_movie_df2_dict={}

for month,df in boxoffice_df_dict.items():
    movie_onscreen = len(df)
    movie_onscreen_df_dict[month] = movie_onscreen

movie_onscreen_df = pd.DataFrame(list(movie_onscreen_df_dict.items()),columns=["月份","電影上映數"])

month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july']
month_numbers = [1, 2, 3, 4, 5, 6, 7]

for month_name, month_number in zip(month_names, month_numbers):
    new_movie_df2_dict[month_name] = boxoffice_df_dict[month_name][
        (boxoffice_df_dict[month_name]["上映日期"].dt.year == 2024) & 
        (boxoffice_df_dict[month_name]["上映日期"].dt.month == month_number)
    ]
    
    new_movie_df_dict[month_name] = len(boxoffice_df_dict[month_name][
        (boxoffice_df_dict[month_name]["上映日期"].dt.year == 2024) & 
        (boxoffice_df_dict[month_name]["上映日期"].dt.month == month_number)
    ])


new_movie_df = pd.DataFrame(list(new_movie_df_dict.items()),columns=["月份","新片上映數"])
    
total_movie_onscreen_df = pd.concat([movie_onscreen_df,new_movie_df.iloc[:,1]],axis=1,ignore_index=True)
total_movie_onscreen_df.columns = ["月份","電影上映數","新片上映數"]
#total_movie_onscreen_df.to_csv("2024 total movie onscreeen.csv",encoding ="utf-8-sig")

averge_boxoffice_df_dict={}
boxoffice_by_country_df_dict={}
boxoffice_by_title_df_dict={}

for month in month_names:
    averge_boxoffice = total_boxoffice_df_dict[month] / movie_onscreen_df_dict[month]
    averge_boxoffice_df_dict[month] = round(averge_boxoffice,3)
    
averge_boxoffice_df= pd.DataFrame(list(averge_boxoffice_df_dict.items()),columns=["月份","平均票房"]) 
averge_boxoffice_df.to_csv("2024 averge boxoffice.csv",encoding ="utf-8-sig")
  
for month,df in months2.items():
    boxoffice_by_country = df.groupby("國別地區")["銷售金額"].sum().reset_index()
    boxoffice_by_country.columns = ['國家', '總票房']
    boxoffice_by_country['月份'] = month
    boxoffice_by_country_df_dict[month] = boxoffice_by_country
    #csv_filename = ("2024 %s country boxoffice.csv" %month)
    #boxoffice_by_country.to_csv(csv_filename,encoding ="utf-8-sig")
    
    boxoffice_by_title = df.groupby("中文片名")["銷售金額"].sum().reset_index()
    boxoffice_by_title.columns = ['片名', '總票房']
    boxoffice_by_title['月份'] = month
    boxoffice_by_title_df_dict[month] =  boxoffice_by_title
    #csv_filename = ("2024 %s title boxoffice.csv" %month)
    #boxoffice_by_title.to_csv(csv_filename,encoding ="utf-8-sig")
    
conn = sqlite3.connect("Movie.db")
print("Connect to database succesfully")

for month,df in months2.items():
    df["上映日期"] = df["上映日期"].dt.date
    
    new_df = pd.DataFrame({
                            "國家": df["國別地區"],
                            "中文片名": df["中文片名"],
                            "上映日期": df["上映日期"],
                            "銷售票數": df["銷售票數"],
                            "銷售金額": df["銷售金額"]
                            })
    
    table_name = ("%s_2024boxoffice") %str(month)
    
    sqlstr1 = ("""
                 CREATE TABLE IF NOT EXISTS %s
                 (country TEXT,
                  title TEXT,
                  onscreen_date DATE,
                  ticket_sale INT,
                  boxoffice_sale INT);""") %table_name
    
    conn.execute(sqlstr1)
    
    new_df.to_sql(table_name,conn,if_exists="replace",index=False)
    
    conn.commit()
    print("Insert data successfully")

conn.close()
print("Connect of database has closed")
   

    