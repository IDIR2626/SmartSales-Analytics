import pandas as pd

df = pd.read_excel('data/Online Retail.xlsx', sheet_name='Online Retail')
print(df.head())