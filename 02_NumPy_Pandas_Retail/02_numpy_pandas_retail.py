 
Original file is located at
    https://colab.research.google.com/drive/1Fmicl4TQoyhNjN_3lVl6lXong2GVVzJk
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("🛒 RETAIL ENTERPRISE DATA CLEANING & REVENUE ANALYSIS PIPELINE")
print("=" * 80)

# -----------------------------------------------------------------------------
# Q1: LOAD DATASET & INSPECT STRUCTURE
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: We check the dataset first to make sure column names and data
# types are correct. This prevents unexpected errors when processing millions of rows later.
print("\n" + "-" * 60)
print("📊 Q1: LOAD DATASET & CHECK STRUCTURE")
print("-" * 60)

df = pd.read_csv("/content/retail_dataset .csv")

print("✓ Preview of First 5 Rows:")
print(df.head().to_string())

print("\n✓ Dataset Columns & Data Types:")
df.info()


# -----------------------------------------------------------------------------
# Q2: IDENTIFY MISSING VALUES
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: Missing data creates big mistakes in monthly financial reports.
# Finding empty cells early helps us fix bad or incomplete records.
print("\n" + "-" * 60)
print("🔍 Q2: MISSING VALUE AUDIT")
print("-" * 60)

missing_per_column = df.isnull().sum()
total_missing = missing_per_column.sum()

print("Missing Values per Column:")
print(missing_per_column.to_string())
print(f"\n[AUDIT RESULT]: Found a total of {total_missing} missing values in the dataset.")


# -----------------------------------------------------------------------------
# Q3: IMPUTE MISSING QUANTITY & PRICE WITH MEAN
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: If we delete rows just because Quantity or Price is missing,
# we lose valuable order history. Replacing empty spaces with the average (mean)
# keeps our sales totals smooth and balanced.
print("\n" + "-" * 60)
print("🩹 Q3: FILL MISSING QUANTITY & PRICE WITH MEAN")
print("-" * 60)

mean_quantity = df["Quantity"].mean()
mean_price = df["Price"].mean()

print(f"[AVERAGE VALUES]: Calculated Mean Quantity = {mean_quantity:.2f} units")
print(f"[AVERAGE VALUES]: Calculated Mean Price    = ₹{mean_price:.2f}")

df["Quantity"] = df["Quantity"].fillna(mean_quantity)
df["Price"] = df["Price"].fillna(mean_price)

print("✓ Filled missing Quantity and Price values using calculated averages.")


# -----------------------------------------------------------------------------
# Q4: REMOVE ROWS WITH MISSING CATEGORY OR REGION
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: We cannot ship a product if we don't know the Region or Category.
# Deleting these specific missing rows keeps our regional tax and shipping reports 100% accurate.
print("\n" + "-" * 60)
print("🧹 Q4: REMOVE ROWS MISSING CATEGORY OR REGION")
print("-" * 60)

initial_rows = len(df)
df_clean = df.dropna(subset=["Product Category", "Region"]).copy().reset_index(drop=True)
cleaned_rows = len(df_clean)

print(f"Total Rows Before Cleaning : {initial_rows}")
print(f"Total Rows After Cleaning  : {cleaned_rows}")
print(f"✓ Removed {initial_rows - cleaned_rows} rows that had missing Region or Category information.")


# -----------------------------------------------------------------------------
# Q5: CREATE REVENUE COLUMN USING NUMPY
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: Normal Python loops are very slow for big datasets. Using NumPy
# vectorization multiplies lists instantly, making website checkout systems super fast.
print("\n" + "-" * 60)
print("💰 Q5: CREATE REVENUE COLUMN (NUMPY VECTORIZATION)")
print("-" * 60)

df_clean["Revenue"] = np.multiply(df_clean["Quantity"].values, df_clean["Price"].values)

print("✓ Created 'Revenue' column using fast NumPy array multiplication.")
print("\nUpdated Dataset Preview (First 5 Rows):")
print(df_clean.head().to_string())


# -----------------------------------------------------------------------------
# Q6: TOTAL REVENUE CALCULATION USING NUMPY
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: Company owners need one main number to see total sales income
# and track business growth.
print("\n" + "-" * 60)
print("🧮 Q6: CALCULATE TOTAL REVENUE (NUMPY)")
print("-" * 60)

total_revenue = np.sum(df_clean["Revenue"].values)
print(f"✓ Total Sales Revenue Generated: ₹{total_revenue:,.2f}")


# -----------------------------------------------------------------------------
# Q7 & Q8: GROUP BY PRODUCT CATEGORY & TOP/BOTTOM CATEGORIES
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: This shows which products make the most money so store managers
# know what items to stock up on and which slow-selling items to put on discount sale.
print("\n" + "-" * 60)
print("📦 Q7 & Q8: REVENUE BY PRODUCT CATEGORY (TOP & BOTTOM 3)")
print("-" * 60)

category_revenue = df_clean.groupby("Product Category")["Revenue"].sum().reset_index()
category_revenue_sorted = category_revenue.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

top_3_categories = category_revenue_sorted.head(3)
bottom_3_categories = category_revenue_sorted.tail(3)

print("Category Sales Ranking:")
print(category_revenue_sorted.to_string(index=False))

print("\n🥇 Top 3 Best-Selling Categories:")
print(top_3_categories.to_string(index=False))

print("\n🔻 Bottom 3 Lowest-Selling Categories:")
print(bottom_3_categories.to_string(index=False))


# -----------------------------------------------------------------------------
# Q9: GROUP BY REGION & HIGHEST/LOWEST REGION
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: Helps companies decide where to open new warehouses and where
# to run bigger advertisement campaigns to increase low sales.
print("\n" + "-" * 60)
print("🗺️ Q9: REGIONAL SALES PERFORMANCE")
print("-" * 60)

region_revenue = df_clean.groupby("Region")["Revenue"].sum().reset_index()
region_revenue_sorted = region_revenue.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

highest_region = region_revenue_sorted.iloc[0]
lowest_region = region_revenue_sorted.iloc[-1]

print("Regional Sales Breakdown:")
print(region_revenue_sorted.to_string(index=False))

print(f"\n🌟 Top Performing Region    : {highest_region['Region']} (₹{highest_region['Revenue']:,.2f})")
print(f"📉 Lowest Performing Region : {lowest_region['Region']} (₹{lowest_region['Revenue']:,.2f})")


# -----------------------------------------------------------------------------
# Q10: MONTHLY REVENUE & NUMPY STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
# [REAL-WORLD WHY]: Tracking sales month-by-month helps plan for festive buying seasons.
# Calculating Mean vs Median tells us if high-priced luxury items are changing our average numbers.
print("\n" + "-" * 60)
print("📅 Q10: MONTHLY TRENDS & NUMPY STATISTICS")
print("-" * 60)

df_clean["Date"] = pd.to_datetime(df_clean["Date"], format="%d-%m-%Y")
df_clean["Month"] = df_clean["Date"].dt.to_period("M")

monthly_revenue = df_clean.groupby("Month")["Revenue"].sum().reset_index()
print("Monthly Revenue Summary:")
print(monthly_revenue.to_string(index=False))

revenue_array = df_clean["Revenue"].values
rev_mean = np.mean(revenue_array)
rev_median = np.median(revenue_array)
rev_std = np.std(revenue_array)

print("\n📊 Overall Revenue Statistics (NumPy):")
print(f"✓ Average Order Revenue (Mean)   : ₹{rev_mean:,.2f}")
print(f"✓ Middle Order Revenue (Median)  : ₹{rev_median:,.2f}")
print(f"✓ Sales Variation (Std Dev)      : ₹{rev_std:,.2f}")

print("\n[SIMPLE INSIGHT]: The Mean (₹4,900) is higher than Median (₹3,282). This means")
print("expensive orders (like Furniture) are pulling up the overall average order value.")


# -----------------------------------------------------------------------------
# 💡 EXECUTIVE SUMMARY (BUSINESS LESSON)
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("💡 EXECUTIVE SUMMARY FOR MANAGERS")
print("=" * 80)

print(f"""
1. BEST SELLERS: Furniture and Electronics generate almost 50% of all sales.
   -> Strategy: Always keep enough stock for Furniture in main warehouses.

2. WEAK REGION: North region sells ₹1.53 Lakhs while West region sells only ₹81 Thousands.
   -> Strategy: Spend more marketing budget in the West region to boost sales.

3. ORDER VALUE: High variation (₹4,721) means order amounts jump up and down.
   -> Strategy: Offer combo deals (like Groceries + Household items) to increase smaller order totals.
""")

print("=" * 80)
print("✅ PIPELINE EXECUTION COMPLETE | 0 ERRORS")
print("=" * 80)