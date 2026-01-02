"""
Data loader - simple wrapper around database
"""
import pandas as pd
import streamlit as st
from logic.database import load_transactions, save_transaction, test_connection

def load_data(user_id=1):
    """Load transactions for a user"""
    print(f"🔄 load_data called for user_id={user_id}")
    df = load_transactions(user_id)
    print(f"📊 load_data returning {len(df)} rows")
    return df

def save_data(user_id, date, trans_type, category, source, amount, description=""):
    """Save a transaction"""
    return save_transaction(user_id, date, trans_type, category, source, amount, description)

def check_database():
    """Check if database is available"""
    connected, message = test_connection()
    if connected:
        print(f"✅ Database check: {message}")
    else:
        print(f"❌ Database check: {message}")
    return connected
