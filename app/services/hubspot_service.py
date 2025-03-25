import requests
import logging
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HUBSPOT_API_URL = settings.HUBSPOT_API_URL

HEADERS = {
    "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

VALID_SOURCES = {
    "direct": "DIRECT_TRAFFIC",
    "organic_search": "ORGANIC_SEARCH",
    "paid_search": "PAID_SEARCH",
    "email": "EMAIL_MARKETING",
    "social_media": "SOCIAL_MEDIA",
    "referral": "REFERRALS",
    "campaign": "OTHER_CAMPAIGNS",
    "offline": "OFFLINE",
    "paid_social": "PAID_SOCIAL"
}

def create_hubspot_contact(contact_data):
    """
    Create a new contact in HubSpot with traffic source tracking.
    """
    # Ensure the source is valid; default to "OTHER_CAMPAIGNS" if not
    traffic_source = VALID_SOURCES.get(contact_data.source.lower(), "DIRECT_TRAFFIC")

    data = {
        "properties": {
            "email": contact_data.email,
            "firstname": contact_data.first_name,
            "lastname": contact_data.last_name,
            "hs_analytics_source": traffic_source  # ✅ Now using Original Traffic Source
        }
    }

    response = requests.post(HUBSPOT_API_URL, headers=HEADERS, json=data)

    if response.status_code == 201:
        contact_id = response.json()["id"]
        logger.info(f" Contact {contact_data.email} created successfully in HubSpot.")
        return {"contact_id": contact_id, "email": contact_data.email, "status": "Created"}

    logger.error(f" Error creating contact: {response.json()}")
    return {"error": response.json()}