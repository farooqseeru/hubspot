from fastapi import APIRouter, HTTPException
from app.models.schemas import ContactCreate, ContactResponse
from app.services.hubspot_service import create_hubspot_contact

router = APIRouter()


@router.post("/create_contact", response_model=ContactResponse)
async def create_contact(contact: ContactCreate):
    """
    Create a new HubSpot contact with source tracking.
    """
    response = create_hubspot_contact(contact)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
