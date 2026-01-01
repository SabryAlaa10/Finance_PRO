import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import streamlit as st
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

@st.cache_data(ttl=300, show_spinner=False)  # Cache for 5 minutes instead of 10 seconds
def load_data_cached(user_id=1, cache_key=None):
    """Load transactions with caching for better performance."""
    print(f"🔄 Loading data for user_id={user_id}, cache_key={cache_key}")
    
    # Try loading from database first
    if database_available():
        try:
            df = load_transactions_from_db(user_id)
            if df is not None and not df.empty:
                print(f"✅ Loaded {len(df)} transactions from database")
                return df
            else:
                print(f"⚠️ Database returned empty, trying CSV")
        except Exception as e:
            print(f"❌ Database load error: {e}, trying CSV")
    else:
        print("⚠️ Database not available, using CSV")
    
    # Fallback to CSV
    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure Date is datetime
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
        print(f"💾 Loaded {len(df)} transactions from CSV")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)

def load_data(user_id=1) -> pd.DataFrame:
    """Load transactions from database (preferred) or CSV file (fallback)."""
    init_db()
    
    # Use cache key from session state to bust cache when needed
    cache_key = st.session_state.get('data_refresh_key', 0)
    return load_data_cached(user_id, cache_key)

def save_transaction(date, type_, category, source, amount, description="", user_id=1):
    """Save transaction to database (preferred) or CSV (fallback)."""
    init_db()
    
    # Try saving to database first
    if database_available():
        try:
            success = save_transaction_to_db(user_id, date, type_, category, source, amount, description)
            if success:
                print(f"✅ Transaction saved to database (user_id={user_id})")
                # Increment cache key to refresh data
                current_key = st.session_state.get('data_refresh_key', 0)
                st.session_state['data_refresh_key'] = current_key + 1
                # Clear the cache to force reload
                load_data_cached.clear()
                return True
            else:
                print(f"⚠️ Database save failed, falling back to CSV")
        except Exception as e:
            print(f"❌ Database error: {e}, falling back to CSV")
    else:
        print("⚠️ Database not available, using CSV")
    
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
    print(f"💾 Transaction saved to CSV")
    
    # Increment cache key to refresh data
    current_key = st.session_state.get('data_refresh_key', 0)
    st.session_state['data_refresh_key'] = current_key + 1
    # Clear the cache to force reload
    load_data_cached.clear()
    
    return True
