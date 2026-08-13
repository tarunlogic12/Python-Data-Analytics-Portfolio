
"""

"""
===============================================================================
HEALTHCARE DATA CLEANING, ETL & RISK ANALYTICS PIPELINE
===============================================================================
Author      : Tarun Das
Domain      : Healthcare Operations & Enterprise Data Quality Assurance
Dataset     : healthcare_data_cleaning_dataset.csv
===============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

# Set random seed for reproducible results
np.random.seed(42)

print("=" * 70)
print("🏥 HEALTHCARE DATA CLEANING & RISK ANALYTICS PIPELINE")
print("=" * 70)

# -----------------------------------------------------------------------------
# STEP 0: LOAD DATASET
# -----------------------------------------------------------------------------
try:
    df = pd.read_csv("healthcare_data_cleaning_dataset.csv")
    print(f"\n[SUCCESS] Raw Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except FileNotFoundError:
    print("\n[ERROR] CSV File not found! Please verify filename.")
    exit()

# -----------------------------------------------------------------------------
# Q1: MISSING DATA IDENTIFICATION
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("📋 Q1: MISSING DATA IDENTIFICATION")
print("-" * 50)
missing_count = df.isnull().sum()
missing_pct = (missing_count / len(df)) * 100

missing_summary = pd.DataFrame(
    {"Missing Count": missing_count, "Missing Percentage (%)": missing_pct.round(2)}
)
print(missing_summary)

# -----------------------------------------------------------------------------
# Q2: HANDLING MISSING AGE
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("🩹 Q2: HANDLING MISSING AGE")
print("-" * 50)
mean_age = df["Age"].mean()
median_age = df["Age"].median()

print(f"Mean Age: {mean_age:.2f} | Median Age: {median_age:.2f}")

# Justification: Median is robust against extreme outliers and invalid entries.
df["Age"] = df["Age"].fillna(median_age)
print(f"✓ Imputed missing Age values with Median: {median_age:.1f}")

# -----------------------------------------------------------------------------
# Q3: HANDLING MISSING TREATMENT COST
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("💰 Q3: HANDLING MISSING TREATMENT COST")
print("-" * 50)
mean_cost = df["Treatment_Cost"].mean()
median_cost = df["Treatment_Cost"].median()

print(f"Skewness of Treatment_Cost: {df['Treatment_Cost'].skew():.2f}")
print(f"Mean Cost: ₹{mean_cost:,.2f} | Median Cost: ₹{median_cost:,.2f}")

# Justification: Treatment cost is right-skewed; median preserves central tendency.
df["Treatment_Cost"] = df["Treatment_Cost"].fillna(median_cost)
print(f"✓ Imputed missing Treatment_Cost with Median: ₹{median_cost:,.2f}")

# -----------------------------------------------------------------------------
# Q4: DUPLICATE PATIENT RECORDS
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("🧹 Q4: DUPLICATE PATIENT RECORDS")
print("-" * 50)
initial_rows = len(df)
duplicate_count = df.duplicated().sum()

# Removing exact duplicate rows
df = df.drop_duplicates().copy()
cleaned_rows = len(df)

print(f"✓ Exact Duplicate Rows Identified & Dropped: {duplicate_count}")
print(f"✓ Verified Dataset Size: {cleaned_rows} rows (Reduced from {initial_rows})")

# -----------------------------------------------------------------------------
# Q5: INVALID AGE VALUES (DATA QUALITY CHECK)
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("🛡️ Q5: INVALID AGE VALUES CHECK")
print("-" * 50)
invalid_age_mask = (df["Age"] <= 0) | (df["Age"] > 100)
invalid_count = invalid_age_mask.sum()

print(f"✓ Invalid Age Records Detected (<=0 or >100): {invalid_count}")
df.loc[invalid_age_mask, "Age"] = median_age
print(f"✓ Replaced anomalous age values with Population Median ({median_age:.1f})")

# -----------------------------------------------------------------------------
# Q6: OUTLIER DETECTION (TREATMENT COST via IQR)
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("📊 Q6: OUTLIER DETECTION VIA IQR METHOD")
print("-" * 50)
Q1 = df["Treatment_Cost"].quantile(0.25)
Q3 = df["Treatment_Cost"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[
    (df["Treatment_Cost"] < lower_bound) | (df["Treatment_Cost"] > upper_bound)
]

print(f"✓ Q1 (25th Percentile): ₹{Q1:,.2f}")
print(f"✓ Q3 (75th Percentile): ₹{Q3:,.2f}")
print(f"✓ Interquartile Range (IQR): ₹{IQR:,.2f}")
print(f"✓ Outlier Thresholds: [Lower: ₹{lower_bound:,.2f} | Upper: ₹{upper_bound:,.2f}]")
print(f"✓ Number of Cost Outliers Detected: {len(outliers)}")

# -----------------------------------------------------------------------------
# Q7: OUTLIER TREATMENT (WINSORIZATION / CAPPING)
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("✂️ Q7: OUTLIER TREATMENT (5TH & 95TH PERCENTILE CAPPING)")
print("-" * 50)
p5 = df["Treatment_Cost"].quantile(0.05)
p95 = df["Treatment_Cost"].quantile(0.95)

print(f"✓ 5th Percentile Cap: ₹{p5:,.2f}")
print(f"✓ 95th Percentile Cap: ₹{p95:,.2f}")

df["Treatment_Cost_Capped"] = df["Treatment_Cost"].clip(lower=p5, upper=p95)
print("✓ Applied Winsorization capping to 'Treatment_Cost_Capped'")

# -----------------------------------------------------------------------------
# Q8: TRANSFORMATION (LOG TRANSFORMATION)
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("📈 Q8: LOG TRANSFORMATION FOR SKEW REDUCTION")
print("-" * 50)
skew_before = df["Treatment_Cost"].skew()
df["Treatment_Cost_Log"] = np.log1p(df["Treatment_Cost_Capped"])
skew_after = df["Treatment_Cost_Log"].skew()

print(f"✓ Skewness Before Transformation: {skew_before:.4f}")
print(f"✓ Skewness After Log Transformation: {skew_after:.4f}")

# -----------------------------------------------------------------------------
# Q9: TIME-BASED MISSING HANDLING
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("📅 Q9: CHRONOLOGICAL SORTING & TIME-SERIES IMPUTATION")
print("-" * 50)
df["Admission_Date"] = pd.to_datetime(df["Admission_Date"])
df = df.sort_values(by="Admission_Date").reset_index(drop=True)

# Forward fill followed by backward fill
df["Admission_Date"] = df["Admission_Date"].ffill().bfill()
print("✓ Chronological sorting complete. Time-series forward/backward fill verified.")

# -----------------------------------------------------------------------------
# Q10: PATIENT RISK STRATIFICATION (PRO-LEVEL INDUSTRY FEATURE)
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("🚀 Q10: ADVANCED FEATURE ENGINEERING (PATIENT RISK SCORING)")
print("-" * 50)

# Normalize metrics between 0 and 1
scaler = MinMaxScaler()
risk_features = ["Age", "Hospital_Visits", "Treatment_Cost_Capped"]
norm_matrix = scaler.fit_transform(df[risk_features])

# Composite Risk Score Calculation (30% Age + 40% Visits + 30% Cost)
df["Patient_Risk_Score"] = (
    (norm_matrix[:, 0] * 0.30) +
    (norm_matrix[:, 1] * 0.40) +
    (norm_matrix[:, 2] * 0.30)
) * 100

# Stratify into Actionable Business Tiers
df["Risk_Tier"] = pd.qcut(df["Patient_Risk_Score"], q=3, labels=["Low Risk", "Medium Risk", "High Risk"])

print("✓ Calculated Weighted Composite 'Patient_Risk_Score' (0-100 scale).")
print("✓ Stratified patients into 'Low', 'Medium', and 'High' Risk Tiers.")

# Risk Summary Output
risk_summary = df.groupby("Risk_Tier").agg(
    Patient_Count=("Patient_ID", "count"),
    Avg_Risk_Score=("Patient_Risk_Score", "mean"),
    Avg_Treatment_Cost=("Treatment_Cost_Capped", "mean"),
    Avg_Hospital_Visits=("Hospital_Visits", "mean")
).round(2)

print("\n📊 EXECUTIVE RISK STRATIFICATION SUMMARY:")
print(risk_summary)

# -----------------------------------------------------------------------------
# EXTRA PRO ADDITIONS: OPTIMIZATION & ADVANCED OUTLIER MODELING
# -----------------------------------------------------------------------------
print("\n" + "-" * 50)
print("⚡ EXTRA PRO ADDITIONS: MEMORY OPTIMIZATION & ISOLATION FOREST")
print("-" * 50)

# Memory Optimization
df["Age"] = df["Age"].astype("int16")
df["Hospital_Visits"] = df["Hospital_Visits"].astype("int16")
df["Insurance_Coverage"] = df["Insurance_Coverage"].astype("int8")
df["Gender"] = df["Gender"].astype("category")
df["City"] = df["City"].astype("category")
df["Diagnosis"] = df["Diagnosis"].astype("category")

# Isolation Forest ML Outlier Check
iso_forest = IsolationForest(contamination=0.02, random_state=42)
df["Isolation_Forest_Outlier"] = iso_forest.fit_predict(df[["Treatment_Cost"]])
iso_outlier_count = (df["Isolation_Forest_Outlier"] == -1).sum()
print(f"✓ ML Isolation Forest Outliers Detected: {iso_outlier_count}")

print("\n" + "=" * 70)
print("✅ ALL PIPELINE STEPS (Q1-Q10) EXECUTED WITH ZERO ERRORS!")
print("=" * 70)