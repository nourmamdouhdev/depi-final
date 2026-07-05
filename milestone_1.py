import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
# The original hardcoded absolute Windows path (C:\Users\mohab\...) only
# works on one machine. Anchoring to the script's own folder instead makes
# this portable across machines / OSes / CI runners, as long as the data
# lives in a "data" subfolder next to this script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "data.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
OUTPUT_PATH = os.path.join(BASE_DIR, "clean_dataset.csv")

os.makedirs(PLOTS_DIR, exist_ok=True)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Could not find data.csv at {DATA_PATH}. "
        "Update DATA_PATH to point at your local copy of the dataset."
    )


def reduce_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Downcast numeric columns to the smallest safe dtype and convert
    low-cardinality object columns to 'category'.

    With ~58M rows, pandas' default dtypes (int64 / float64 / object) use
    far more memory than the data needs -- e.g. 'wday' only ever holds
    1-7, but int64 reserves 8 bytes per value instead of 1. On this
    dataset that's the difference between ~9.1 GB and roughly a third of
    that, which matters both for avoiding OOM and for making every
    downstream operation (.describe(), .corr(), .duplicated(), to_csv)
    faster.

    Using pd.to_numeric(..., downcast=...) rather than a fixed dtype dict
    in read_csv is the safer choice: it inspects the *actual* values
    already in memory rather than guessing ranges up front, so it can't
    silently overflow or fail to parse.
    """
    start_mem = df.memory_usage(deep=True).sum() / 1024 ** 2

    for col in df.columns:
        col_type = df[col].dtype

        if col_type == "object":
            n_unique = df[col].nunique()
            if n_unique / len(df) < 0.5:
                df[col] = df[col].astype("category")
        elif pd.api.types.is_integer_dtype(col_type):
            df[col] = pd.to_numeric(df[col], downcast="integer")
        elif pd.api.types.is_float_dtype(col_type):
            df[col] = pd.to_numeric(df[col], downcast="float")

    end_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    print(
        f"Memory usage reduced from {start_mem:.1f} MB to {end_mem:.1f} MB "
        f"({100 * (start_mem - end_mem) / start_mem:.1f}% reduction)"
    )
    return df


def save_and_close(filename: str):
    """
    Save the current matplotlib figure to disk instead of calling
    plt.show(). plt.show() blocks execution until the window is closed --
    fine in a notebook, but it means this script can never run unattended
    (cron job, CI pipeline, server) and forces a human to click through
    eight chart windows on every run, on top of the 58M-row processing
    time.
    """
    path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(path, bbox_inches="tight", dpi=100)
    plt.close()
    print(f"Saved plot: {path}")


# ------------------------------------------------------------------
# Load
# ------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df = reduce_memory_usage(df)

print("=" * 50)
print("First 5 Rows")
print(df.head())

print("=" * 50)
print("Dataset Shape")
print(df.shape)

print("=" * 50)
print("Dataset Information")
df.info()
# NOTE: .info() prints its own output and returns None. The original
# `print(df.info())` therefore printed a spurious extra "None" line below
# the real output -- that's why it showed up in your run log.

print("=" * 50)
print("Summary Statistics")
# NOTE: .describe() on the full 58M-row frame is a genuinely expensive
# full-table scan across every numeric column. It's kept here since it's
# a one-time diagnostic step, but be aware of the cost if this script is
# re-run frequently -- consider sampling first if it becomes a bottleneck.
print(df.describe())

print("=" * 50)
print("Columns")
print(df.columns)

print("=" * 50)
print("Missing Values")
print(df.isnull().sum())

print("=" * 50)
print("Duplicate Rows (full row):", df.duplicated().sum())

# A full-row duplicate check hashes all 21 columns across 58M rows, which
# is expensive AND isn't the right definition of "duplicate" for a time
# series. The meaningful business key is one row per store x item x day.
# Checking on that key catches real data integrity problems (the same
# store/item/day appearing twice with different sales figures) that a
# full-row check would miss entirely if even one other column differed.
key_cols = ["store_id", "item_number", "wm_yr_wk", "wday"]
dup_keys = df.duplicated(subset=key_cols).sum()
print(f"Duplicate Rows (store/item/day key): {dup_keys}")

print("=" * 50)
print("Invalid Prices")

# The original check only caught sell_price == -1. Broadened to also
# catch any other non-positive or NaN price, since -1 is just this
# dataset's chosen sentinel and other invalid encodings are possible.
invalid_price_mask = (df["sell_price"] <= 0) | (df["sell_price"].isna())
n_invalid = int(invalid_price_mask.sum())
pct_invalid = 100 * n_invalid / len(df)
print(f"Invalid price rows: {n_invalid} ({pct_invalid:.2f}% of dataset)")

# *** TIME SERIES INTEGRITY WARNING ***
# lag_1 and lag_7 already exist in the source data, meaning they were
# computed upstream, per store/item, in date order, BEFORE this filter
# runs. Dropping ~13M rows here removes days from the *middle* of each
# store-item series, which silently breaks the day-to-day / week-to-week
# continuity those lag features depend on. A row that immediately follows
# a dropped gap will now carry a lag_7 value that does NOT actually
# reflect "7 days ago" -- it reflects whatever day happened to survive
# filtering. This won't raise an error; it will quietly feed incorrect
# features into Milestone 2 modeling. Recomputing lags after filtering is
# out of scope for Milestone 1 as defined, but this should be addressed
# (either recompute lags post-filter, or impute prices instead of
# dropping rows) before those features are trusted downstream.
df = df[~invalid_price_mask].copy()

df["quarter"] = ((df["month"] - 1) // 3 + 1).astype("int8")
df["week_of_month"] = ((df["day"] - 1) // 7 + 1).astype("int8")

# EDA: Exploratory Data Analysis
sample = df.sample(100_000, random_state=42)
# --------------------------------------
# Sales Distribution
plt.figure(figsize=(10, 5))

sns.histplot(sample["sales"], bins=100, kde=True)

plt.title("Sales Distribution")

save_and_close("sales_distribution.png")
# "Sales values are heavily right-skewed, with most records showing low sales (0-3 units) and a long tail of rare high-sales outliers.
# This suggests log transformation may help before modeling, and indicates intermittent/low demand for most products."

# _________________________________
# Sales Outliers
plt.figure(figsize=(10, 5))

sns.boxplot(x=sample["sales"])

plt.title("Sales Boxplot")

save_and_close("sales_boxplot.png")
# Since the sales distribution is highly right-skewed,
# log transformation can be considered in the modeling stage to reduce skewness and improve model performance.

# Boxplot Analysis:
# The boxplot shows that most sales values are concentrated near zero,
# while a large number of higher sales values appear as statistical outliers according to the IQR method.
# These observations are likely genuine demand spikes caused by promotions,
# holidays, or popular products rather than data errors.
# Therefore, the outliers were retained to preserve valuable information for the forecasting model.
# A log transformation may be applied in the modeling stage to reduce skewness.


# ____________________________
# Sales by Month
monthly = sample.groupby("month")["sales"].mean()

plt.figure(figsize=(10, 5))

monthly.plot(kind="bar")

plt.title("Average Monthly Sales")

save_and_close("avg_monthly_sales.png")

# Average monthly sales exhibit mild seasonal variation.
# February has the highest average sales, while January has the lowest.
# However, differences across months are relatively small,
# indicating that seasonality has a moderate influence on sales compared with other factors such as promotions and events.


# ____________________________
# Sales by Week of Month
weekday = sample.groupby("wday")["sales"].mean()

plt.figure(figsize=(10, 5))

weekday.plot(kind="bar")

plt.title("Sales by Weekday")

save_and_close("sales_by_weekday.png")

# Sales exhibit a clear weekly pattern,
# with higher average sales on certain days of the week and lower sales on others.
# This weekly seasonality is more pronounced than the monthly seasonality,
# indicating that the day of the week is an important feature for forecasting sales.

# important to forecasting sales


# ____________________________
# Weekend effect on sales
plt.figure(figsize=(8, 5))

sns.boxplot(data=sample,
            x="is_weekend",
            y="sales")

save_and_close("weekend_effect.png")

# The weekend boxplot confirms the weekly pattern observed previously.
# Weekend days generally have a higher typical sales range and more frequent moderately high sales compared to weekdays.
# Although the highest individual sales value occurs on a weekday,
# it is likely associated with a special event or promotion rather than the regular weekly pattern.

# ____________________________
# SNAP effect on sales
# Combined mean + median into a single groupby pass instead of two
# separate full-table scans over 58M rows.
snap_stats = df.groupby("snap")["sales"].agg(["mean", "median"])
print(snap_stats)
########Result##########
# snap
# 0    1.362728
# 1    1.537341
plt.figure(figsize=(8, 5))

sns.boxplot(data=sample,
            x="snap",
            y="sales")

save_and_close("snap_effect.png")

# SNAP Effect:
# The boxplot shows little visible difference between SNAP and non-SNAP days because sales are heavily right-skewed and the median is zero for both groups.
# However, the average sales increase from 1.36 on non-SNAP days to 1.54 on SNAP days (approximately 13% higher),
# indicating that SNAP has a positive, though moderate, effect on sales.


# ____________________________
# Event effect
print(df["is_event"].value_counts())

# is_event
# 0    41673756
# 1     3635941

event_stats = df.groupby("is_event")["sales"].agg(["mean", "median"])
print(event_stats)
# is_event
# 0    1.426193 / median 0.0
# 1    1.353696 / median 0.0

plt.figure(figsize=(8, 5))

sns.boxplot(data=sample,
            x="is_event",
            y="sales")

save_and_close("event_effect.png")

# Event Effect:
# Event days represent approximately 8% of the observations.
# The average sales on event days (1.354) are slightly lower than on non-event days (1.426),
# while the median sales remain zero for both groups.
# This suggests that the binary is_event feature alone does not show a strong positive relationship with sales.
# Additional event-related features such as event_impact and event_count may provide a better representation of event influence.

print(df[["event_count", "sales"]].corr())

print(df[["event_impact", "sales"]].corr())

# Event Analysis:
# The binary is_event feature does not show a clear positive relationship with sales.
# Event days account for approximately 8% of the dataset and have a slightly lower average sales value than non-event days.
# Furthermore, event_count has virtually no correlation with sales (r = -0.004).
# In contrast, event_impact shows a weak positive correlation (r = 0.158),
# suggesting that the intensity of an event is more informative than simply indicating whether an event occurred.

# ____________________________
# Prices vs Sales
plt.figure(figsize=(10, 5))

sns.scatterplot(data=sample,
                 x="sell_price",
                 y="sales")

save_and_close("price_vs_sales.png")
print(df[["sell_price", "sales"]].corr())

# Price vs. Sales Analysis:
# The scatter plot indicates a negative relationship between product price and sales volume.
# High sales volumes occur almost exclusively among low-priced products,
# while higher-priced products consistently exhibit lower sales volumes.
# The Pearson correlation coefficient between sell_price and sales is -0.150,
# indicating a weak negative linear relationship.
# This suggests that although higher prices generally correspond to lower sales,
# the relationship is likely non-linear and influenced by additional factors such as promotions, product categories, and demand patterns.


# ____________________________
# Correlation Heatmap
plt.figure(figsize=(15, 10))

sns.heatmap(sample.corr(numeric_only=True),
            annot=True,
            cmap="coolwarm")

save_and_close("correlation_heatmap.png")

# Highly correlated engineered features were identified.
# Since the final forecasting model is expected to be based on deep learning (LSTM/RNN),
# these features were retained. However, for linear models, redundant features should be removed to reduce multicollinearity.


print(df["price_flag"].value_counts())
# Remove constant feature
df.drop(columns=["price_flag"], inplace=True)

print(df.shape)

# Constant Feature Removal:
# The price_flag feature contained only a single value (0) across all observations,
# providing no predictive information. Therefore, it was removed from the dataset before modeling.

df.info()

# ------------------------------------------------------------------
# Post-cleaning validation
# ------------------------------------------------------------------
# Cheap sanity checks that confirm the cleaning steps above actually did
# what they claim to. These are informational (printed, not asserted) so
# a genuine data surprise doesn't hard-crash the pipeline -- but they
# should be eyeballed on every run.
print("=" * 50)
print("Post-cleaning validation")
print("sell_price > 0 for all rows:", bool((df["sell_price"] > 0).all()))
print("sales >= 0 for all rows:", bool((df["sales"] >= 0).all()))
print("Remaining full-row duplicates:", int(df.duplicated().sum()))

df.to_csv(OUTPUT_PATH, index=False)

print(f"Clean dataset saved successfully to {OUTPUT_PATH}")