# Set up the database connection and provide a session to interact with the database.
# Create the SQLAlchemy engine to manage the database connection.
# Create a configured session factory to produce session objects.
# Define a dependency function to provide and close database sessions.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration for RDS PostgreSQL
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "EliteGaming275"
DATABASE_HOST = "booking-db.crguaws8egqt.us-east-2.rds.amazonaws.com"
DATABASE_PORT = "5432"
DATABASE_NAME = "booking-db"

# Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models to inherit from
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
