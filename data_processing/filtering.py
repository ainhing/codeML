from numpy import nan as NA
import pandas as pd
data = pd.DataFrame([[1.,6.5,3.],
                     [1.,NA,NA],
                     [NA,NA,NA],
                     [NA,8.,3.]])
print(data)
print("-"*10)
cleaned=data.dropna()
print(cleaned)
print("-"*10)
cleaned2=data.dropna(how='all')
print(cleaned2)