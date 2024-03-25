import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your CSV file is named 'sales_data.csv'
df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# Display the first 5 rows of the dataset just to check the structure
print(df.head())

# Check for missing data
print("Missing Data:\n", df.isnull().sum())

# Drop rows with missing values
df_clean = df.dropna()

#Task 1

# Group by 'zip_code' and 'item_number' and calculate the total bottles sold
grouped_data = df_clean.groupby(['zip_code', 'item_number'])['bottles_sold'].sum().reset_index()

# Find the index of the maximum bottles sold in each zip code
max_index = grouped_data.groupby('zip_code')['bottles_sold'].idxmax()

#  Use the index to get the corresponding row in the original DataFrame
most_popular_items = grouped_data.loc[max_index]

# Display the result
print("Most popular item in each zip code:")
print(most_popular_items[['zip_code', 'item_number', 'bottles_sold']])

# Assign unique colors to each item_number
item_colors = sns.color_palette("husl", n_colors=len(most_popular_items['item_number'].unique()))
item_color_dict = dict(zip(most_popular_items['item_number'].unique(), item_colors))

# Scatter plot with different colors for each item_number
plt.subplot(1,2,1)
for item_number, color in item_color_dict.items():
    item_data = most_popular_items[most_popular_items['item_number'] == item_number]
    plt.scatter(item_data['zip_code'], item_data['bottles_sold'],
                label=item_number, alpha=0.7, color=color)

# Annotate the top 5 item numbers
top_5_items = most_popular_items.nlargest(5, 'bottles_sold')
for index, row in top_5_items.iterrows():
    plt.annotate(f' {row["item_number"]}\n',
                 (row['zip_code'], row['bottles_sold']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8, color='red')

plt.title('Bottles Sold')
plt.xlabel('Zip Code')
plt.ylabel('Bottles Sold')

#Task 2

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter data for the timeframe 2016-2019
filtered_df = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2019)]

# Group by store and calculate total bottles sold
total_sales_per_store = filtered_df.groupby('store_name')['bottles_sold'].sum().reset_index()

# Calculate sales percentage per store
total_sales = total_sales_per_store['bottles_sold'].sum()
total_sales_per_store['sales_percentage'] = (total_sales_per_store['bottles_sold'] / total_sales) * 100

# Sort values by sales percentage in descending order
total_sales_per_store = total_sales_per_store.sort_values(by='sales_percentage', ascending=False)

# Take the top 15 stores
top_15_stores = total_sales_per_store.head(15)

# Create a horizontal bar plot for the top 15 stores
plt.subplot(1,2,2)

plt.barh(top_15_stores['store_name'], top_15_stores['sales_percentage'], color='skyblue')
plt.xlabel('%Sales')
plt.ylabel('Store Name')
plt.title('%Sales by store')
plt.grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()

plt.show()