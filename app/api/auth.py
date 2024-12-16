from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    # Placeholder for actual authentication
    if request.username == "demo" and request.password == "demo":
        return {
            "success": True,
            "token": "demo_token"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")
