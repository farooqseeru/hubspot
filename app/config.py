# app/config.py

import boto3
import json
import os

REGION_NAME = os.getenv("AWS_REGION", "eu-west-2")  # Adjust to your region
SECRET_ID = "flex_backend_core_service"  # The name of your secret in AWS Secrets Manager


def get_secret_dict(secret_id=SECRET_ID) -> dict:
    client = boto3.client("secretsmanager", region_name=REGION_NAME)
    response = client.get_secret_value(SecretId=secret_id)
    return json.loads(response["SecretString"])


def get_auth_credentials():
    """
    Returns (username, password) tuple from AWS Secrets Manager
    """
    secret = get_secret_dict()
    return secret["username"], secret["password"]
