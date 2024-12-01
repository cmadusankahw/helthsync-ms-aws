import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the base for the ORM models
Base = declarative_base()

def get_db_credentials(secret_name: str, region_name: str):
    """
    Retrieve database credentials from AWS Secrets Manager.
    """
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)
    
    # Retrieve the secret value
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        credentials = json.loads(secret)
        return credentials
    except Exception as e:
        raise Exception(f"Failed to retrieve secrets: {str(e)}")

# Database connection function
def get_database_url():
    """
    Build the database URL using credentials from Secrets Manager.
    """
    secret_name = "my-db-secret"
    region_name = "ap-south-1" 

    # Retrieve credentials
    credentials = get_db_credentials(secret_name, region_name)
    
    # Extract values
    username = credentials["username"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    database = credentials["dbname"]
    
    # Build the database URL
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"

# SQLAlchemy session setup
def get_engine():
    """
    Create and return a SQLAlchemy engine.
    """
    database_url = get_database_url()
    return create_engine(database_url)

def get_session():
    """
    Create a new session and return it.
    """
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Dependency for FastAPI endpoints
def get_db():
    """
    Dependency to provide a database session.
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()
    
# Create a SQLAlchemy engine
engine = create_engine(get_database_url())