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

@st.cache_data(ttl=60, show_spinner=False)  # Cache for 1 minute only for faster updates
def load_data_cached(user_id=1, cache_key=None):
    """Load transactions with caching - ONLY from database."""
    print(f"🔄 Loading data for user_id={user_id}, cache_key={cache_key}")
    
    # ONLY database - no CSV fallback
    if not database_available():
        print("❌ Database not configured!")
        return pd.DataFrame(columns=COLUMNS)
    
    try:
        df = load_transactions_from_db(user_id)
        if df is not None:
            print(f"✅ Loaded {len(df)} transactions from Neon database")
            return df
        else:
            print(f"⚠️ Database query returned None")
            return pd.DataFrame(columns=COLUMNS)
    except Exception as e:
        print(f"❌ Database load error: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame(columns=COLUMNS)

def load_data(user_id=1) -> pd.DataFrame:
    """Load transactions from database (preferred) or CSV file (fallback)."""
    init_db()
    
    # Use cache key from session state to bust cache when needed
    cache_key = st.session_state.get('data_refresh_key', 0)
    return load_data_cached(user_id, cache_key)

def save_transaction(date, type_, category, source, amount, description="", user_id=1):
    """Save transaction - ONLY to database (Neon)."""
    init_db()
    
    # Database ONLY - no CSV fallback
    if not database_available():
        print("❌ Database not configured! Cannot save transaction.")
        return False
    
    try:
        print(f"💾 Saving transaction to Neon database (user_id={user_id})")
        success = save_transaction_to_db(user_id, date, type_, category, source, amount, description)
        
        if success:
            print(f"✅ Transaction saved successfully to Neon database")
            # Increment cache key to refresh data
            current_key = st.session_state.get('data_refresh_key', 0)
            st.session_state['data_refresh_key'] = current_key + 1
            # Clear the cache to force reload
            load_data_cached.clear()
            return True
        else:
            print(f"❌ Failed to save transaction to database")
            return False
            
    except Exception as e:
        print(f"❌ Database save error: {e}")
        import traceback
        traceback.print_exc()
        return False
