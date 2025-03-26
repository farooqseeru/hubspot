# app/routes/hubspot.py

from fastapi import APIRouter, Depends
from app.models.schemas import Customer, TokenData
from app.services.auth import verify_token
from app.services.hubspot_service import store_customer_in_hubspot

router = APIRouter()


@router.post("/customers")
def create_customer(customer: Customer, token_data: TokenData = Depends(verify_token)):
    result = store_customer_in_hubspot(customer)
    return {"message": "Customer stored successfully", "result": result}
