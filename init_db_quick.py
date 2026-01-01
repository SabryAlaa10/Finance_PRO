"""
Quick database initialization script
"""
import os
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_7zCUmphky2uG@ep-odd-salad-agm5mb2r-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require"

from sqlalchemy import create_engine, text

# Create engine
engine = create_engine(os.environ['DATABASE_URL'])

print("=" * 60)
print("Creating database tables...")
print("=" * 60)

try:
    with engine.connect() as conn:
        # Create users table
        print("\n1. Creating users table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✅ Users table created")
        
        # Create transactions table
        print("\n2. Creating transactions table...")
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
        print("✅ Transactions table created")
        
        # Create index
        print("\n3. Creating index...")
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
            ON transactions(user_id, date)
        """))
        print("✅ Index created")
        
        # Insert default user
        print("\n4. Creating default user...")
        result = conn.execute(text("SELECT id FROM users WHERE username = 'saleh'"))
        if result.fetchone() is None:
            conn.execute(text("""
                INSERT INTO users (username, password) 
                VALUES ('saleh', 'saleh109')
            """))
            print("✅ Default user created (saleh / saleh109)")
        else:
            print("✅ Default user already exists")
        
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Database initialized successfully!")
        print("=" * 60)
        print("\nYou can now login with:")
        print("  Username: saleh")
        print("  Password: saleh109")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
