# 🏥 Transforming Raw Healthcare Data into Actionable Business Intelligence

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-ETL_Cleansing-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit_Learn-Risk_Stratification-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Verified_&_Tested-success?style=for-the-badge" />
</p>

---

## 📖 The Business Problem
When a hospital's database receives thousands of daily admissions, data errors inevitably creep in: missing patient ages, unrecorded billing amounts, duplicate records, and unrealistic values[cite: 9]. Uncleaned data leads to bad financial planning and poor patient risk monitoring[cite: 9].

This project builds an automated **Data Cleansing and Analytics Pipeline** to transform **5,100 raw patient records** into a clean, decision-ready financial and clinical dataset[cite: 9].

---

## 📊 EXECUTIVE SUMMARY & ETL METRICS (KPI TABLE)

| Data Quality Metric / Stage | Raw Condition | Cleaned Outcome | Business Impact & Takeaway |
| :--- | :---: | :---: | :--- |
| **Total Record Volume** | 5,100 Rows | **5,001 Rows** | Dropped **99 exact duplicate records** to prevent billing inflation[cite: 9]. |
| **Missing Patient Age** | Null Entries | **Median Imputed** | Restored null entries using demographic population medians[cite: 9]. |
| **Anomalous Age Filter** | 49 Invalid Rows | **Fixed (`0 < Age <= 100`)** | Corrected negative/zero/unrealistic age values[cite: 9]. |
| **Financial Outlier Capping** | High Billings | **5th-95th Winsorization** | Capped extreme billing spikes between **₹2,914** and **₹48,188**[cite: 9]. |
| **Log Normalization** | Skewed Costs | **Log1p Applied** | Normalized distribution for accurate predictive modeling[cite: 9]. |

---

## 🖼️ VISUAL ANALYTICS DASHBOARD

![Healthcare Analytics Summary Dashboard](./healthcare_analytics_summary.png)

---

## 🧹 Data Cleansing Journey (ETL)

* **Missing Data Imputation:** Filled missing Age and Treatment Cost using **Median Imputation** to avoid distortion from high-cost surgeries[cite: 9].
* **Deduplication:** Identified and dropped **99 duplicate patient records**, leaving 5,001 unique entries[cite: 9].
* **Anomaly Correction:** Fixed **49 invalid age entries** (`Age <= 0` or `> 100`) using demographic median mapping[cite: 9].
* **Outlier Capping:** Capped extreme financial billing spikes using **5th (₹2,914)** and **95th (₹48,188) percentiles** (Winsorization)[cite: 9].
* **Skewness Correction:** Applied **Log Transformation** (`np.log1p`) to normalize the distribution for predictive modeling[cite: 9].

---

## 💼 Executive Business Insights

1. **Top Revenue Drivers:** **Hypertension (₹2.63 Cr)** and **Diabetes (₹2.58 Cr)** account for the highest cumulative revenue[cite: 9].
2. **High-Cost Diagnosis:** **Flu cases** recorded the highest per-patient average cost (**₹25,924**), indicating high emergency medication needs during peak flu seasons[cite: 9].
3. **Regional Volume:** Hospital visit frequencies are evenly spread across major hubs (**~10 visits/patient** in Mumbai, Delhi, Hyderabad, and Bangalore)[cite: 9].
4. **Insurance Gap:** Uninsured patients average higher billings (**₹25,401**) than insured patients (**₹25,029**), showing an opportunity for micro-insurance products[cite: 9].

---

## 🚀 Pro Business Feature: Patient Risk Stratification
Engineered a composite **Patient Risk Score (0 - 100)** incorporating[cite: 9]:
* **Age (30%)** + **Visit Frequency (40%)** + **Treatment Cost (30%)**[cite: 9]

Categorized patients into 3 actionable tiers[cite: 9]:
* 🟢 **Low Risk:** Routine checkups & stable billing[cite: 9].
* 🟡 **Medium Risk:** Moderate visits requiring standard follow-ups[cite: 9].
* 🔴 **High Risk:** Critical cases requiring proactive care management[cite: 9].

---

## 📁 Repository Structure
* `05_healthcare_data_cleaning.py` — Complete automated Python cleaning pipeline.
* `healthcare_data_cleaning_dataset.csv` — Raw healthcare dataset[cite: 9].
* `healthcare_analytics_summary.png` — 4-Panel Seaborn BI Dashboard.
* `README.md` — Executive summary and non-technical business documentation[cite: 9].

---

## 👤 Author & Credits
**Tarun Das** | *Data Analytics & Generative AI Pro*  
* **GitHub Profile:** [@tarunlogic12](https://github.com/tarunlogic12)
