"""
Simple database module - PostgreSQL/Neon only
"""
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import os

def get_db_url():
    """Get database URL from secrets or environment"""
    try:
        return st.secrets.get("database", {}).get("url") or os.environ.get("DATABASE_URL")
    except:
        return os.environ.get("DATABASE_URL")

def get_engine():
    """Create database engine with connection pooling"""
    url = get_db_url()
    if not url:
        return None
    
    # Simple connection pooling
    engine = create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    return engine

def load_transactions(user_id=1):
    """Load all transactions for a user"""
    engine = get_engine()
    if not engine:
        print("❌ No database connection")
        return pd.DataFrame()
    
    try:
        query = """
            SELECT date, type, category, source, amount, description
            FROM transactions
            WHERE user_id = :user_id
            ORDER BY date DESC
        """
        
        print(f"🔍 Loading transactions for user_id={user_id}")
        
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params={"user_id": user_id})
        
        print(f"📊 Found {len(df)} transactions")
        
        if not df.empty:
            # Rename columns to match app format
            df = df.rename(columns={
                'date': 'Date',
                'type': 'Type',
                'category': 'Category',
                'source': 'Source',
                'amount': 'Amount',
                'description': 'Description'
            })
            # Convert date
            df['Date'] = pd.to_datetime(df['Date'])
            print(f"✅ Successfully loaded {len(df)} transactions")
            
        return df
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def save_transaction(user_id, date, trans_type, category, source, amount, description=""):
    """Save a single transaction"""
    engine = get_engine()
    if not engine:
        print("❌ No database connection")
        return False
    
    try:
        query = """
            INSERT INTO transactions (user_id, date, type, category, source, amount, description)
            VALUES (:user_id, :date, :type, :category, :source, :amount, :description)
        """
        
        with engine.connect() as conn:
            conn.execute(
                text(query),
                {
                    "user_id": user_id,
                    "date": date,
                    "type": trans_type,
                    "category": category,
                    "source": source,
                    "amount": float(amount),
                    "description": description
                }
            )
            conn.commit()
        
        print(f"✅ Transaction saved: {trans_type} {amount} EGP")
        return True
        
    except Exception as e:
        print(f"❌ Save error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection():
    """Test database connection"""
    engine = get_engine()
    if not engine:
        return False, "No database URL configured"
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return True, "Connected successfully"
    except Exception as e:
        return False, str(e)
