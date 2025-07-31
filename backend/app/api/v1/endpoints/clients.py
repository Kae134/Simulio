from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.api.deps import get_current_user, get_pagination_params, PaginationParams, get_user_client
from app.models.database import get_db
from app.models.models import User, Client, Simulation
from app.api.schemas.client import ClientCreate, ClientResponse, ClientUpdate, ClientWithStats

router = APIRouter(tags=["Clients"])
logger = logging.getLogger(__name__)

@router.post("/create", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        existing_client = db.query(Client).filter(
            Client.email == client_data.email,
            Client.user_id == current_user.id
        ).first()
        
        if existing_client:
            raise HTTPException(
                status_code=400,
                detail="Un client avec cet email existe déjà"
            )
        
        new_client = Client(
            name=client_data.name,
            email=client_data.email,
            phone=client_data.phone,
            user_id=current_user.id
        )
        
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        return ClientResponse(
            id=new_client.id,
            name=new_client.name,
            email=new_client.email,
            phone=new_client.phone,
            user_id=new_client.user_id,
            created_at=new_client.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur création client: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création du client: {str(e)}"
        )

@router.get("/", response_model=dict)
async def get_clients_for_simulation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clients = (
        db.query(Client)
        .filter(Client.user_id == current_user.id)
        .order_by(Client.name.asc())  # Tri alphabétique pour UX
        .all()
    )
    
    clients_data = []
    for client in clients:
        simulation_count = db.query(Simulation).filter(
            Simulation.client_id == client.id
        ).count()
        
        last_simulation = db.query(Simulation).filter(
            Simulation.client_id == client.id
        ).order_by(Simulation.created_at.desc()).first()
        
        clients_data.append({
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "stats": {
                "total_simulations": simulation_count,
                "last_simulation_date": last_simulation.created_at if last_simulation else None
            }
        })
    
    return {
        "clients": clients_data,
        "total": len(clients_data),
        "message": "Sélectionnez un client pour enregistrer la simulation" if clients_data else "Aucun client trouvé. Créez d'abord un client."
    }

@router.get("/{client_id}/debug")
async def debug_client(
    client: Client = Depends(get_user_client),
):

    return {
        "raw_data": {
            "id": client.id,
            "name": repr(client.name),
            "email": repr(client.email),
            "phone": repr(client.phone),
            "user_id": client.user_id,
            "created_at": client.created_at
        },
        "data_types": {
            "id": type(client.id).__name__,
            "name": type(client.name).__name__,
            "email": type(client.email).__name__,
            "phone": type(client.phone).__name__,
            "user_id": type(client.user_id).__name__,
            "created_at": type(client.created_at).__name__
        }
    }

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client: Client = Depends(get_user_client),
):

    try:
        return ClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            user_id=client.user_id,
            created_at=client.created_at
        )
    except Exception as e:
        logger.error(f"Erreur récupération client: {str(e)}")
        logger.error(f"Client data: id={client.id}, name={client.name}, email={client.email}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du client: {str(e)}"
        )

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_data: ClientUpdate,  # Changé vers ClientUpdate
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db)
):

    try:
        if client_data.email and client_data.email != client.email:
            existing_client = db.query(Client).filter(
                Client.email == client_data.email,
                Client.user_id == client.user_id,
                Client.id != client.id
            ).first()
            
            if existing_client:
                raise HTTPException(
                    status_code=400,
                    detail="Un autre client avec cet email existe déjà"
                )
        
        update_data = client_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)
        
        db.commit()
        db.refresh(client)
        
        return ClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            user_id=client.user_id,
            created_at=client.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur mise à jour client: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )

@router.delete("/{client_id}")
async def delete_client(
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db)
):
    try:
        db.delete(client)
        db.commit()
        
        return {"message": "Client supprimé avec succès"}
        
    except Exception as e:
        logger.error(f"Erreur suppression client: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )

@router.get("/{client_id}/simulations", response_model=dict)
async def get_client_simulations(
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params)
):

    query = db.query(Simulation).filter(
        Simulation.client_id == client.id,
        Simulation.user_id == client.user_id
    )
    
    simulations = (
        query
        .order_by(Simulation.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )
    
    total = query.count()
    
    from app.api.schemas.simulation import SimulationResponse
    
    simulations_data = []
    for s in simulations:
        sim_data = {
            "id": s.id,
            "data": s.data,
            "result": s.result,
            "created_at": s.created_at,
            "client_id": s.client_id,
            "summary": {
                "mensualite": s.result.get('mensualite', 0) if s.result else 0,
                "capital": s.data.get('C2', 0) if s.data else 0,
                "duree_annees": s.data.get('N', 0) if s.data else 0,
                "taux": s.data.get('T', 0) if s.data else 0
            }
        }
        simulations_data.append(sim_data)
    
    return {
        "client": {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "created_at": client.created_at
        },
        "simulations": simulations_data,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
        "stats": {
            "total_simulations": total,
            "average_capital": sum([s.data.get('C2', 0) for s in simulations if s.data]) / max(len(simulations), 1),
            "last_simulation": simulations[0].created_at if simulations else None
        }
    }