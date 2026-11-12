
import pandas as pd
from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset path
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "sms-call-internet-mi-2013-11-01.txt"

# Define column names
columns = [
    "square_id",
    "time_interval",
    "country_code",
    "sms_in",
    "sms_out",
    "call_in",
    "call_out",
    "internet_traffic"
]

# Load only the first 10,000 records initially
df = pd.read_csv(
    DATA_FILE,
    sep="\t",
    header=None,
    names=columns,
    nrows=10000
)

# Display first five records
print("\nFIRST FIVE RECORDS")
print(df.head())

# Dataset dimensions
print("\nDATASET SHAPE")
print(df.shape)

# Column data types
print("\nDATA TYPES")
print(df.dtypes)

# Missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

# Convert Unix timestamp into readable datetime
df["datetime"] = pd.to_datetime(
    df["time_interval"],
    unit="ms",
    utc=True
).dt.tz_convert("Europe/Rome")

print("\nCONVERTED TIMESTAMPS")
print(df[["time_interval", "datetime"]].head())

# Internet traffic summary
print("\nINTERNET TRAFFIC")
print(df["internet_traffic"].describe())
