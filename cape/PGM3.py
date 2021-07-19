import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Import Feature Engineered Sales Transaction file
sales_df = pd.read_csv('Sales-Transactions-Edited.csv')
top_sell_cust_items_df = sales_df.groupby(['category','item_id']).agg({'rating':'sum'})

# Reset the index by converting the Party and Product into a column
top_sell_cust_items_df.reset_index(inplace=True)

party_col = top_sell_cust_items_df['category']
qty_col = top_sell_cust_items_df['rating'].astype(str)
top_sell_cust_items_df['Top_Sell_Rank'] = (party_col + qty_col).rank(method='min',ascending=False).astype(int)

#print(top_sell_cust_items_df.sort_values('Top_Sell_Rank',ascending=True).head(20))
unique_order_items_df = sales_df.drop_duplicates(['category','item_id','timestamp'])
freq_items_df = unique_order_items_df.groupby(['category','item_id']).agg({'timestamp':'count'})
freq_items_df.columns=['No_of_Orders']
freq_items_df.reset_index(inplace=True)
#print(freq_items_df.head())

party_col = freq_items_df['category']
ord_count_col = freq_items_df['No_of_Orders'].astype(str)
freq_items_df['Popularity_Rank'] = (party_col + ord_count_col).rank(method='min',ascending=False).astype(int)
#print(freq_items_df.sort_values('Popularity_Rank',ascending=True).head(20))

cust_prod_rankings_df = pd.merge(top_sell_cust_items_df,freq_items_df,how='inner',on=['category','item_id'])
items_price_df = sales_df.groupby(['item_id']).agg({'rating':'max'})
items_price_df.reset_index(inplace=True)

cust_prod_rankings_df = pd.merge(cust_prod_rankings_df,items_price_df,how='left',on='item_id')
cust_prod_rankings_df = cust_prod_rankings_df[['category','item_id','Top_Sell_Rank','No_of_Orders','Popularity_Rank']]
print(cust_prod_rankings_df.sort_values('Popularity_Rank',ascending=True).head(20))

cust_prod_rankings_df.to_csv('Customer-Product-Rankings.csv',index=False)
pickle.dump(cust_prod_rankings_df, open('cust_prod_ranking_model.pkl','wb'))