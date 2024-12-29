import boto3
import json
import os
import base64
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# Define the base for the ORM models
Base = declarative_base()

load_dotenv()

def get_db_credentials(secret_name: str, region_name: str):
    """
    Retrieve database credentials from AWS Secrets Manager.
    """
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)
    
    # Retrieve the secret value
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        credentials = json.loads(secret)
        return credentials
    except Exception as e:
        raise Exception(f"Failed to retrieve secrets: {str(e)}")


def get_db_engine():
    secret_name = os.getenv("RDS_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")

    # Retrieve credentials
    credentials = get_db_credentials(secret_name, region_name)
    
    # Extract values
    username = credentials["username"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    database = credentials["dbname"]

    database_engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
    print("RDS connection successful!")
    
    return database_engine


def get_redshift_engine():
    secret_name = os.getenv("RS_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")

    # Retrieve credentials
    credentials = get_db_credentials(secret_name, region_name)

    # Extract values
    username = credentials["username"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    database = credentials["database"]

    url = URL.create(
        drivername='redshift+psycopg2',
        host=host, 
        port=port,
        database=database,
        username=username,
        password=password
        )

    #redshift_client = boto3.client('redshift-serverless', region_name=region_name)

    rs_engine = create_engine(url)
    print("Redshift connection successful!")
    return rs_engine
