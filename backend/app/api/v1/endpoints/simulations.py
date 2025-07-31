from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.api.deps import get_current_user, get_pagination_params, PaginationParams, get_user_client
from app.models.database import get_db
from app.models.models import User, Client, Simulation
from app.api.schemas.simulation import SimulationCreate, SimulationResponse, SimulationSaveWithResult
from app.services.algo import CalculerMensualite39_bis2_ANCIEN

router = APIRouter(tags=["Simulations"])
logger = logging.getLogger(__name__)

@router.post("/simulate", response_model=dict)
async def simulate(
    data: SimulationCreate, 
    current_user: User = Depends(get_current_user)
):

    try:
        result = CalculerMensualite39_bis2_ANCIEN(
            N=data.N,
            C2=data.C2,
            T=data.T,
            ASSU=data.ASSU,
            apport=data.apport,
            mois=data.mois,
            annee=data.annee,
            fraisAgence=data.fraisAgence,
            fraisNotaire=data.fraisNotaire,
            TRAVAUX=data.TRAVAUX,
            revalorisationBien=data.revalorisationBien
        )
                
        return {
            "success": True,
            "simulation_data": data.dict(),  
            "result": result, 
            "summary": {
                "mensualite": result.get('mensualite', 0),
                "capital": data.C2,
                "duree_annees": data.N,
                "taux": data.T
            }
        }
        
    except Exception as e:
        logger.error(f"Erreur simulation: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors du calcul: {str(e)}"
        )


@router.get("/", response_model=dict)
async def get_simulations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params),
    client_id: Optional[int] = Query(None, description="Filtrer par client"),
    with_client: bool = Query(False, description="Inclure les informations du client")
):

    query = db.query(Simulation).filter(Simulation.user_id == current_user.id)
    
    if client_id:
        client_exists = db.query(Client).filter(
            Client.id == client_id,
            Client.user_id == current_user.id
        ).first()
        
        if not client_exists:
            raise HTTPException(
                status_code=404,
                detail="Client non trouvé"
            )
            
        query = query.filter(Simulation.client_id == client_id)
    
    simulations = (
        query
        .order_by(Simulation.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )
    
    total = query.count()
    
    response_simulations = []
    for s in simulations:
        sim_data = {
            "id": s.id,
            "data": s.data,
            "result": s.result,
            "created_at": s.created_at,
            "client_id": s.client_id
        }
        
        if with_client and s.client_id:
            client = db.query(Client).filter(Client.id == s.client_id).first()
            if client:
                sim_data["client"] = {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone
                }
        
        response_simulations.append(sim_data)
    
    return {
        "simulations": response_simulations,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }

@router.get("/{simulation_id}", response_model=dict)
async def get_simulation(
    simulation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    with_client: bool = Query(False, description="Inclure les informations du client")
):
    simulation = db.query(Simulation).filter(
        Simulation.id == simulation_id,
        Simulation.user_id == current_user.id
    ).first()
    
    if not simulation:
        raise HTTPException(
            status_code=404,
            detail="Simulation non trouvée"
        )
    
    response_data = {
        "id": simulation.id,
        "data": simulation.data,
        "result": simulation.result,
        "created_at": simulation.created_at,
        "client_id": simulation.client_id
    }
    
    if with_client and simulation.client_id:
        client = db.query(Client).filter(Client.id == simulation.client_id).first()
        if client:
            response_data["client"] = {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone
            }
    
    return response_data

@router.put("/{simulation_id}/assign-client")
async def assign_client_to_simulation(
    simulation_id: int,
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    simulation = db.query(Simulation).filter(
        Simulation.id == simulation_id,
        Simulation.user_id == current_user.id
    ).first()
    
    if not simulation:
        raise HTTPException(
            status_code=404,
            detail="Simulation non trouvée"
        )
    
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.user_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client non trouvé"
        )
    
    try:
        simulation.client_id = client_id
        db.commit()
        
        return {
            "message": "Client associé à la simulation avec succès",
            "simulation_id": simulation_id,
            "client_id": client_id
        }
        
    except Exception as e:
        logger.error(f"Erreur association client-simulation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'association: {str(e)}"
        )

@router.delete("/{simulation_id}")
async def delete_simulation(
    simulation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    simulation = db.query(Simulation).filter(
        Simulation.id == simulation_id,
        Simulation.user_id == current_user.id
    ).first()
    
    if not simulation:
        raise HTTPException(
            status_code=404,
            detail="Simulation non trouvée"
        )
    
    try:
        db.delete(simulation)
        db.commit()
        
        return {"message": "Simulation supprimée avec succès"}
        
    except Exception as e:
        logger.error(f"Erreur suppression simulation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )