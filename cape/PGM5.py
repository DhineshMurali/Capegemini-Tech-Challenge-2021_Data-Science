import pandas as pd
import pickle

# Import Feature Engineered Sales Transaction file
sales_df = pd.read_csv('Sales-Transactions-Edited.csv')

prod_cust_qty_df = sales_df.groupby(['item_id','category']).agg({'rating':'sum'})

# Reset the index by converting the Party and Product into columns
prod_cust_qty_df.reset_index(inplace=True)


# Find the no of unique customers purchased each product
prod_cust_count_df = sales_df.groupby(['item_id']).agg({'category':'nunique'})

# Set the customer count column
prod_cust_count_df.columns=['No_of_Customers']

# Reset the index by converting the Party and Product into columns
prod_cust_count_df.reset_index(inplace=True)


# Merge the unique customer count and qty purchased of each product
prod_cust_df = pd.merge(prod_cust_qty_df,prod_cust_count_df,how='inner',on='item_id')

prod_cust_pivot_df = prod_cust_df.pivot(index='category',columns='item_id',values='rating').fillna(0)
prod_correlation_df = prod_cust_pivot_df.corr(method='pearson',min_periods=5)

prod_correlation_df.to_csv('Product-Product-Correlation-Matrix.csv')
pickle.dump(prod_correlation_df, open('prod_correlation_model.pkl','wb'))