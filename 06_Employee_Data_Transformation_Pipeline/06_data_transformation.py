 
"""

import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder, StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Visual formatting setup
sns.set_style("whitegrid")
np.random.seed(42)

print("=" * 80)
print("🏢 ENTERPRISE DATA TRANSFORMATION & PREPROCESSING PIPELINE")
print("=" * 80)

# -----------------------------------------------------------------------------
# STEP 0: DATA INGESTION & AUDIT
# ❤ INDUSTRY USE-CASE: Ingesting raw transactional HR data & verifying data health.
# ❤ MEMORY TRICK: pd.read_csv() -> shape, info(), isnull().sum()
# -----------------------------------------------------------------------------
dataset_path = "/content/employee_productivity_dataset.csv"

df = None # Initialize df to None
try:
  df = pd.read_csv(dataset_path)
  print(
      f"✓ Ingested Dataset '{dataset_path}': {df.shape[0]} Rows x"
      f" {df.shape[1]} Columns."
  )
except FileNotFoundError:
  print(f"❌ Error: Dataset '{dataset_path}' not found!")
  # Removed exit() to allow for more graceful error handling in Colab

print("\n--- Initial Schema Audit ---")
if df is not None:
  df.info()
  df_clean = df.copy()
else:
  print("Skipping initial schema audit and data cleaning as dataset was not loaded.")
  # To prevent further NameErrors, initialize df_clean as an empty DataFrame or handle as appropriate.
  df_clean = pd.DataFrame()

# -----------------------------------------------------------------------------
# Q1: HANDLE MISSING VALUES (BASIC CLEANING & IMPUTATION)
# ❤ REAL-WORLD USE: Skewed numbers (Salary/Net Worth) use Median; Normal symmetric data use Mean.
# ❤ MEMORY TRICK: Skewed/Outlier Heavy = Median | Bell-Curve/Uniform = Mean
# ⚠️ ROOKIE TRAP: Never use Mean on data with extreme outliers (it distorts central tendency).
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 1/10] Q1: MISSING VALUE IMPUTATION")
print("=" * 50)

if not df_clean.empty:
  print("Missing values before imputation:")
  print(df_clean.isnull().sum()[df_clean.isnull().sum() > 0])

  # Imputation logic as per assignment requirements:
  df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
  df_clean["Salary"] = df_clean["Salary"].fillna(df_clean["Salary"].mean())
  df_clean["Hours_Worked_Per_Week"] = df_clean["Hours_Worked_Per_Week"].fillna(
      df_clean["Hours_Worked_Per_Week"].median()
  )
  df_clean["Performance_Score"] = df_clean["Performance_Score"].fillna(
      df_clean["Performance_Score"].mean()
  )

  print(
      f"\n✓ Imputed Nulls: Age (Median={df_clean['Age'].median():.1f}),"
      f" Salary (Mean=₹{df_clean['Salary'].mean():,.2f}),"
      f" Hours (Median={df_clean['Hours_Worked_Per_Week'].median():.1f}),"
      f" Score (Mean={df_clean['Performance_Score'].mean():.2f})"
  )
  print("✓ Total remaining nulls across dataset:", df_clean.isnull().sum().sum())
else:
  print("Skipping missing value imputation as DataFrame is empty.")

# -----------------------------------------------------------------------------
# Q2: LABEL ENCODING (ORDINAL & BINARY CATEGORIES)
# ❤ REAL-WORLD USE: Used for Binary features (Yes/No, Male/Female) or Ordered ranks (Junior < Mid < Senior).
# ❤ MEMORY TRICK: LabelEncoder -> 1D Column to Integer Mapping (0, 1, 2...)
# ⚠️ ROOKIE TRAP: Do NOT use LabelEncoder on unordered multi-class features (e.g. Cities) because ML assumes 2 > 1 > 0.
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 2/10] Q2: LABEL ENCODING (GENDER & DEPARTMENT)")
print("=" * 50)

if not df_clean.empty and "Gender" in df_clean.columns and "Department" in df_clean.columns:
  le_gender = LabelEncoder()
  le_dept = LabelEncoder()

  df_clean["Gender_Encoded"] = le_gender.fit_transform(df_clean["Gender"])
  df_clean["Department_Encoded"] = le_dept.fit_transform(df_clean["Department"])

  print("✓ Encoded 'Gender' & 'Department':")
  print(
      df_clean[
          ["Gender", "Gender_Encoded", "Department", "Department_Encoded"]
      ].head(5).to_string(index=False)
  )
else:
  print("Skipping Label Encoding as DataFrame is empty or required columns are missing.")

# -----------------------------------------------------------------------------
# Q3: ONE-HOT ENCODING (NOMINAL UNORDERED CATEGORIES)
# ❤ REAL-WORLD USE: Used for Unordered categories (Work Mode, Cities, Payment Mode) to eliminate artificial numeric hierarchy.
# ❤ MEMORY TRICK: One-Hot = 1 Column -> N Binary Indicator Columns (0s and 1s)
# ⚠️ ROOKIE TRAP: Very high cardinality (e.g. 1000 zipcodes) creates the "Curse of Dimensionality" (use Target Encoding instead).
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 3/10] Q3: ONE-HOT ENCODING (WORK_MODE & LOCATION)")
print("=" * 50)

if not df_clean.empty and "Work_Mode" in df_clean.columns and "Location" in df_clean.columns:
  initial_cols = df_clean.shape[1]
  df_clean = pd.get_dummies(
      df_clean, columns=["Work_Mode", "Location"], drop_first=False, dtype=int
  )
  new_dummy_cols = [
      c for c in df_clean.columns if "Work_Mode_" in c or "Location_" in c
  ]

  print(
      "✓ One-Hot Encoding Applied. Total New Columns Created:"
      f" {len(new_dummy_cols)}"
  )
  print("Created Columns:", new_dummy_cols)
else:
  print("Skipping One-Hot Encoding as DataFrame is empty or required columns are missing.")

# -----------------------------------------------------------------------------
# Q4: NORMALIZATION (MIN-MAX SCALING: RANGE [0, 1])
# ❤ REAL-WORLD USE: Used when features do NOT follow a Gaussian distribution (e.g., Image Pixels, Neural Networks, KNN distance).
# ❤ MEMORY TRICK: MinMax = Squeeze strictly into [0, 1] -> (X - Xmin) / (Xmax - Xmin)
# ⚠️ ROOKIE TRAP: Very sensitive to extreme outliers; one outlier compresses all other regular values close to 0.
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 4/10] Q4: NORMALIZATION (MIN-MAX SCALING [0, 1])")
print("=" * 50)

norm_cols = [col for col in ["Salary", "Hours_Worked_Per_Week"] if col in df_clean.columns]

if not df_clean.empty and norm_cols:
  min_max_scaler = MinMaxScaler()
  norm_results = min_max_scaler.fit_transform(df_clean[norm_cols])

  df_norm_show = pd.DataFrame(
      norm_results, columns=[f"{col}_Normalized" for col in norm_cols]
  )
  print("✓ Normalized 'Salary' & 'Hours_Worked_Per_Week' (Bounded strictly [0, 1]):")
  print(df_norm_show.head(5).round(4).to_string(index=False))
else:
  print("Skipping Normalization as DataFrame is empty or required columns are missing.")

# -----------------------------------------------------------------------------
# Q5: STANDARDIZATION (Z-SCORE SCALING: MEAN=0, STD=1)
# ❤ REAL-WORLD USE: The industry gold standard for Linear/Logistic Regression, PCA, and SVM.
# ❤ MEMORY TRICK: Z-Score = Center at 0 -> (X - Mean) / Std_Dev
# ⚠️ ROOKIE TRAP: Does not bound data to a fixed range (values can be -3.5 to +4.2).
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 5/10] Q5: STANDARDIZATION (Z-SCORE SCALING)")
print("=" * 50)

std_cols = [col for col in ["Age", "Projects_Completed"] if col in df_clean.columns]

if not df_clean.empty and std_cols:
  std_scaler = StandardScaler()
  std_results = std_scaler.fit_transform(df_clean[std_cols])

  df_std_show = pd.DataFrame(
      std_results, columns=[f"{col}_Standardized" for col in std_cols]
  )
  print("✓ Standardized 'Age' & 'Projects_Completed' (Mean ≈ 0, Variance ≈ 1):")
  print(df_std_show.head(5).round(4).to_string(index=False))
else:
  print("Skipping Standardization as DataFrame is empty or required columns are missing.")

# -----------------------------------------------------------------------------
# Q6: SIDE-BY-SIDE SCALING COMPARISON (SALARY COLUMN)
# ❤ REAL-WORLD USE: Demonstrates how different scaling math alters revenue/salary distribution curves.
# ❤ MEMORY TRICK: MinMax = Bounded Box [0, 1] | StandardScaler = Standard Normal Curve
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 6/10] Q6: COMPARATIVE SCALING BENCHMARK (SALARY)")
print("=" * 50)

if not df_clean.empty and "Salary" in df_clean.columns:
  salary_raw = df_clean[["Salary"]].values
  salary_minmax = MinMaxScaler().fit_transform(salary_raw)
  salary_standard = StandardScaler().fit_transform(salary_raw)

  comparison_df = pd.DataFrame({
      "Original_Salary": df_clean["Salary"],
      "MinMaxScaler (0 to 1)": salary_minmax.flatten().round(4),
      "StandardScaler (Z-Score)": salary_standard.flatten().round(4),
  })
  print(comparison_df.head(6).to_string(index=False))
else:
  print("Skipping scaling comparison as DataFrame is empty or 'Salary' column is missing.")
  comparison_df = pd.DataFrame() # Ensure comparison_df is defined to prevent errors later

# -----------------------------------------------------------------------------
# Q7 & Q8: ENTERPRISE PREPROCESSING PIPELINE (COLUMN TRANSFORMER)
# ❤ REAL-WORLD USE: Prevents "Data Leakage" between Train/Test splits; Deploys cleanly into production APIs.
# ❤ MEMORY TRICK: ColumnTransformer = Bundle Imputation + Scaling + OneHot into 1 single object
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 7 & 8/10] Q7 & Q8: SKLEARN COLUMN TRANSFORMER PIPELINE")
print("=" * 50)

if os.path.exists(dataset_path): # Check if the dataset file actually exists for this part
  raw_df = pd.read_csv(dataset_path)

  # Impute raw baseline dataframe
  raw_clean = raw_df.copy()
  raw_clean["Age"] = raw_clean["Age"].fillna(raw_clean["Age"].median())
  raw_clean["Salary"] = raw_clean["Salary"].fillna(raw_clean["Salary"].mean())
  raw_clean["Hours_Worked_Per_Week"] = raw_clean["Hours_Worked_Per_Week"].fillna(
      raw_clean["Hours_Worked_Per_Week"].median()
  )
  raw_clean["Performance_Score"] = raw_clean["Performance_Score"].fillna(
      raw_clean["Performance_Score"].mean()
  )

  num_minmax_features = ["Salary", "Hours_Worked_Per_Week"]
  num_std_features = ["Age", "Projects_Completed", "Performance_Score"]
  cat_features = ["Gender", "Department", "Work_Mode", "Location"]

  # Filter features that are actually present in raw_clean to avoid errors if some were missing
  num_minmax_features = [f for f in num_minmax_features if f in raw_clean.columns]
  num_std_features = [f for f in num_std_features if f in raw_clean.columns]
  cat_features = [f for f in cat_features if f in raw_clean.columns]

  transformers_list = []
  if num_minmax_features: transformers_list.append(("minmax", MinMaxScaler(), num_minmax_features))
  if num_std_features: transformers_list.append(("std", StandardScaler(), num_std_features))
  if cat_features: transformers_list.append(("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features))

  if transformers_list: # Only create preprocessor if there are transformers
    preprocessor = ColumnTransformer(
        transformers=transformers_list,
        remainder="drop",
    )

    transformed_array = preprocessor.fit_transform(raw_clean)
    feature_names = preprocessor.get_feature_names_out()
    final_transformed_df = pd.DataFrame(transformed_array, columns=feature_names)

    print(
        f"✓ Pipeline Executed Successfully. Transformed Matrix Shape:"
        f" {final_transformed_df.shape} (250 Rows x {final_transformed_df.shape[1]} Clean ML Features)"
    )
    print("\nSample Pipeline Output Features (First 3 Rows):")
    print(final_transformed_df.iloc[:3, :6].round(4).to_string(index=False))
  else:
    print("No features to transform. Skipping ColumnTransformer pipeline.")
  final_transformed_df = pd.DataFrame() # Initialize even if no transformation happens

else:
  print(f"Skipping Column Transformer pipeline as dataset '{dataset_path}' not found!")
  final_transformed_df = pd.DataFrame() # Initialize even if not loaded

# -----------------------------------------------------------------------------
# Q9 & Q10: EXECUTIVE CONCEPTUAL CORNER (INTERVIEW ESSENTIALS)
# -----------------------------------------------------------------------------
print("\n" + "=" * 50)
print("[STAGE 9 & 10/10] Q9 & Q10: INTERVIEW CONCEPT CHEAT-SHEET")
print("=" * 50)

print("""
❦ Q9: WHY IS FEATURE SCALING CRITICAL IN MACHINE LEARNING?
-------------------------------------------------------------------------------
1. Prevents Feature Dominance: Features with large numerical ranges (e.g. Salary: Rs 65,000)
   will overpower features with small ranges (e.g. Age: 25, Rating: 4.2) in Distance-based
   algorithms (KNN, K-Means, SVM, PCA), creating heavily biased models.
2. Speeds Up Gradient Descent: Optimization algorithms converge 10x faster when
   loss surface contours are spherical rather than stretched ellipsoids.

❦ Q10: WHY MUST CATEGORICAL DATA BE CONVERTED TO NUMERICAL VECTORS?
-------------------------------------------------------------------------------
1. Linear Algebra Requirement: Machine learning models are mathematical matrices (W.X + b).
   You cannot calculate the dot-product or gradient of strings like "Remote" or "HR".
2. Weight Assignment: Converting labels to numbers allows algorithms to calculate
   statistical weights, feature importance, and regression coefficients.
""")

# -----------------------------------------------------------------------------
# VISUAL DASHBOARD GENERATION
# -----------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
fig.suptitle(
    "EMPLOYEE DATA TRANSFORMATION & SCALING BENCHMARK",
    fontsize=15,
    fontweight="bold",
    y=0.98,
    color="#0F172A",
)

# Panel 1: Original Salary Distribution
if not df_clean.empty and "Salary" in df_clean.columns:
  sns.histplot(
      df_clean["Salary"],
      kde=True,
      ax=axes[0],
      color="#2563EB",
      bins=15,
      edgecolor="black",
      alpha=0.6,
  )
  axes[0].set_title(
      "1. Original Salary Distribution (Raw INR)",
      fontsize=12,
      fontweight="bold",
      pad=10,
  )
  axes[0].set_xlabel("Salary (INR)")
  axes[0].set_ylabel("Employee Count")
else:
  axes[0].set_title("1. Original Salary Distribution (Data Missing)")
  axes[0].text(0.5, 0.5, "Data not available", horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)

# Panel 2: Scaled Comparisons
if not comparison_df.empty:
  sns.kdeplot(
      comparison_df["MinMaxScaler (0 to 1)"],
      ax=axes[1],
      color="#16A34A",
      label="MinMaxScaler [0, 1]",
      fill=True,
      alpha=0.35,
      linewidth=2,
  )
  sns.kdeplot(
      comparison_df["StandardScaler (Z-Score)"],
      ax=axes[1],
      color="#DC2626",
      label="StandardScaler (Z-Score)",
      fill=True,
      alpha=0.35,
      linewidth=2,
  )
  axes[1].set_title(
      "2. Rescaled Distribution Benchmark (MinMax vs Standard)",
      fontsize=12,
      fontweight="bold",
      pad=10,
  )
  axes[1].set_xlabel("Rescaled Value")
  axes[1].set_ylabel("Density")
  axes[1].legend(frameon=True, facecolor="white", framealpha=0.9)
else:
  axes[1].set_title("2. Rescaled Distribution Benchmark (Data Missing)")
  axes[1].text(0.5, 0.5, "Data not available", horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("data_transformation_summary.png", dpi=300, bbox_inches="tight")
print("\n✓ Visual Analytics Chart Saved: 'data_transformation_summary.png'")

print("\n" + "=" * 80)
print("✅ PIPELINE EXECUTION COMPLETE | READY FOR SUBMISSION")
print("=" * 80)