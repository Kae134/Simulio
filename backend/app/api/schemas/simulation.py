from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, Dict, Any
from datetime import datetime

class SimulationBase(BaseModel):
    N: int = Field(..., gt=0, le=50, description="Durée en années")
    C2: float = Field(..., gt=0, description="Montant du capital")
    T: float = Field(..., ge=0, le=20, description="Taux d'intérêt en %")
    ASSU: float = Field(..., ge=0, le=5, description="Taux d'assurance en %")
    apport: float = Field(..., ge=0, description="Apport personnel")
    mois: Literal["01","02","03","04","05","06","07","08","09","10","11","12"] = Field(
        ..., description="Mois au format 'MM'"
    )
    annee: str = Field(..., pattern=r"^\d{4}$", description="Année au format 'YYYY'")
    fraisAgence: float = Field(..., ge=0, le=20, description="Frais d'agence en %")
    fraisNotaire: float = Field(..., ge=0, le=10, description="Frais de notaire en %")
    TRAVAUX: float = Field(..., ge=0, description="Montant des travaux")
    revalorisationBien: float = Field(..., ge=-10, le=20, description="Taux de revalorisation du bien en %")
    
    @validator('C2', 'apport', 'TRAVAUX')
    def validate_positive_amounts(cls, v):
        if v < 0:
            raise ValueError('Les montants ne peuvent pas être négatifs')
        return v
    
    @validator("annee")
    def annee_valide(cls, v):
        year = int(v)
        if year < 1900 or year > 2100:
            raise ValueError("L'année doit être comprise entre 1900 et 2100.")
        return v

class SimulationCreate(SimulationBase):
    """Schema pour créer une simulation (calcul uniquement)"""
    pass

class SimulationSaveWithResult(BaseModel):
    """
    Nouveau schéma pour sauvegarder une simulation avec résultats pré-calculés
    """
    simulation_data: SimulationCreate
    result: Dict[str, Any]  # Résultats pré-calculés de l'algorithme
    client_id: Optional[int] = None

class SimulationResponse(BaseModel):
    id: int
    data: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    created_at: datetime
    client_id: Optional[int]
    
    class Config:
        from_attributes = True

class SimulationListResponse(BaseModel):
    simulations: list[SimulationResponse]
    total: int
    skip: int
    limit: int