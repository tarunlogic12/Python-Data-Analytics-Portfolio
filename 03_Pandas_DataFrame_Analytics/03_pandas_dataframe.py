 

# 🏢 Enterprise Pandas Data Analysis Pipeline: Retail Sales Performance

## Business Problem Statement:
A retail company wants to gain deeper insights into its sales data to optimize product strategy, marketing efforts, and regional focus. The goal is to identify key trends, understand customer purchasing behavior, and evaluate overall sales performance to inform strategic business decisions.

This pipeline aims to provide a structured approach to data manipulation, indexing, aggregation, and basic visualization, mirroring a typical data analyst's workflow in a business environment.
"""

# =============================================================================
# 🏢 ENTERPRISE PANDAS DATAFRAME ANALYTICS PIPELINE
# Module 03: Core Data Manipulation, Indexing & Aggregation Engine
# Lead Analyst: Tarun Das | Data Analytics & Generative AI
# GitHub: https://github.com/tarunlogic12
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_analytics_pipeline():
    print("=" * 80)
    print("🐼 MODULE 03: ENTERPRISE PANDAS ANALYTICS & QUERY PIPELINE")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Q1: CREATING DATAFRAME FROM PYTHON DICTIONARY
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: In real jobs, when creating custom mock data or testing API responses.
    # 🧠 MEMORY TRICK: Dictionary keys become 'Column Names', values become 'Rows'.
    # 💡 WHAT THIS DOES: Converts raw key-value pairs into a clean tabular structure.
    print("\n[STAGE 1/10] Q1: CREATING A DATAFRAME FROM DICTIONARY")
    print("-" * 60)

    dict_data = {
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
        'Region': ['East', 'West', 'North', 'South', 'East'],
        'Sales': [1200, 25, 75, 300, 50],
        'Quantity': [1, 5, 2, 1, 3]
    }

    df_q1 = pd.DataFrame(dict_data)
    print("✓ Custom Sample DataFrame:")
    print(df_q1.to_string(index=False))

    # -------------------------------------------------------------------------
    # Q2: DATASET INGESTION & QUALITY AUDIT
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: First step in any analytics task—checking dataset size and data types.
    # 🧠 MEMORY TRICK: head() = First 5, tail() = Last 5, info() = Data types & Missing values, shape = Dimensions.
    # 💡 WHAT THIS DOES: Audits the raw transaction history before running calculations.
    print("\n[STAGE 2/10] Q2: DATASET INGESTION & QUALITY AUDIT")
    print("-" * 60)

    file_path = '/content/Retail_dataset.csv'
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Ingested Dataset: {df.shape[0]} Rows \u00d7 {df.shape[1]} Columns.")
    except FileNotFoundError:
        print(f"❌ Error: '{file_path}' not found. Please upload the CSV file.")
        return

    print("\n--- First 5 Rows (head) ---")
    print(df.head().to_string(index=False))

    print("\n--- Last 5 Rows (tail) ---")
    print(df.tail().to_string(index=False))

    print("\n--- Column Data Types & Non-Null Audit (info) ---")
    df.info()

    print(f"\n✓ Total Dataset Dimensions: {df.shape[0]} Rows, {df.shape[1]} Columns")

    # --- Additional Data Cleaning and Preprocessing ---
    print("\n--- Missing Values Audit ---")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0]) # Only show columns with missing values
    if missing_values.sum() == 0:
        print("No missing values found.\n")
    else:
        print("Consider strategies for handling missing values (e.g., imputation, removal).\n")

    print("--- Duplicates Audit ---")
    num_duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {num_duplicates}")
    if num_duplicates > 0:
        df.drop_duplicates(inplace=True)
        print(f"Removed {num_duplicates} duplicate rows. New dataset shape: {df.shape[0]} Rows \u00d7 {df.shape[1]} Columns.\n")
    else:
        print("No duplicate rows found.\n")
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Q3: TARGETED COLUMN SELECTION
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Hiding irrelevant columns (e.g., internal IDs) to focus only on business metrics.
    # 🧠 MEMORY TRICK: Double brackets [[ 'Col1', 'Col2' ]] are required to select multiple columns.
    # 💡 WHAT THIS DOES: Filters table to show only Product, Region, and Sales columns.
    print("\n[STAGE 3/10] Q3: TARGETED COLUMN SELECTION")
    print("-" * 60)

    selected_cols_df = df[['Product', 'Region', 'Sales']]
    print("✓ Filtered View (Product, Region, Sales):")
    print(selected_cols_df.head(5).to_string(index=False))

    # -------------------------------------------------------------------------
    # Q4: LABEL-BASED INDEXING (.loc)
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Looking up a specific order or customer using exact Row ID / Name.
    # 🧠 MEMORY TRICK: .loc Uses LABELS (Row Index ID or Column Header Name).
    # 💡 WHAT THIS DOES: Fetches complete details of Row 10 and exact Sales at Row 20.
    print("\n[STAGE 4/10] Q4: LABEL-BASED INDEXING (.loc)")
    print("-" * 60)

    row_10 = df.loc[10]
    sales_at_20 = df.loc[20, 'Sales']

    print("✓ Full Record at Index 10:")
    print(row_10.to_dict())
    print(f"\n✓ Exact Sales Value at Row Index 20: ₹{sales_at_20:,.2f}")

    # -------------------------------------------------------------------------
    # Q5: POSITIONAL INDEXING (.iloc)
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Slicing data based on numeric positions (e.g., 'give me the top 5 rows and first 4 columns').
    # 🧠 MEMORY TRICK: .iloc Uses NUMERIC POSITIONS (0-based numbers only, like array indices).
    # 💡 WHAT THIS DOES: Cuts out a 6x4 matrix and retrieves the value at row 3 (Index 2).
    print("\n[STAGE 5/10] Q5: POSITIONAL INDEXING (.iloc)")
    print("-" * 60)

    matrix_6x4 = df.iloc[0:6, 0:4]
    sales_3rd_row = df.iloc[2, df.columns.get_loc('Sales')]

    print("✓ First 6 Rows & First 4 Columns Matrix:")
    print(matrix_6x4.to_string(index=False))
    print(f"\n✓ Sales Metric from 3rd Row Position (Index 2): ₹{sales_3rd_row:,.2f}")

    # -------------------------------------------------------------------------
    # Q6: ROW SLICING OPERATIONS
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Pagination on dashboards (showing orders 1-10 on page 1, 15-25 on page 2).
    # 🧠 MEMORY TRICK: df[start:stop] slices rows. Remember 'stop' index is exclusive.
    # 💡 WHAT THIS DOES: Fetches batches of rows for chunked analysis.
    print("\n[STAGE 6/10] Q6: ROW SLICING EXERCISES")
    print("-" * 60)

    first_10_rows = df.head(10)
    rows_15_to_25 = df.iloc[15:26]

    print("✓ First 10 Rows Slice:")
    print(first_10_rows.to_string(index=False))

    print("\n✓ Rows 15 to 25 Slice:")
    print(rows_15_to_25.to_string(index=False))

    # -------------------------------------------------------------------------
    # Q7: SINGLE CONDITION FILTERING
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Isolating regional transactions or identifying high-value customers.
    # 🧠 MEMORY TRICK: df[ df['Column'] == 'Value' ] creates a boolean mask to filter rows.
    # 💡 WHAT THIS DOES: Slices dataset into 'East Region orders' and 'Orders > ₹1500'.
    print("\n[STAGE 7/10] Q7: SINGLE CONDITION LOGICAL FILTERING")
    print("-" * 60)

    east_region_df = df[df['Region'] == 'East']
    sales_above_1500 = df[df['Sales'] > 1500]

    print(f"✓ Total Transactions in 'East' Region: {len(east_region_df)}")
    print(east_region_df.head(5).to_string(index=False))

    print(f"\n✓ Total High-Ticket Orders (Sales > ₹1,500): {len(sales_above_1500)}")
    print(sales_above_1500.head(5).to_string(index=False))

    # -------------------------------------------------------------------------
    # Q8: MULTI-CONDITION BOOLEAN MASKING
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Targeted marketing (e.g., 'Find customers in West region who spent over ₹1200').
    # 🧠 MEMORY TRICK: Use '&' for AND, '|' for OR. Always wrap each condition in parentheses `()`.n# 💡 WHAT THIS DOES: Filters rows that satisfy BOTH regional and sales criteria.
    print("\n[STAGE 8/10] Q8: MULTI-CONDITION BOOLEAN FILTERING")
    print("-" * 60)

    multi_cond_df = df[(df['Region'] == 'West') & (df['Sales'] > 1200)]
    print(f"✓ West Region High-Value Orders (Sales > ₹1,200): {len(multi_cond_df)} Found")
    print(multi_cond_df.to_string(index=False))

    # -------------------------------------------------------------------------
    # Q9: DESCRIPTIVE STATISTICAL PROFILING
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Understanding average spend, identifying pricing anomalies or outliers.
    # 🧠 MEMORY TRICK: describe() gives count, mean, std, min, 25%, 50%, 75%, max instantly.
    # 💡 WHAT THIS DOES: Computes distribution statistics across numerical metrics.
    print("\n[STAGE 9/10] Q9: DESCRIPTIVE STATISTICAL PROFILING")
    print("-" * 60)

    stats_df = df.describe()
    print("✓ Dataset Summary Matrix:")
    print(stats_df.round(2).to_string())

    mean_sales = stats_df.loc['mean', 'Sales']
    max_quantity = stats_df.loc['max', 'Quantity']
    min_sales = stats_df.loc['min', 'Sales']

    print(f"\n✓ Key Takeaway - Mean Sales Value     : ₹{mean_sales:,.2f}")
    print(f"✓ Key Takeaway - Maximum Quantity Sold : {max_quantity:.0f} units")
    print(f"✓ Key Takeaway - Minimum Sales Value   : ₹{min_sales:,.2f}")

    # --- Visualization for Sales Distribution ---
    print("\n--- Sales Distribution (Histogram) ---")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Sales'], kde=True, bins=15, color='skyblue')
    plt.title('Distribution of Sales Values')
    plt.xlabel('Sales Value (₹)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    # -------------------------------------------

    # -------------------------------------------------------------------------
    # Q10: EXECUTIVE AGGREGATION ANALYSIS
    # -------------------------------------------------------------------------
    # 🎯 BUSINESS USE-CASE: Preparing top-level executive KPI dashboards for Management/VP reports.
    # 🧠 MEMORY TRICK: Aggregations (.sum(), .mean(), .max(), .min()) convert raw data into single KPI numbers.
    # 💡 WHAT THIS DOES: Evaluates Total Revenue (GMV), Average Order Value, Peak & Baseline Sale.
    print("\n[STAGE 10/10] Q10: EXECUTIVE SALES AGGREGATION")
    print("-" * 60)

    tot_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()
    max_sales = df['Sales'].max()
    min_sales = df['Sales'].min()

    print(f"1. Total Gross Revenue (GMV) : ₹{tot_sales:,.2f}")
    print(f"2. Average Invoice Size      : ₹{avg_sales:,.2f}")
    print(f"3. Peak Single Transaction   : ₹{max_sales:,.2f}")
    print(f"4. Baseline Minimum Sale     : ₹{min_sales:,.2f}")

    # --- Visualization for Regional Sales Performance ---
    print("\n--- Regional Sales Performance (Bar Chart) ---")
    sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sales_by_region.index, y=sales_by_region.values, palette='viridis')
    plt.title('Total Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Total Sales (₹)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    # ---------------------------------------------------

    print("\n" + "=" * 80)
    print("✅ PIPELINE EXECUTION COMPLETE | PRODUCTION READY FOR RECRUITERS")
    print("=" * 80)

if __name__ == '__main__':
    run_analytics_pipeline()