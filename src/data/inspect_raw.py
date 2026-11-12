
from pathlib import Path

# Locate the project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "sms-call-internet-mi-2013-11-01.txt"
)

# Check whether the file exists
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# Display basic file information
print("File:", DATA_FILE.name)
print("File size:", round(DATA_FILE.stat().st_size / (1024 * 1024), 2), "MB")

# Read and inspect the first five raw records
print("\nFirst five records:\n")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    for i in range(5):
        line = file.readline()

        if not line:
            break

        print(repr(line))
