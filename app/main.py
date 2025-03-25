from fastapi import FastAPI
from app.routes import hubspot

app = FastAPI(title="HubSpot API", version="1.0", description="API for tracking users and storing data in HubSpot")

# Include routes
app.include_router(hubspot.router, prefix="/hubspot", tags=["HubSpot"])


@app.get("/")
async def root():
    return {"message": "HubSpot Tracking API is Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
