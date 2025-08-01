from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import logging
import re

from app.api.deps import get_current_user, get_pagination_params, PaginationParams, get_user_client
from app.models.database import get_db
from app.models.models import User, Client, Simulation
from app.api.schemas.client import ClientCreate, ClientResponse, ClientUpdate


router = APIRouter(tags=["Clients"])
logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    if not phone:
        return True
    
    clean_phone = re.sub(r'[\s\.\-]', '', phone)
    
    pattern = r'^0[1-9][0-9]{8}$'
    return re.match(pattern, clean_phone) is not None

@router.post("/create", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not client_data.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nom du client ne peut pas être vide"
            )
        
        email = client_data.email.lower().strip()
        if not validate_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format d'email invalide"
            )
        
        if client_data.phone and not validate_phone(client_data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format de téléphone invalide (format français attendu)"
            )
        
        existing_client = db.query(Client).filter(
            Client.email == email,
            Client.user_id == current_user.id
        ).first()
        
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Un client avec cet email existe déjà"
            )
        
        new_client = Client(
            name=client_data.name.strip(),
            email=email,
            phone=client_data.phone.strip() if client_data.phone else None,
            user_id=current_user.id
        )
        
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        logger.info(f"Nouveau client créé: {new_client.name} ({new_client.email})")
        
        return ClientResponse.model_validate(new_client)
    
    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un client avec cet email existe déjà"
        )
    except Exception as e:
        logger.error(f"Erreur création client: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du client"
        )


@router.get("/", response_model=dict)
async def get_clients_for_simulation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params),
    search: str = Query(None, description="Rechercher par nom ou email"),
    include_stats: bool = Query(True, description="Inclure les statistiques")
):
    try:
        query = db.query(Client).filter(Client.user_id == current_user.id)
        
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                Client.name.ilike(search_term) | 
                Client.email.ilike(search_term)
            )
        
        clients = (
            query
            .order_by(Client.name.asc())
            .offset(pagination.skip)
            .limit(pagination.limit)
            .all()
        )
        
        total = query.count()
        
        clients_data = []
        for client in clients:
            client_info = {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "created_at": client.created_at
            }
            
            if include_stats:
                simulation_count = db.query(Simulation).filter(
                    Simulation.client_id == client.id
                ).count()
                
                last_simulation = db.query(Simulation).filter(
                    Simulation.client_id == client.id
                ).order_by(Simulation.created_at.desc()).first()
                
                client_info["stats"] = {
                    "total_simulations": simulation_count,
                    "last_simulation_date": last_simulation.created_at if last_simulation else None
                }
            
            clients_data.append(client_info)
        
        return {
            "clients": clients_data,
            "pagination": {
                "total": total,
                "skip": pagination.skip,
                "limit": pagination.limit,
                "pages": (total + pagination.limit - 1) // pagination.limit
            },
            "message": "Clients récupérés avec succès" if clients_data else "Aucun client trouvé"
        }
        
    except Exception as e:
        logger.error(f"Erreur récupération clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des clients"
        )

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client: Client = Depends(get_user_client),
):

    try:
        return ClientResponse.model_validate(client)
    except Exception as e:
        logger.error(f"Erreur récupération client {client.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du client"
        )


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_data: ClientUpdate,
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db)
):

    try:
        update_data = client_data.model_dump(exclude_unset=True)
        
        if "name" in update_data and not update_data["name"].strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le nom du client ne peut pas être vide"
            )
        
        if "email" in update_data:
            email = update_data["email"].lower().strip()
            if not validate_email(email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Format d'email invalide"
                )
            
            if email != client.email:
                existing_client = db.query(Client).filter(
                    Client.email == email,
                    Client.user_id == client.user_id,
                    Client.id != client.id
                ).first()
                
                if existing_client:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Un autre client avec cet email existe déjà"
                    )
                    
                update_data["email"] = email
        
        if "phone" in update_data and update_data["phone"]:
            if not validate_phone(update_data["phone"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Format de téléphone invalide"
                )
            update_data["phone"] = update_data["phone"].strip()
        
        for field, value in update_data.items():
            setattr(client, field, value)
        
        db.commit()
        db.refresh(client)
        
        logger.info(f"Client modifié: {client.name} ({client.email})")
        
        return ClientResponse.model_validate(client)
        
    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un client avec cet email existe déjà"
        )
    except Exception as e:
        logger.error(f"Erreur modification client {client.id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la modification du client"
        )

@router.delete("/{client_id}")
async def delete_client(
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db)
):
    try:
        client_name = client.name
        
        simulations_count = db.query(Simulation).filter(
            Simulation.client_id == client.id
        ).count()
        
        if simulations_count > 0:
            db.query(Simulation).filter(Simulation.client_id == client.id).delete()
        
        db.delete(client)
        db.commit()
        
        logger.info(f"Client supprimé: {client_name} ({simulations_count} simulations supprimées)")
        
        return {
            "message": "Client supprimé avec succès",
            "deleted_client": client_name,
            "deleted_simulations": simulations_count
        }
        
    except Exception as e:
        logger.error(f"Erreur suppression client {client.id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression du client"
        )

@router.get("/{client_id}/simulations", response_model=dict)
async def get_client_simulations(
    client: Client = Depends(get_user_client),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params)
):

    try:
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
        
        simulations_data = []
        total_capital = 0
        
        for simulation in simulations:
            capital = simulation.data.get('C2', 0) if simulation.data else 0
            total_capital += capital
            
            sim_data = {
                "id": simulation.id,
                "data": simulation.data,
                "result": simulation.result,
                "created_at": simulation.created_at,
                "summary": {
                    "mensualite": simulation.result.get('mensualite', 0) if simulation.result else 0,
                    "capital": capital,
                    "duree_annees": simulation.data.get('N', 0) if simulation.data else 0,
                    "taux": simulation.data.get('T', 0) if simulation.data else 0
                }
            }
            simulations_data.append(sim_data)
        
        average_capital = total_capital / max(len(simulations_data), 1)
        
        return {
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "created_at": client.created_at
            },
            "simulations": simulations_data,
            "pagination": {
                "total": total,
                "skip": pagination.skip,
                "limit": pagination.limit,
                "pages": (total + pagination.limit - 1) // pagination.limit
            },
            "statistics": {
                "total_simulations": total,
                "average_capital": round(average_capital, 2),
                "total_capital": total_capital,
                "last_simulation": simulations_data[0]["created_at"] if simulations_data else None
            }
        }
        
    except Exception as e:
        logger.error(f"Erreur récupération simulations client {client.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des simulations"
        )