import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "raw" / "sms-call-internet-mi-2013-11-01.txt"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

columns = [
    "square_id",
    "time_interval",
    "country_code",
    "sms_in",
    "sms_out",
    "call_in",
    "call_out",
    "internet_traffic",
]

print("Loading raw dataset...")

df = pd.read_csv(DATA_FILE, sep="\t", header=None, names=columns)

print("Loaded records:", len(df))

# Missing internet activity represents no recorded
# activity for that service in this combination.
df["internet_traffic"] = df["internet_traffic"].fillna(0)

# Aggregate country-code activity for each cell and timestamp.
print("Aggregating geographic cell traffic...")

cell_traffic = (
    df.groupby(["time_interval", "square_id"])["internet_traffic"]
    .sum()
    .unstack(fill_value=0)
)

# Calculate total city-wide internet activity.
city_traffic = cell_traffic.sum(axis=1)

# Convert timestamps into Milan local time.
datetimes = pd.to_datetime(cell_traffic.index, unit="ms", utc=True).tz_convert(
    "Europe/Rome"
)

# Save city-wide dataset.
city_df = pd.DataFrame(
    {"datetime": datetimes, "total_internet_cdrs": city_traffic.values}
)

city_df.to_csv(OUTPUT_DIR / "city_traffic.csv", index=False)

# Save cell-level dataset.
cell_traffic.index = datetimes

cell_traffic.to_csv(OUTPUT_DIR / "cell_traffic.csv")

print("\nAGGREGATION COMPLETE")

print("City-wide records:", len(city_df))
print("Geographic cells:", cell_traffic.shape[1])

print("\nCITY-WIDE TRAFFIC SUMMARY")
print(city_df["total_internet_cdrs"].describe())

print("\nGenerated files:")
print("1. data/processed/city_traffic.csv")
print("2. data/processed/cell_traffic.csv")
