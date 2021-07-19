import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Import Feature Engineered Sales Transaction file
sales_df = pd.read_csv('Sales-Transactions-Edited.csv')
top_sell_items_df = sales_df.groupby('item_id').agg({'rating':'max'})

# Reset the index by converting the Product into a column
top_sell_items_df.reset_index(inplace=True)
top_sell_items_df['Top_Sell_Rank'] = top_sell_items_df['rating'].rank(method='min',ascending=False).astype(int)
#print(top_sell_items_df.sort_values('rating',ascending=False).head(20))
unique_order_items_df = sales_df.drop_duplicates(['item_id','timestamp','category'])
most_popular_items_df = unique_order_items_df.groupby('item_id').agg({'timestamp':'count', 'category':'nunique'})
most_popular_items_df.columns=['No_of_Orders','No_of_Customers']
#print(most_popular_items_df.head())
most_popular_items_df.reset_index(inplace=True)
O = most_popular_items_df['No_of_Orders']
C = most_popular_items_df['No_of_Customers']
M = most_popular_items_df['No_of_Customers'].max()
most_popular_items_df['Weighted_No_of_Orders'] = O * (C / M)
most_popular_items_df['Popularity_Rank'] = most_popular_items_df['Weighted_No_of_Orders'].rank(method='min',ascending=False).astype(int)
#print(most_popular_items_df.sort_values('Popularity_Rank',ascending=True).head(20))

product_rankings_df = pd.merge(top_sell_items_df,most_popular_items_df,how='inner',on='item_id')
product_rankings_df = product_rankings_df[['item_id','rating','Top_Sell_Rank','Popularity_Rank']]
print(product_rankings_df.sort_values('Popularity_Rank',ascending=True).head(20))

#product_rankings_df.to_csv('Product-Rankings.csv',index=False)
#pickle.dump(product_rankings_df, open('prod_ranking_model.pkl','wb'))