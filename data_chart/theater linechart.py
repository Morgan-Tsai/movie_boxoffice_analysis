import pdfplumber
import pandas as pd
from matplotlib import pyplot as plt

file_positon = r"C:\Users\user\Desktop\python專題\csv\data source\23電影映演業家數.pdf"

with pdfplumber.open(file_positon) as pdf:
    first_page = pdf.pages[0]
    table = first_page.extract_table()
        
    if table:
        df = pd.DataFrame(table[1:], columns=table[0])
    
    # df["年別"] = df["年別"].astype(int)
    df["家數"] = df["家數"].astype(int)
    
    plt.rcParams["font.family"] = "Microsoft JhengHei"
    
    plt.figure(figsize=(10, 5))
    
    plt.plot(df["年別"],df["家數"],marker="o",lw=4,markersize=11,c="#39B5DB")
    
    
    plt.ylim(100,130)
    plt.grid(axis="y")
    plt.ylabel("電影院數量(家)",fontsize=14)
    plt.title("2010年~2023年電影院數量變化",fontsize=21)
    
    plt.savefig("2010~2023 theater.png")
    
    plt.show()
    
    