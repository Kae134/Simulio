from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import logging

from app.models.database import get_db
from app.models.models import User
from app.api.core.config import settings
from app.api.schemas.auth import Token, UserCreate, UserResponse
from app.api.deps import get_current_user

router = APIRouter(tags=["Auth"])
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Erreur lors de la création du token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération du token"
        )

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    
    if not user:
        return None
        
    if not verify_password(password, user.password_hash):
        return None
        
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}, 
            expires_delta=access_token_expires
        )
        
        logger.info(f"Connexion réussie pour l'utilisateur: {user.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@router.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        email = user_data.email.lower().strip()
        
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Un compte avec cet email existe déjà"
            )
        
        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le mot de passe doit contenir au moins 8 caractères"
            )
        
        hashed_password = hash_password(user_data.password)
        user = User(
            email=email,
            password_hash=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Nouveau compte créé: {user.email}")
        
        return {
            "message": "Compte créé avec succès",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'inscription: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du compte"
        )

@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    try:
        return {
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "created_at": current_user.created_at
            },
            "statistics": {
                "total_clients": len(current_user.clients) if current_user.clients else 0,
                "total_simulations": len(current_user.simulations) if current_user.simulations else 0
            }
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du profil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des informations"
        )