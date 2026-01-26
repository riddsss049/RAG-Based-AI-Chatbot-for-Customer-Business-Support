from fastapi import APIRouter
from app.models.lead_model import Lead
from app.services.firebase_service import save_lead

router = APIRouter()

@router.post("/")
async def save_user_lead(data: Lead):
    save_lead(data.dict())
    return {"message": "Lead saved"}
