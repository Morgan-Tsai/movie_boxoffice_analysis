import pdfplumber
import pandas as pd

file_positon = "23電影映演業家數.pdf"

with pdfplumber.open(file_positon) as pdf:
    first_page = pdf.pages[0]
    table = first_page.extract_table()
        
    if table:
        df = pd.DataFrame(table[1:], columns=table[0])
   
        df.to_csv('movie_theater_data.csv', index=False,encoding="utf-8")
        
        
print(df)

