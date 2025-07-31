from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.core.config import settings
from app.api.v1.endpoints import auth, clients, simulations, users

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(clients.router, prefix="/api/v1/clients") 
app.include_router(simulations.router, prefix="/api/v1/simulations")
app.include_router(users.router, prefix="/api/v1/users")

@app.get("/")
def read_root():
    return {
        "message": "Simulio API", 
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )