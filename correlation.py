import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# ==========================================
# Plot Output Setup
# ==========================================
PLOTS_DIR = "plots_2"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ==========================================
# Load Dataset
# ==========================================
# Use the FEATURE-ENGINEERED dataset (output of feature_engineering.py)
# so correlation/RFE actually evaluate the new features (price_category,
# season one-hot columns, log_price, etc.), not just the raw Milestone 1
# columns.
df = pd.read_csv("feature_engineered_dataset.csv")

# log_sales is a direct deterministic transform of the target ("sales").
# Keeping it as a candidate feature would leak the target into the
# correlation-with-target and RFE analysis (it would trivially show
# correlation ~1.0 and dominate feature ranking). Drop it from the
# feature-selection view only; it stays in the saved dataset in case
# Milestone 3 wants to model log(sales) as an alternative target.
df_features = df.drop(columns=["log_sales"])

print("=" * 60)
print("Correlation Analysis & RFE")
print("=" * 60)

# ==========================================
# Correlation Matrix
# ==========================================
plt.figure(figsize=(15, 10))

sns.heatmap(
    df_features.corr(numeric_only=True),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Correlation Matrix")
plt.savefig(os.path.join(PLOTS_DIR, "correlation_matrix.png"), dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# Correlation with Target (Sales)
# ==========================================
print("\nCorrelation with Sales:\n")

corr = df_features.corr(numeric_only=True)["sales"].sort_values(ascending=False)

print(corr)

# ==========================================
# Correlation Bar Plot
# ==========================================
plt.figure(figsize=(10,6))

corr.drop("sales").plot(kind="bar")

plt.title("Feature Correlation with Sales")
plt.xlabel("Features")
plt.ylabel("Correlation")

plt.grid(axis="y")

plt.savefig(os.path.join(PLOTS_DIR, "feature_correlation_with_sales.png"), dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# Recursive Feature Elimination (RFE)
# ==========================================
print("\n" + "=" * 60)
print("Recursive Feature Elimination (RFE)")
print("=" * 60)

# RFE only needs to RANK features, not fit a final model, and it refits
# LinearRegression once per elimination step. Running that on the full
# ~58M rows is extremely expensive for no ranking benefit. A random
# sample is enough to get a stable, representative ranking.
RFE_SAMPLE_SIZE = 1_000_000
sample_df = (
    df_features.sample(n=RFE_SAMPLE_SIZE, random_state=42)
    if len(df_features) > RFE_SAMPLE_SIZE
    else df_features
)

# Select numeric features
numeric_df = sample_df.select_dtypes(include=["number"])

# Features
X = numeric_df.drop(columns=["sales"])

# Target
y = numeric_df["sales"]

# LinearRegression-based RFE ranks features by the magnitude of their
# fitted coefficients. Features on different scales (e.g. sell_price vs.
# month vs. wday) would get artificially larger/smaller coefficients
# just because of their units, biasing the ranking. Standardizing here
# is local to this ranking step only - it is NOT saved back into the
# feature_engineered_dataset.csv, so it doesn't affect Milestone 3's
# own train/test scaling.
X_scaled = pd.DataFrame(
    StandardScaler().fit_transform(X),
    columns=X.columns,
    index=X.index
)

# Linear Regression Model
model = LinearRegression()

# Apply RFE
rfe = RFE(
    estimator=model,
    n_features_to_select=10
)

rfe.fit(X_scaled, y)

# Feature Ranking
feature_ranking = pd.DataFrame({
    "Feature": X.columns,
    "Selected": rfe.support_,
    "Ranking": rfe.ranking_
})

feature_ranking = feature_ranking.sort_values(by="Ranking")

print(feature_ranking)

# ==========================================
# Selected Features
# ==========================================
print("\nSelected Features:\n")

print(feature_ranking[feature_ranking["Selected"] == True])

# ==========================================
# RFE Visualization
# ==========================================
plt.figure(figsize=(10,6))

sns.barplot(
    data=feature_ranking,
    x="Ranking",
    y="Feature"
)

plt.title("RFE Feature Ranking")
plt.xlabel("Ranking (1 = Most Important)")
plt.ylabel("Features")

plt.savefig(os.path.join(PLOTS_DIR, "rfe_feature_ranking.png"), dpi=300, bbox_inches="tight")
plt.close()

print("=" * 60)
print("Correlation Analysis & RFE Completed Successfully!")
print("=" * 60)