import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, f_oneway, chi2_contingency


def cohens_d(group_a, group_b):
    """
    Effect size for a t-test. With ~58M rows, p-values will be
    significant almost by default even for tiny, practically meaningless
    differences, so we report Cohen's d alongside every t-test to judge
    whether the difference is actually large enough to matter.
    """
    n_a, n_b = len(group_a), len(group_b)
    pooled_std = np.sqrt(
        ((n_a - 1) * group_a.var(ddof=1) + (n_b - 1) * group_b.var(ddof=1))
        / (n_a + n_b - 2)
    )
    return (group_a.mean() - group_b.mean()) / pooled_std

# ==========================================
# Load Dataset
# ==========================================
df = pd.read_csv("clean_dataset.csv")

print("=" * 60)
print("Advanced Statistical Analysis")
print("=" * 60)

# ==========================================================
# 1. T-Test : Weekend vs Weekday Sales
# ==========================================================
print("\n1. T-Test (Weekend vs Weekday)")

weekend_sales = df[df["is_weekend"] == 1]["sales"]
weekday_sales = df[df["is_weekend"] == 0]["sales"]

# equal_var=False -> Welch's t-test. Real-world sales data is unlikely
# to have equal variance between groups, so we don't assume it.
t_stat, p_value = ttest_ind(weekend_sales, weekday_sales, equal_var=False)
effect_size = cohens_d(weekend_sales, weekday_sales)

print(f"T-Statistic : {t_stat:.4f}")
print(f"P-Value     : {p_value:.6f}")
print(f"Cohen's d   : {effect_size:.4f}")

if p_value < 0.05:
    print("There is a significant difference between weekend and weekday sales.")
    print("(Check Cohen's d above - with this sample size, statistical")
    print("significance does not automatically mean a practically large effect.)")
else:
    print("There is no significant difference between weekend and weekday sales.")

# ==========================================================
# 2. T-Test : SNAP vs Non-SNAP
# ==========================================================
print("\n" + "=" * 60)
print("2. T-Test (SNAP vs Non-SNAP)")

snap_sales = df[df["snap"] == 1]["sales"]
non_snap_sales = df[df["snap"] == 0]["sales"]

t_stat, p_value = ttest_ind(snap_sales, non_snap_sales, equal_var=False)
effect_size = cohens_d(snap_sales, non_snap_sales)

print(f"T-Statistic : {t_stat:.4f}")
print(f"P-Value     : {p_value:.6f}")
print(f"Cohen's d   : {effect_size:.4f}")

if p_value < 0.05:
    print("There is a significant difference between SNAP and Non-SNAP sales.")
else:
    print("There is no significant difference between SNAP and Non-SNAP sales.")

# ==========================================================
# 3. ANOVA : Sales Across Months
# ==========================================================
print("\n" + "=" * 60)
print("3. ANOVA (Sales Across Months)")

monthly_groups = []

for month in sorted(df["month"].unique()):
    monthly_groups.append(df[df["month"] == month]["sales"])

f_stat, p_value = f_oneway(*monthly_groups)

print(f"F-Statistic : {f_stat:.4f}")
print(f"P-Value     : {p_value:.6f}")

if p_value < 0.05:
    print("Average sales differ significantly across months.")
else:
    print("No significant difference in average sales across months.")

# ==========================================================
# 4. Chi-Square Test : Event vs Weekend
# ==========================================================
print("\n" + "=" * 60)
print("4. Chi-Square Test (Event vs Weekend)")

contingency_table = pd.crosstab(df["is_event"], df["is_weekend"])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic : {chi2:.4f}")
print(f"P-Value              : {p_value:.6f}")
print(f"Degrees of Freedom   : {dof}")

if p_value < 0.05:
    print("There is a significant association between Event and Weekend.")
else:
    print("There is no significant association between Event and Weekend.")

# ==========================================================
# 5. Chi-Square Test : SNAP vs Event
# ==========================================================
print("\n" + "=" * 60)
print("5. Chi-Square Test (SNAP vs Event)")

contingency_table = pd.crosstab(df["snap"], df["is_event"])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic : {chi2:.4f}")
print(f"P-Value              : {p_value:.6f}")
print(f"Degrees of Freedom   : {dof}")

if p_value < 0.05:
    print("There is a significant association between SNAP and Event.")
else:
    print("There is no significant association between SNAP and Event.")

print("\n" + "=" * 60)
print("Note: 5 hypothesis tests were run above at alpha=0.05 without a")
print("multiple-comparisons correction (e.g. Bonferroni), which raises")
print("the chance of at least one false positive. Treat borderline")
print("p-values with that in mind.")
print("=" * 60)
print("Statistical Analysis Completed Successfully!")
print("=" * 60)