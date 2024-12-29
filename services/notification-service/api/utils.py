import boto3
import json
import os
import base64
from dotenv import load_dotenv
import smtplib

load_dotenv()

def get_smtp_credentials():
    """
    Retrieve SMTP credentials from AWS Secrets Manager.
    """
    secret_name = os.getenv("AWS_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")
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


def send_email(to_email: str, subject: str, body: str):
    ses_credentials = get_smtp_credentials()
    smtp_username = ses_credentials["SMTP_user"]
    smtp_password = ses_credentials["SMTP_password"]
    smtp_host = ses_credentials["SMTP_host"]
    smtp_port = ses_credentials["SMTP_port"]

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(smtp_username, to_email, message)

    print(f"Email sent to {to_email}")

