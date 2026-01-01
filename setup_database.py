"""
Setup script to initialize the database
Run this once after creating your database on Neon
"""
from logic.database import init_database, database_available

print("=" * 60)
print("Finance PRO - Database Setup")
print("=" * 60)

if not database_available():
    print("\n❌ Database URL not found!")
    print("\nPlease set up your database URL in one of these ways:")
    print("1. Create .streamlit/secrets.toml with [database] url = 'your_url'")
    print("2. Set DATABASE_URL environment variable")
    print("\nGet a free PostgreSQL database from:")
    print("- Neon.tech: https://neon.tech (Recommended)")
    print("- Supabase: https://supabase.com")
    print("- Railway: https://railway.app")
    exit(1)

print("\n🔄 Initializing database...")
success = init_database()

if success:
    print("\n✅ Database initialized successfully!")
    print("\nCreated tables:")
    print("  - users (for authentication)")
    print("  - transactions (for financial data)")
    print("\nDefault user created:")
    print("  Username: saleh")
    print("  Password: saleh109")
    print("\n✨ You're ready to go!")
else:
    print("\n❌ Database initialization failed!")
    print("Please check your database connection and try again.")

print("\n" + "=" * 60)
