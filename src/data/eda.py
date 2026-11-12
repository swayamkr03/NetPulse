import pandas as pd
import matplotlib

# Use non-interactive backend to save all charts automatically
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "city_traffic.csv"
CELL_FILE = PROJECT_ROOT / "data" / "processed" / "cell_traffic.csv"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading processed datasets...")

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE, parse_dates=["datetime"])
cells = pd.read_csv(CELL_FILE, index_col=0)

df = df.sort_values("datetime")

print("City-wide records:", len(df))
print("Geographic cells:", cells.shape[1])

# --------------------------------------------------
# 3. TRAFFIC OVER TIME
# --------------------------------------------------

plt.figure(figsize=(14, 5))

plt.plot(df["datetime"], df["total_internet_cdrs"], linewidth=1.5)

plt.title("City-Wide Internet Traffic Over Time")
plt.xlabel("Time")
plt.ylabel("Internet CDR Activity")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(REPORT_DIR / "traffic_over_time.png", dpi=150)

plt.close()

print("Saved: traffic_over_time.png")

# --------------------------------------------------
# 4. HOURLY TRAFFIC
# --------------------------------------------------

df["hour"] = df["datetime"].dt.hour

hourly_traffic = df.groupby("hour")["total_internet_cdrs"].sum()

plt.figure(figsize=(12, 5))

hourly_traffic.plot(kind="bar")

plt.title("Total Internet Traffic by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Total Internet CDR Activity")
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(REPORT_DIR / "hourly_traffic.png", dpi=150)

plt.close()

print("Saved: hourly_traffic.png")

# --------------------------------------------------
# 5. TRAFFIC DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.hist(df["total_internet_cdrs"], bins=20, edgecolor="black")

plt.title("Distribution of City-Wide Internet Traffic")
plt.xlabel("Internet CDR Activity")
plt.ylabel("Frequency")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(REPORT_DIR / "traffic_distribution.png", dpi=150)

plt.close()

print("Saved: traffic_distribution.png")

# --------------------------------------------------
# 6. TOP 10 GEOGRAPHIC CELLS
# --------------------------------------------------

top_cells = cells.sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 5))

top_cells.plot(kind="bar")

plt.title("Top 10 Geographic Cells by Internet Traffic")
plt.xlabel("Geographic Cell")
plt.ylabel("Total Internet CDR Activity")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(REPORT_DIR / "top_traffic_cells.png", dpi=150)

plt.close()

print("Saved: top_traffic_cells.png")

# --------------------------------------------------
# 7. EDA SUMMARY
# --------------------------------------------------

peak_idx = df["total_internet_cdrs"].idxmax()
lowest_idx = df["total_internet_cdrs"].idxmin()

print("\n========== EDA SUMMARY ==========")

print("\nPeak traffic interval:")
print(df.loc[peak_idx, ["datetime", "total_internet_cdrs"]])

print("\nLowest traffic interval:")
print(df.loc[lowest_idx, ["datetime", "total_internet_cdrs"]])

print("\nHourly traffic:")
print(hourly_traffic)

print("\nTop 10 geographic cells:")
print(top_cells)

print("\nTraffic statistics:")
print(df["total_internet_cdrs"].describe())

print("\n=================================")
print("EDA COMPLETED SUCCESSFULLY")
print("Charts saved in:", REPORT_DIR)
print("=================================")
