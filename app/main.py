# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.routes import hubspot
from app.services.auth import create_access_token, validate_user
from app.models.schemas import Token

app = FastAPI()


# Auth endpoint
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    validate_user(form_data.username, form_data.password)
    token = create_access_token(
        data={"sub": form_data.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}


# HubSpot routes
app.include_router(hubspot.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
