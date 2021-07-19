import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import model_selection

df = pd.read_csv("D:\Capegemini Hacathon\modcloth.csv")
sales_df = df.drop(columns=['fit','size','user_attr','brand'],axis=1)
sales_df = sales_df[sales_df['user_id'] != ' '].dropna(subset=['user_id'])
sales_df['category'] = sales_df['category'].str.upper()
sales_df['timestamp'] = pd.to_datetime(sales_df['timestamp'],dayfirst=True)
sales_df.to_csv('Sales-Transactions-Edited.csv',index=False)
print(sales_df.isnull().sum())
