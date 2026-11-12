import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "raw" / "sms-call-internet-mi-2013-11-01.txt"

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

df = pd.read_csv(DATA_FILE, sep="\t", header=None, names=columns)

# Convert timestamp
df["datetime"] = pd.to_datetime(df["time_interval"], unit="ms", utc=True).dt.tz_convert(
    "Europe/Rome"
)

print("\n--- DATASET OVERVIEW ---")
print("Total records:", len(df))
print("Unique geographic cells:", df["square_id"].nunique())
print("Unique timestamps:", df["time_interval"].nunique())
print("Unique country codes:", df["country_code"].nunique())

print("\n--- TIME RANGE ---")
print("Start:", df["datetime"].min())
print("End:", df["datetime"].max())

print("\n--- COUNTRY CODES ---")
print(df["country_code"].value_counts().head(10))

print("\n--- INTERNET TRAFFIC AVAILABILITY ---")
print("Available:", df["internet_traffic"].notna().sum())
print("Missing:", df["internet_traffic"].isna().sum())

print("\n--- DUPLICATE OBSERVATIONS ---")
duplicates = df.duplicated(subset=["square_id", "time_interval", "country_code"]).sum()

print("Duplicate records:", duplicates)

print("\n--- RECORDS PER TIMESTAMP ---")
print(df.groupby("time_interval").size().describe())

print("\n--- INTERNET OBSERVATIONS PER TIMESTAMP ---")
print(df.groupby("time_interval")["internet_traffic"].count().describe())
