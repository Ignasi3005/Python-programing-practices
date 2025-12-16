"""
Pandas Quickstart — Example script

Run:
    python examples/pandas_quickstart.py

What it demonstrates:
- Create synthetic dataset (sales by date, region, product)
- Basic inspection: head, info, describe
- Simple cleaning (introduce and fill NA)
- GroupBy aggregation and pivot table
- Save results to CSV
- Plot aggregated sales by region (saved to ./examples/plots directory)
"""

from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

OUTDIR = Path(__file__).parent
PLOTS_DIR = OUTDIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

# Create synthetic data
np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=180)
regions = ["North", "South", "East", "West"]
products = ["Alpha", "Bravo", "Charlie"]

rows = []
for d in dates:
    for r in regions:
        for p in products:
            rows.append({
                "date": d,
                "region": r,
                "product": p,
                "units": int(np.random.poisson(20)),
                "price": round(np.random.uniform(5.0, 50.0), 2),
            })

df = pd.DataFrame(rows)

# Introduce some missing values intentionally
mask = np.random.rand(len(df)) < 0.02
df.loc[mask, "price"] = np.nan

# Inspect
print("--- HEAD ---")
print(df.head())
print("\n--- INFO ---")
print(df.info())
print("\n--- DESCRIPTION (units & price) ---")
print(df[["units", "price"]].describe())

# Cleaning: fill missing price with median price per product
median_price_by_product = df.groupby("product")["price"].transform("median")
df["price"] = df["price"].fillna(median_price_by_product)

# Add revenue column
df["revenue"] = df["units"] * df["price"]

# Aggregation: total revenue by region
rev_by_region = df.groupby("region")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
print("\n--- REVENUE BY REGION ---")
print(rev_by_region)

# Pivot: revenue by product and region
pivot = pd.pivot_table(df, values="revenue", index="product", columns="region", aggfunc="sum")
print("\n--- PIVOT (PRODUCT x REGION) ---")
print(pivot)

# Timeseries: daily revenue
daily = df.groupby("date")["revenue"].sum().reset_index()

# Save outputs
rev_by_region.to_csv(OUTDIR / "revenue_by_region.csv", index=False)
pivot.to_csv(OUTDIR / "revenue_pivot.csv")

# Plot: revenue by region (bar)
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.barplot(data=rev_by_region, x="region", y="revenue", palette="Blues_d")
plt.title("Total Revenue by Region")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "revenue_by_region.png")
plt.close()

# Plot: daily revenue (line)
plt.figure(figsize=(10,4))
plt.plot(daily["date"], daily["revenue"].rolling(7).mean(), label="7-day MA")
plt.title("Daily Revenue (7-day MA)")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "daily_revenue_ma7.png")
plt.close()

print(f"\nSaved outputs in {OUTDIR} and plots in {PLOTS_DIR}")
