from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
import logging

logger = logging.getLogger(__name__)

# Get and normalize DATABASE_URL
database_url = settings.DATABASE_URL

# Fix common issues with DATABASE_URL
# 1. Handle postgres:// vs postgresql:// (Heroku/Render use postgres://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# 2. Remove any accidental 'psql ' prefix or extra quotes
if database_url.startswith("psql "):
    database_url = database_url[5:]
database_url = database_url.strip().strip("'\"")

logger.info(f"Connecting to database...")

# Create database engine
engine = create_engine(
    database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative base for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
