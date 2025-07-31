from fastapi import APIRouter, Depends
from app.models.models import User
from app.api.deps import get_current_user

router = APIRouter(tags=["Users"])

@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at
        },
        "stats": {
            "total_clients": len(current_user.clients) if current_user.clients else 0,
            "total_simulations": len(current_user.simulations) if current_user.simulations else 0
        }
    }