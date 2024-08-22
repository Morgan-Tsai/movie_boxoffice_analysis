import sqlite3
import pandas as pd

conn = sqlite3.connect("Movie.db")
print("Connect to database succesfully")

cur = conn.cursor()

file_path = r"C:\Users\user\Desktop\Python movie data\csv_output\2018~2024 boxoffice\yearly boxoffice\2018 movie boxoffice.csv"

data = pd.read_csv(file_path,encoding="utf-8-sig")

data["上映日期"] = data["上映日期"].str.split(' ').str[0]
data["上映日期"] = pd.to_datetime(data["上映日期"])
data["上映日期"] = data["上映日期"].dt.date
data["銷售票數"] = data["銷售票數"].str.replace(",","")
data["銷售金額"] = data["銷售金額"].str.replace(",","")
data["銷售票數"] = data["銷售票數"].fillna(0).astype(int)
data["銷售金額"] = data["銷售金額"].fillna(0).astype(int)

sqlstr1 = """
             CREATE TABLE IF NOT EXISTS boxoffice_2018
             (country TEXT,
              title TEXT,
              onscreen_date DATE,
              ticket_sale INT,
              boxoffice_sale INT);"""

cur.execute(sqlstr1)

new_df = pd.DataFrame({
                        "國家": data["國別地區"],
                        "中文片名": data["中文片名"],
                        "上映日期": data["上映日期"],
                        "銷售票數": data["銷售票數"],
                        "銷售金額": data["銷售金額"]
                        })

#new_df.to_sql("boxoffice_2018",conn,if_exists="replace",index=False)

conn.commit()
print("Insert data successfully")

sql_select = """
            SELECT `國家`,`中文片名`,SUM(`銷售金額`) AS "總票房"
            FROM `boxoffice_2018`
            GROUP BY `中文片名`
            HAVING `國家` = "中華民國"
            ORDER BY SUM(`銷售金額`) DESC;
            """

TW_boxoffice_ranking = pd.read_sql(sql_select, conn)

print(TW_boxoffice_ranking.head(5))

conn.close()
print("Connect of database has closed")
