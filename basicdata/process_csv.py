import pandas as pd

df=pd.read_csv("../dataset/SalesTransactions/SalesTransactions.csv",
               sep=',',encoding='utf-8',low_memory=False)
# da phan la \t
print(df)