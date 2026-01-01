import pandas as pd
from pathlib import Path
import os
from datetime import datetime

# Define the data directory and file path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "transactions.csv"

# Columns for the transactions CSV
COLUMNS = [
    "Date",
    "Type",        # Income, Expense, Investment, Transfer
    "Category",    # Personal, University, Gym, Gold, Trading, Freelancing, etc.
    "Source",      # Vodafone Cash, InstaPay, Bank A, Bank B, Cash, etc.
    "Amount",
    "Description"
]

def init_db():
    """Ensure the data directory and CSV file exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)

def load_data() -> pd.DataFrame:
    """Load transactions from the CSV file."""
    init_db()
    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure Date is datetime
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_transaction(date, type_, category, source, amount, description=""):
    """Append a new transaction to the CSV."""
    init_db()
    
    # Create a DataFrame for the new row
    new_data = {
        "Date": [date],
        "Type": [type_],
        "Category": [category],
        "Source": [source],
        "Amount": [float(amount)],
        "Description": [description]
    }
    new_df = pd.DataFrame(new_data)
    
    # Append to CSV
    # If file exists, append without header; if not, write with header (handled by init_db/to_csv mode)
    header = not DATA_FILE.exists()
    new_df.to_csv(DATA_FILE, mode='a', header=header, index=False)
    
    return True
