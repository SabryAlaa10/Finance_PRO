import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from logic.database import (
    database_available, 
    load_transactions_from_db, 
    save_transaction_to_db,
    init_database
)

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
    """Ensure the data directory and CSV file exist, and initialize database if available."""
    # Initialize CSV
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)
    
    # Initialize database if available
    if database_available():
        init_database()

def load_data(user_id=1) -> pd.DataFrame:
    """Load transactions from database (preferred) or CSV file (fallback)."""
    init_db()
    
    # Try loading from database first
    if database_available():
        df = load_transactions_from_db(user_id)
        if df is not None:
            return df
    
    # Fallback to CSV
    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure Date is datetime
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_transaction(date, type_, category, source, amount, description="", user_id=1):
    """Save transaction to database (preferred) or CSV (fallback)."""
    init_db()
    
    # Try saving to database first
    if database_available():
        success = save_transaction_to_db(user_id, date, type_, category, source, amount, description)
        if success:
            return True
    
    # Fallback to CSV
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
    header = not DATA_FILE.exists()
    new_df.to_csv(DATA_FILE, mode='a', header=header, index=False)
    
    return True
