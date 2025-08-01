from fastapi import APIRouter

from app.api.v1.endpoints import auth, clients, simulations, users

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(users.router, tags=["Users"])  
api_router.include_router(clients.router, tags=["Clients"])
api_router.include_router(simulations.router, tags=["Simulations"])