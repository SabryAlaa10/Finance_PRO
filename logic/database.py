"""
Database module for PostgreSQL integration
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import streamlit as st

def get_database_url():
    """Get database URL from Streamlit secrets or environment variable"""
    try:
        # Try Streamlit secrets first (for Cloud deployment)
        if hasattr(st, 'secrets') and 'database' in st.secrets:
            return st.secrets['database']['url']
    except:
        pass
    
    # Try environment variable
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Fix for Heroku-style URLs
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url
    
    return None

@st.cache_resource
def get_engine():
    """Create SQLAlchemy engine with connection pooling (cached as singleton)"""
    db_url = get_database_url()
    if db_url:
        # Use connection pooling for better performance
        return create_engine(
            db_url,
            pool_size=10,           # Increased pool size
            max_overflow=20,        # Increased overflow
            pool_pre_ping=True,     # Check connection health before using
            pool_recycle=1800,      # Recycle connections after 30 minutes
            pool_timeout=10,        # Wait max 10 seconds for connection
            echo=False,             # Disable SQL logging for better performance
            connect_args={
                'connect_timeout': 3,  # Faster timeout
                'options': '-c statement_timeout=5000'  # 5 second query timeout
            }
        )
    return None

def init_database():
    """Initialize database tables"""
    engine = get_engine()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            # Create users table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create transactions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    date DATE NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    category VARCHAR(100),
                    source VARCHAR(100),
                    amount DECIMAL(15, 2) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create index on user_id and date for faster queries
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
                ON transactions(user_id, date)
            """))
            
            conn.commit()
            
            # Insert default user if not exists (separate transaction)
            result = conn.execute(text("SELECT id FROM users WHERE username = :username"),
                                {"username": "saleh"})
            if result.fetchone() is None:
                conn.execute(text("""
                    INSERT INTO users (username, password) 
                    VALUES (:username, :password)
                """), {"username": "saleh", "password": "saleh109"})
                conn.commit()
        
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

def load_transactions_from_db(user_id=1):
    """Load transactions from PostgreSQL with optimized query"""
    engine = get_engine()
    if not engine:
        print("❌ No database engine available")
        return None
    
    try:
        print(f"🔍 Querying database for user_id={user_id}")
        
        # First, check what's in the database (debug)
        debug_query = "SELECT COUNT(*) as total FROM transactions"
        debug_df = pd.read_sql_query(debug_query, engine)
        print(f"📊 Total transactions in DB (all users): {debug_df['total'].iloc[0]}")
        
        # Check transactions per user
        users_query = "SELECT user_id, COUNT(*) as count FROM transactions GROUP BY user_id"
        users_df = pd.read_sql_query(users_query, engine)
        print(f"👥 Transactions by user_id:\n{users_df.to_string()}")
        
        # Now query for specific user
        query = """
            SELECT date, type, category, source, amount, description
            FROM transactions
            WHERE user_id = %(user_id)s
            ORDER BY date DESC
        """
        # Use read_sql_query instead of read_sql for better performance
        df = pd.read_sql_query(query, engine, params={"user_id": user_id})
        
        print(f"📊 Database returned {len(df)} rows for user_id={user_id}")
        
        if not df.empty:
            print(f"📋 Columns from DB: {df.columns.tolist()}")
            print(f"🔢 First row: {df.iloc[0].to_dict() if len(df) > 0 else 'N/A'}")
            
            # Convert columns in bulk
            df = df.rename(columns={
                'date': 'Date',
                'type': 'Type',
                'category': 'Category',
                'source': 'Source',
                'amount': 'Amount',
                'description': 'Description'
            })
            # Convert date column efficiently
            df['Date'] = pd.to_datetime(df['Date'])
            
            print(f"✅ Successfully loaded and formatted {len(df)} transactions")
            return df
        else:
            print(f"⚠️ Query returned empty DataFrame for user_id={user_id}")
            print(f"💡 Tip: Check if transactions have correct user_id in database")
            return df
            
    except Exception as e:
        print(f"❌ Error loading from database: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_transaction_to_db(user_id, date, type_, category, source, amount, description=""):
    """Save transaction to PostgreSQL with optimized connection handling"""
    engine = get_engine()
    if not engine:
        return False
    
    try:
        # Use connection context manager for automatic cleanup
        with engine.begin() as conn:  # begin() handles commit automatically
            conn.execute(text("""
                INSERT INTO transactions (user_id, date, type, category, source, amount, description)
                VALUES (:user_id, :date, :type, :category, :source, :amount, :description)
            """), {
                "user_id": user_id,
                "date": date,
                "type": type_,
                "category": category,
                "source": source,
                "amount": float(amount),
                "description": description
            })
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def verify_user(username, password):
    """Verify user credentials"""
    engine = get_engine()
    if not engine:
        return None
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id FROM users WHERE username = :username AND password = :password"),
                {"username": username, "password": password}
            )
            row = result.fetchone()
            return row[0] if row else None
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

def database_available():
    """Check if database is available"""
    db_url = get_database_url()
    available = db_url is not None
    if available:
        print(f"✅ Database URL configured: {db_url[:30]}...")
    else:
        print("❌ No database URL found")
    return available
