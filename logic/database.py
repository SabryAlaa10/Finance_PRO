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

def get_engine():
    """Create SQLAlchemy engine with connection pooling"""
    db_url = get_database_url()
    if db_url:
        # Use connection pooling for better performance
        return create_engine(
            db_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Check connection health before using
            pool_recycle=3600,   # Recycle connections after 1 hour
            connect_args={
                'connect_timeout': 5,  # Shorter timeout
                'options': '-c statement_timeout=10000'  # 10 second query timeout
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
    """Load transactions from PostgreSQL"""
    engine = get_engine()
    if not engine:
        return None
    
    try:
        query = """
            SELECT date, type, category, source, amount, description
            FROM transactions
            WHERE user_id = %(user_id)s
            ORDER BY date DESC
        """
        df = pd.read_sql(query, engine, params={"user_id": user_id})
        if not df.empty:
            df['Date'] = pd.to_datetime(df['date'])
            df['Type'] = df['type']
            df['Category'] = df['category']
            df['Source'] = df['source']
            df['Amount'] = df['amount']
            df['Description'] = df['description']
            df = df[['Date', 'Type', 'Category', 'Source', 'Amount', 'Description']]
        return df
    except Exception as e:
        print(f"Error loading from database: {e}")
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
    return get_database_url() is not None
