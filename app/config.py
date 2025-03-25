import os
from dotenv import load_dotenv

import boto3
import json

# Load environment variables
load_dotenv()


class Settings:
    HUBSPOT_API_URL: str = os.getenv("HUBSPOT_API_URL", "https://api.hubapi.com/crm/v3/objects/contacts")
    HUBSPOT_ACCESS_TOKEN: str = os.getenv("HUBSPOT_ACCESS_TOKEN")
    API_PORT: int = int(os.getenv("API_PORT", 8000))


settings = Settings()

AWS_REGION = "eu-west-2"
SECRET_NAME = "rgbrebrnjytuekmfg456thjtghnd"


def get_secret():
    """Retrieve secrets from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=AWS_REGION)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(get_secret_value_response["SecretString"])
    except Exception as e:
        print("Error retrieving secret:", e)
        return {}
