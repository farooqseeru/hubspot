import os
import requests
from app.models.schemas import Customer
from app.utils.logger import logger
from fastapi import HTTPException

# Best practice: store this in AWS Secrets Manager, not env
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")  # Private App token


def store_customer_in_hubspot(customer: Customer):
    """
    Sends customer data to HubSpot CRM using Bearer auth (Private App Token).
    Docs: https://developers.hubspot.com/docs/api/crm/contacts
    """
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    payload = {
        "properties": {
            "email": customer.email,
            "firstname": customer.name,
            "phone": customer.phone
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"HubSpot API returned error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail="HubSpot API error")
    except Exception as e:
        logger.error(f"Unexpected error while storing customer: {e}")
        raise Exception("Unexpected HubSpot error")
