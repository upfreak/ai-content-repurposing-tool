import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/content_repurpose')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()
try:
    result = db.execute("SELECT id, email, username, created_at, is_active FROM users ORDER BY id")
    users = result.fetchall()
    
    print(f"\n=== Total users in database: {len(users)} ===\n")
    
    for user in users:
        print(f"ID: {user[0]}")
        print(f"Email: {user[1]}")
        print(f"Username: {user[2]}")
        print(f"Created: {user[3]}")
        print(f"Active: {user[4]}")
        print("-" * 50)
            
finally:
    db.close()

