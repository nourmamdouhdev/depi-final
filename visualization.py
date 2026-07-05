import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# Plot Output Setup
# ============================================
PLOTS_DIR = "visualizations"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ============================================
# Load Dataset
# ============================================
df = pd.read_csv("feature_engineered_dataset.csv")

sns.set_style("whitegrid")

# Plots that draw one mark per row (scatter, KDE, per-point outliers)
# get slow, overplotted, and memory-heavy at ~58M rows without adding
# any visual information over a representative sample. Aggregated plots
# (groupby bar charts, correlation heatmap) use the full data since
# those are cheap and exact either way.
PLOT_SAMPLE_SIZE = 50_000
plot_df = (
    df.sample(n=PLOT_SAMPLE_SIZE, random_state=42)
    if len(df) > PLOT_SAMPLE_SIZE
    else df
)

# ============================================
# 1. Sales Distribution
# ============================================
plt.figure(figsize=(10,5))
sns.histplot(plot_df["sales"], bins=50, kde=True)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Count")
plt.savefig(os.path.join(PLOTS_DIR, "sales_distribution.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 2. Average Sales by Month
# ============================================
monthly_sales = df.groupby("month")["sales"].mean().reset_index()

plt.figure(figsize=(10,5))
sns.barplot(data=monthly_sales,
            x="month",
            y="sales")

plt.title("Average Sales by Month")
plt.xlabel("Month")
plt.ylabel("Average Sales")
plt.savefig(os.path.join(PLOTS_DIR, "average_sales_by_month.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 3. Average Sales by Weekday
# ============================================
weekday_sales = df.groupby("wday")["sales"].mean().reset_index()

plt.figure(figsize=(10,5))
sns.barplot(data=weekday_sales,
            x="wday",
            y="sales")

plt.title("Average Sales by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Average Sales")
plt.savefig(os.path.join(PLOTS_DIR, "average_sales_by_weekday.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 4. Weekend vs Weekday
# ============================================
plt.figure(figsize=(8,5))
sns.boxplot(data=plot_df,
            x="is_weekend",
            y="sales",
            showfliers=False)

plt.title("Weekend vs Weekday Sales")
plt.xlabel("Weekend")
plt.ylabel("Sales")
plt.savefig(os.path.join(PLOTS_DIR, "weekend_vs_weekday_sales.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 5. SNAP Effect
# ============================================
plt.figure(figsize=(8,5))
sns.boxplot(data=plot_df,
            x="snap",
            y="sales",
            showfliers=False)

plt.title("SNAP Effect on Sales")
plt.xlabel("SNAP")
plt.ylabel("Sales")
plt.savefig(os.path.join(PLOTS_DIR, "snap_effect_on_sales.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 6. Event Effect
# ============================================
plt.figure(figsize=(8,5))
sns.boxplot(data=plot_df,
            x="is_event",
            y="sales",
            showfliers=False)

plt.title("Event Effect on Sales")
plt.xlabel("Event")
plt.ylabel("Sales")
plt.savefig(os.path.join(PLOTS_DIR, "event_effect_on_sales.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 7. Price vs Sales
# ============================================
plt.figure(figsize=(10,6))
sns.scatterplot(data=plot_df,
                x="sell_price",
                y="sales",
                alpha=0.4)

plt.title("Price vs Sales")
plt.xlabel("Sell Price")
plt.ylabel("Sales")
plt.savefig(os.path.join(PLOTS_DIR, "price_vs_sales.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 8. Sales by Price Category
# ============================================
plt.figure(figsize=(8,5))
sns.boxplot(data=plot_df,
            x="price_category",
            y="sales",
            showfliers=False)

plt.title("Sales by Price Category")
plt.xlabel("Price Category")
plt.ylabel("Sales")
plt.savefig(os.path.join(PLOTS_DIR, "sales_by_price_category.png"), dpi=300, bbox_inches="tight")
plt.close()

# ============================================
# 9. Correlation Heatmap
# ============================================
plt.figure(figsize=(15,10))

sns.heatmap(df.corr(numeric_only=True),
            cmap="coolwarm",
            annot=False)

plt.title("Correlation Heatmap")
plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"), dpi=300, bbox_inches="tight")
plt.close()

print("="*50)
print("Visualization Completed Successfully!")