from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Le nom ne peut pas être vide')
        return v.strip()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not v or not v.strip():
            raise ValueError('Le téléphone ne peut pas être vide')
        import re
        phone_clean = re.sub(r'[^\d+]', '', v.strip())
        if not re.match(r'^(?:\+33|0)[1-9](?:[0-9]{8})$', phone_clean):
            raise ValueError('Format de téléphone invalide')
        return phone_clean

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Le nom ne peut pas être vide')
        return v.strip() if v else v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Le téléphone ne peut pas être vide')
            import re
            phone_clean = re.sub(r'[^\d+]', '', v.strip())
            if not re.match(r'^(?:\+33|0)[1-9](?:[0-9]{8})$', phone_clean):
                raise ValueError('Format de téléphone invalide')
            return phone_clean
        return v

class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime

class ClientWithStats(ClientResponse):
    total_simulations: int = 0
    last_simulation_date: Optional[datetime] = None