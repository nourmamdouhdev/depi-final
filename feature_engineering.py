import pandas as pd
import numpy as np

# ============================================
# Load Dataset
# ============================================
df = pd.read_csv("clean_dataset.csv")

print("=" * 50)
print("Original Dataset Shape")
print(df.shape)

# ============================================
# 1. Log Transformation
# ============================================
df["log_sales"] = np.log1p(df["sales"])
df["log_price"] = np.log1p(df["sell_price"])

print("Log Transformation Applied.")

# ============================================
# 2. Price Category
# ============================================
df["price_category"] = pd.qcut(
    df["sell_price"],
    q=3,
    labels=["Low", "Medium", "High"]
)

print("Price Category Feature Created.")

# ============================================
# 3. Season Feature
# ============================================
season_map = {
    1: "Winter",
    2: "Spring",
    3: "Summer",
    4: "Autumn"
}

df["season"] = df["quarter"].map(season_map)

print("Season Feature Created.")

# ============================================
# 4. Encode Categorical Features
# ============================================
# price_category is ORDINAL (Low < Medium < High), so we map it to
# integers that preserve that order. LabelEncoder would encode it
# alphabetically (High=0, Low=1, Medium=2), which silently breaks the
# ordering and distorts any correlation / linear-model analysis
# downstream (correlation.py, RFE).
price_category_order = {"Low": 0, "Medium": 1, "High": 2}
df["price_category"] = df["price_category"].map(price_category_order)

# season is NOMINAL (no natural order between Winter/Spring/Summer/Autumn).
# Label-encoding it would force a fake linear relationship between
# categories, which biases correlation and the LinearRegression-based
# RFE step in correlation.py. One-hot encoding avoids that.
df = pd.get_dummies(df, columns=["season"], prefix="season")

print("Categorical Features Encoded (ordinal map for price_category, one-hot for season).")

# ============================================
# 5. Feature Scaling
# ============================================
# NOTE: Scaling is intentionally NOT applied here.
# Fitting a scaler on the full dataset before any train/test split
# leaks information from future/test rows into the "training"
# distribution (mean/std would be computed using data that shouldn't
# be visible yet in a time-series forecasting setup). Scaling should
# be fit on the training split only, inside the Milestone 3 modeling
# pipeline, and applied to validation/test data using those same
# fitted parameters.
print("Feature Scaling skipped here on purpose - to be fit on the train split only in Milestone 3.")

# ============================================
# Final Dataset Information
# ============================================
print("=" * 50)
print("Dataset Shape After Feature Engineering")
print(df.shape)

print("=" * 50)
print(df.head())

print("=" * 50)
print(df.info())

# ============================================
# Save Dataset
# ============================================
df.to_csv("feature_engineered_dataset.csv", index=False)

print("=" * 50)
print("Feature Engineered Dataset Saved Successfully!")