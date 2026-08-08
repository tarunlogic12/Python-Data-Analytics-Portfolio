 

# Retail Sales Data Analysis: Real-World Insights
"""
# =============================================================================
# 🏢 ADVANCED PANDAS ENTERPRISE ANALYTICS & DATA WRANGLING PIPELINE
# 04: Advanced Grouping, Reshaping, Multi-Indexing & Pivot Analytics
# Lead Analyst: Tarun Das | Data Analytics & Generative AI Pro
# GitHub Profile: https://github.com/tarunlogic12
# =============================================================================

import pandas as pd
import numpy as np

# Ingest the dataset globally so 'df' is accessible to all cells
file_path = '/content/Advanced_pandas_sales_dataset.csv'
try:
    df = pd.read_csv(file_path)
    print(f"✓ Ingested Dataset '{file_path}': {df.shape[0]} Rows × {df.shape[1]} Columns.")
except FileNotFoundError:
    print(f"❌ Error: Dataset '{file_path}' not found in working directory.")

# Ensure Order_Date is datetime for time-series analysis for all subsequent cells
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
print("✓ 'Order_Date' column converted to datetime format for global df.")
print(df['Order_Date'].head())                                                                                                                                                                                                                              

# ----------------------------------------------------------------------------
# 2. 04 ASSIGNMENT PIPELINE (Q1 - Q10)
# -----------------------------------------------------------------------------


def run_advanced_pandas_pipeline():
    print("=" * 80)
    print("🐼 MODULE 04: ADVANCED PANDAS ANALYTICS & DATA WRANGLING PIPELINE")
    print("=" * 80)

    # The DataFrame 'df' is now expected to be loaded globally before this function is called.
    # Q1: Exploration
    # 🎯 BUSINESS USE-CASE: Ingesting & inspecting schema datatypes.
    # 🧠 MEMORY TRICK: head(10), info(), shape, dtypes.
    print("[STAGE 1/10] Q1: DATASET EXPLORATION")
    print("--- First 10 Rows ---")
    print(df.head(10).to_string(index=False))
    print("\n--- Schema Audit ---")
    df.info()

    # Q2: Filtering
    # 🎯 BUSINESS USE-CASE: High-value order identification.
    # 🧠 MEMORY TRICK: df[(df['Region'] == 'East') & (df['Sales'] > 2500)]
    print("\n[STAGE 2/10] Q2: SALES FILTERING ANALYSIS")
    sales_3500 = df[df['Sales'] > 3500]
    # Corrected sales threshold for East region to > 2500 as per assignment
    east_sales_2500 = df[(df['Region'] == 'East') & (df['Sales'] > 2500)]
    print(f"1. Orders Sales > 3500: {len(sales_3500)} records found (Max sale is ₹{df['Sales'].max():,.2f}).")
    print(f"2. East Region & Sales > 2500: {len(east_sales_2500)} records found.") # Corrected variable name
    print(east_sales_2500.to_string(index=False))

    # Q3: Top 5 Customers
    # 🎯 BUSINESS USE-CASE: Key Account Management (KAM).
    # 🧠 MEMORY TRICK: groupby('Customer')['Sales'].sum().nlargest(5)
    print("\n[STAGE 3/10] Q3: CUSTOMER PURCHASE ANALYSIS (TOP 5 CUSTOMERS)")
    top_5 = df.groupby('Customer')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(5)
    print(top_5.to_string(index=False))

    # Q4: Regional Sales
    # 🎯 BUSINESS USE-CASE: Regional market dominance.
    # 🧠 MEMORY TRICK: groupby('Region')['Sales'].sum()
    print("\n[STAGE 4/10] Q4: REGIONAL SALES PERFORMANCE")
    reg_sales = df.groupby('Region')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
    print(reg_sales.to_string(index=False))
    print(f"🏆 Highest Revenue Region: {reg_sales.iloc[0]['Region']} (₹{reg_sales.iloc[0]['Sales']:,.2f})")
    print(f"📉 Lowest Revenue Region: {reg_sales.iloc[-1]['Region']} (₹{reg_sales.iloc[-1]['Sales']:,.2f})")

    # Q5: Product Quantity Performance
    # 🎯 BUSINESS USE-CASE: Inventory volume forecasting.
    # 🧠 MEMORY TRICK: groupby('Product')['Sales'].sum() # Changed from Quantity to Sales
    print("\n[STAGE 5/10] Q5: PRODUCT PERFORMANCE ANALYSIS")
    # Assignment asks for total sales by each product, not quantity
    prod_sales = df.groupby('Product')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
    print(prod_sales.to_string(index=False))
    print(f"🔥 Most Popular Product (by Sales): {prod_sales.iloc[0]['Product']} (₹{prod_sales.iloc[0]['Sales']:,.2f})")

    # Q6: Multi-Level Grouping
    # 🎯 BUSINESS USE-CASE: Region & Category sales matrix.
    # 🧠 MEMORY TRICK: groupby(['Region', 'Category'])['Sales'].sum()
    print("\n[STAGE 6/10] Q6: MULTI-LEVEL GROUPING (REGION & CATEGORY)")
    # Assignment asks to group by Region and Category
    multi_group_cat = df.groupby(['Region', 'Category'])['Sales'].sum().reset_index()
    print(multi_group_cat.to_string(index=False))
    print("\nInsights: This analysis shows sales distribution across different product categories within each region, highlighting which categories perform better in specific regions.")

    # Q7: Pivot Table Creation
    # 🎯 BUSINESS USE-CASE: Executive cross-tabulation dashboard.
    # 🧠 MEMORY TRICK: df.pivot_table(index='Region', columns='Product', values='Sales', aggfunc='sum')
    print("\n[STAGE 7/10] Q7: PIVOT TABLE CREATION")
    pivot_q7 = df.pivot_table(index='Region', columns='Product', values='Sales', aggfunc='sum', fill_value=0)
    print(pivot_q7.to_string())
    # Check if 'Laptop' column exists before accessing
    if 'Laptop' in pivot_q7.columns:
        print(f"\n💻 Region with Highest Laptop Sales: {pivot_q7['Laptop'].idxmax()} (₹{pivot_q7['Laptop'].max():,.2f})")
    else:
        print("\nLaptop product not found in the pivot table for sales analysis.")

    # Q8: Profitability Analysis
    # 🎯 BUSINESS USE-CASE: Unit realization assessment.
    # 🧠 MEMORY TRICK: Calculate average profit for each product category.
    print("\n[STAGE 8/10] Q8: PROFITABILITY ANALYSIS")
    # Based on df.info(), a 'Profit' column is available.
    avg_profit_cat = df.groupby('Category')['Profit'].mean().reset_index().sort_values(by='Profit', ascending=False)
    print(avg_profit_cat.round(2).to_string(index=False))
    print(f"\n📈 Most Profitable Category (by Avg Profit): {avg_profit_cat.iloc[0]['Category']} (₹{avg_profit_cat.iloc[0]['Profit']:.2f})")

    # Q9: Discount Impact Study
    # 🎯 BUSINESS USE-CASE: Analyze the relationship between discount and profit.
    # 🧠 MEMORY TRICK: Group by 'Discount' and calculate average 'Profit'.
    print("\n[STAGE 9/10] Q9: DISCOUNT IMPACT STUDY")
    # Based on df.info(), 'Discount' and 'Profit' columns are available.
    # Discretize discount to analyze impact of discount levels
    # Using pd.cut to create bins for discount levels, as pd.qcut might create uneven ranges for sparse discount values

    # If discount values are few and distinct, grouping directly is fine:
    discount_impact = df.groupby('Discount')['Profit'].mean().reset_index().sort_values(by='Discount', ascending=True)
    print(discount_impact.round(2).to_string(index=False))

    print("\nInsights: This analysis shows the average profit at different discount levels. Observe if increasing discounts lead to a decrease in average profit, indicating a negative relationship.")
    if discount_impact['Profit'].is_monotonic_decreasing:
        print("   Observation: Higher discounts consistently lead to lower average profit.")
    elif discount_impact['Profit'].is_monotonic_increasing:
        print("   Observation: Higher discounts consistently lead to higher average profit.")
    else:
        print("   Observation: The relationship between discount and average profit is not consistently monotonic.")

    # Q10: End-to-End Data Wrangling Task
    # 🎯 BUSINESS USE-CASE: ETL Filter -> Group -> Pivot Pipeline.
    # 🧠 MEMORY TRICK: Filter > Groupby > Pivot.
    print("\n[STAGE 10/10] Q10: END-TO-END DATA WRANGLING WORKFLOW")
    # Corrected filter for Sales > 3000 as per assignment
    filtered_df = df[df['Sales'] > 3000]
    grouped_df = filtered_df.groupby(['Region', 'Product'])['Sales'].sum().reset_index()
    pivot_q10 = grouped_df.pivot(index='Region', columns='Product', values='Sales').fillna(0)
    print(f"Reshaped Pivot Table for High-Ticket Orders (> ₹3000):\n{pivot_q10.to_string()}")
    print("\nBusiness Insights: This pivot table provides a clear view of high-value product sales across different regions, allowing identification of key products and regions contributing most to high-ticket revenue.")

    print("\n" + "=" * 80)
    print("✅ ADVANCED PANDAS PIPELINE EXECUTION COMPLETE | READY FOR SUBMISSION")
    print("=" * 80)

if __name__ == '__main__':
    run_advanced_pandas_pipeline()

"""## Real-World Business Insights & Advanced Analytics

To further demonstrate a comprehensive analytical approach, beyond the assignment questions, we will explore key real-world business insights. These analyses focus on aspects critical for strategic decision-making and operational improvements.

### 1. Monthly Sales Trend Analysis

🎯 **BUSINESS USE-CASE**: Understand if sales are growing, shrinking, or changing with seasons, helping with future planning and budgeting.
🧠 **MEMORY TRICK**: Group by 'Order_Date' (set as index), then `resample('M')` to get monthly sums of 'Sales'.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Aggregate sales by month
monthly_sales = df.set_index('Order_Date').resample('M')['Sales'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Order_Date'].dt.strftime('%Y-%m')

plt.figure(figsize=(12, 6))
sns.lineplot(x='Month', y='Sales', data=monthly_sales, marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales (₹)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nInsights: This plot visually represents the sales performance over time, helping to identify peaks, troughs, and overall growth patterns.")

"""### 2. Customer Value Metrics: Average Order Value (AOV) & Purchase Frequency

🎯 **BUSINESS USE-CASE**: Find your best customers (those who spend a lot or buy often) to give them special attention or tailor offers.
🧠 **MEMORY TRICK**: `groupby('Customer')` to get `Total_Sales` (sum) and `Number_of_Orders` (count unique orders).
"""

# Calculate total sales and number of orders per customer
customer_summary = df.groupby('Customer').agg(
    Total_Sales=('Sales', 'sum'),
    Number_of_Orders=('Order_ID', 'nunique')
).reset_index()

# Calculate Average Order Value (AOV) and Purchase Frequency
customer_summary['Average_Order_Value'] = customer_summary['Total_Sales'] / customer_summary['Number_of_Orders']
customer_summary['Purchase_Frequency'] = customer_summary['Number_of_Orders'] / len(df['Order_Date'].dt.to_period('M').unique()) # Frequency per month for simplicity

print("Top 10 Customers by Average Order Value:")
print(customer_summary.sort_values(by='Average_Order_Value', ascending=False).head(10).round(2).to_string(index=False))

print("\nTop 10 Customers by Purchase Frequency:")
print(customer_summary.sort_values(by='Purchase_Frequency', ascending=False).head(10).round(2).to_string(index=False))

print("\nInsights: These metrics help in identifying high-value customers (high AOV), loyal customers (high frequency), and understanding different customer segments for targeted marketing.")

"""### 3. Identification of Low-Profit / Loss-Making Products

🎯 **BUSINESS USE-CASE**: Figure out which products are losing money or barely making any, so you can decide whether to fix them, change their price, or stop selling them.
🧠 **MEMORY TRICK**: `groupby('Product')['Profit'].sum()` and `sort_values()` to see the lowest profits.
"""

# Aggregate profit by Product
product_profit = df.groupby('Product')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True)

print("Bottom 10 Products by Total Profit (including loss-making products):")
print(product_profit.head(10).round(2).to_string(index=False))

# Aggregate profit by Category
category_profit = df.groupby('Category')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True)

print("\nCategories by Total Profit (lowest first):")
print(category_profit.round(2).to_string(index=False))

print("\nInsights: Identifying low-profit or loss-making products/categories is crucial. It prompts investigation into pricing strategies, cost structures, supply chain inefficiencies, or potential product discontinuation to improve overall profitability.")

"""### 4. RFM (Recency, Frequency, Monetary) Analysis for Customer Segmentation

🎯 **BUSINESS USE-CASE**: Group customers based on how recently they bought, how often they buy, and how much they spend. This helps target marketing better (e.g., offer a discount to customers who haven't bought recently).
🧠 **MEMORY TRICK**: For each customer, calculate `Recency` (days since last purchase), `Frequency` (how many orders), and `Monetary` (total sales). Then use `pd.qcut()` to score them from 1 to 4.
"""

import datetime as dt

# Define a snapshot date for RFM analysis (one day after the latest order date)
snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

# Calculate R, F, and M for each customer
rfm_df = df.groupby('Customer').agg(
    Recency=('Order_Date', lambda date: (snapshot_date - date.max()).days),
    Frequency=('Order_ID', 'nunique'), # Number of unique orders
    Monetary=('Sales', 'sum')
).reset_index()

# Display RFM scores
print("Customer RFM Scores (Recency, Frequency, Monetary):")
print(rfm_df.head().to_string(index=False))

# Create RFM segments (e.g., using quartiles)
rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 4, labels=[4, 3, 2, 1]) # Lower recency is better (higher score)
rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'], 4, labels=[1, 2, 3, 4]) # Higher frequency is better
rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 4, labels=[1, 2, 3, 4]) # Higher monetary is better

rfm_df['RFM_Score'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)

print("\nTop 5 Customers by RFM Score (High value customers tend to have higher R, F, and M scores):")
# Example of how to interpret RFM scores - '444' would be best customers
print(rfm_df.sort_values(by=['R_Score', 'F_Score', 'M_Score'], ascending=False).head(5).to_string(index=False))

print("\nInsights: RFM analysis helps segment customers into different groups (e.g., 'Champions' (444), 'Loyal Customers' (344), 'At-Risk' (122)). This enables businesses to target specific customer segments with personalized campaigns, improve retention, and increase customer lifetime value.")

"""### 5. Product Co-occurrence (Affinity) Analysis

🎯 **BUSINESS USE-CASE**: Discover which products customers tend to buy together (e.g., bread and butter). Use this for product bundles, suggesting related items, or arranging items in a store.
🧠 **MEMORY TRICK**: `groupby('Order_ID')['Product'].apply(list)` to get products per order, then `itertools.combinations()` to find pairs.
"""

from itertools import combinations

# Group products by Order_ID
products_per_order = df.groupby('Order_ID')['Product'].apply(list)

# Generate all unique pairs of products within each order
pair_counts = {}
for product_list in products_per_order:
    # Ensure products are sorted to count (A, B) and (B, A) as the same pair
    sorted_products = sorted(product_list)
    for p1, p2 in combinations(sorted_products, 2):
        pair = tuple(sorted((p1, p2))) # Ensure consistent order for pairs
        pair_counts[pair] = pair_counts.get(pair, 0) + 1

# Convert to DataFrame for easier sorting and display
product_pairs_df = pd.DataFrame(pair_counts.items(), columns=['Product_Pair', 'Count'])
product_pairs_df = product_pairs_df.sort_values(by='Count', ascending=False).reset_index(drop=True)

print("Top 10 Most Frequent Product Co-occurrences:")
print(product_pairs_df.head(10).to_string(index=False))

print("\nInsights: This analysis reveals which products customers tend to buy together. For example, if 'Mouse' and 'Keyboard' are frequently purchased as a pair, a business could create a 'Desktop Essentials Bundle', offer cross-selling prompts, or place these items closer together in an online store to increase average transaction value.")