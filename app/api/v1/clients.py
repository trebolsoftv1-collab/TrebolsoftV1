from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.cloudinary import upload_client_photo
from app.models.user import User, RoleType
from app.models.client import Client as ClientModel
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.crud import client as crud_client

router = APIRouter()


@router.get("/count", response_model=dict)
def count_clients(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Devuelve la cantidad total de clientes visibles para el usuario."""
    query = db.query(ClientModel)
    
    if is_active is not None:
        query = query.filter(ClientModel.is_active == is_active)

    # Admin: ve todo
    if current_user.role == RoleType.ADMIN:
        return {"total": query.count()}
    
    # Supervisor: ve clientes de sus cobradores + asignados + propios
    elif current_user.role == RoleType.SUPERVISOR:
        subordinate_ids = crud_client.get_subordinate_collector_ids(db, current_user.id)
        
        # Agregar IDs de usuarios asignados por nombre en assigned_routes
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                subordinate_ids.extend([u.id for u in extra_users])
                
        allowed_ids = subordinate_ids + [current_user.id]
        
        count = query.filter(ClientModel.collector_id.in_(allowed_ids)).count()
        return {"total": count}
    
    # Cobrador: solo sus propios clientes
    else:
        count = query.filter(ClientModel.collector_id == current_user.id).count()
        return {"total": count}


@router.get("/", response_model=List[Client])
def list_clients(
    skip: int = 0,
    limit: int = 100,
    collector_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos los clientes con filtros opcionales."""
    # Admin: ve todo
    if current_user.role == RoleType.ADMIN:
        return crud_client.get_clients(
            db,
            skip=skip,
            limit=limit,
            collector_id=collector_id,
            is_active=is_active
        )
    
    # Supervisor: ve clientes de sus cobradores + sus propios clientes
    elif current_user.role == RoleType.SUPERVISOR:
        subordinate_ids = crud_client.get_subordinate_collector_ids(db, current_user.id)
        # Incluye al supervisor mismo (puede tener clientes propios)
        
        # Agregar IDs de usuarios asignados por nombre en assigned_routes
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                subordinate_ids.extend([u.id for u in extra_users])
                
        allowed_ids = subordinate_ids + [current_user.id]
        
        clients = crud_client.get_clients(
            db,
            skip=0,  # Filtramos después
            limit=10000,  # Traemos todo para filtrar
            is_active=is_active
        )
        # Filtrar solo clientes de cobradores permitidos
        filtered = [c for c in clients if c.collector_id in allowed_ids]
        return filtered[skip:skip+limit]
    
    # Cobrador: solo sus propios clientes
    else:
        return crud_client.get_clients(
            db,
            skip=skip,
            limit=limit,
            collector_id=current_user.id,
            is_active=is_active
        )


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea un nuevo cliente. Acceso para Admin, Supervisor y Cobrador."""
    
    # Lógica de asignación automática y validación por rol
    if current_user.role == RoleType.COLLECTOR:
        client.collector_id = current_user.id
    elif current_user.role == RoleType.SUPERVISOR:
        if not client.collector_id:
            raise HTTPException(status_code=400, detail="Debe asignar un cobrador")
        # Validar que el cobrador sea subordinado
        subordinate_ids = crud_client.get_subordinate_collector_ids(db, current_user.id)
        
        # Agregar IDs de usuarios asignados por nombre
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                subordinate_ids.extend([u.id for u in extra_users])

        if client.collector_id != current_user.id and client.collector_id not in subordinate_ids:
            raise HTTPException(status_code=400, detail="El cobrador no pertenece a su equipo")
    elif current_user.role == RoleType.ADMIN:
        if not client.collector_id:
            raise HTTPException(status_code=400, detail="Debe asignar un cobrador")

    # Verificar si ya existe un cliente con ese DNI
    existing = crud_client.get_client_by_dni(db, client.dni)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client with this DNI already exists"
        )
    
    return crud_client.create_client(db, client)


@router.get("/{client_id}", response_model=Client)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene un cliente por ID."""
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Admin: acceso total
    if current_user.role == RoleType.ADMIN:
        return db_client
    
    # Supervisor: ve clientes de sus cobradores + propios
    elif current_user.role == RoleType.SUPERVISOR:
        subordinate_ids = crud_client.get_subordinate_collector_ids(db, current_user.id)
        
        # Agregar IDs de usuarios asignados por nombre
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                subordinate_ids.extend([u.id for u in extra_users])
                
        allowed_ids = subordinate_ids + [current_user.id]
        
        if db_client.collector_id not in allowed_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return db_client
    
    # Cobrador: solo sus propios clientes
    else:
        if db_client.collector_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return db_client


@router.put("/{client_id}", response_model=Client)
def update_existing_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza un cliente. Requiere rol supervisor o admin."""
    # Reutilizamos la lógica de read_client para verificar permisos de acceso primero
    db_client = read_client(client_id=client_id, db=db, current_user=current_user)

    # Solo Admin y Supervisor pueden actualizar
    if current_user.role not in [RoleType.ADMIN, RoleType.SUPERVISOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this client."
        )

    updated = crud_client.update_client(db, client_id, client)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return updated


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Desactiva un cliente (soft delete). Requiere rol supervisor o admin."""
    # Reutilizamos la lógica de read_client para verificar permisos de acceso primero
    db_client = read_client(client_id=client_id, db=db, current_user=current_user)

    # Solo Admin puede eliminar (Supervisor solo puede editar)
    if current_user.role != RoleType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede eliminar clientes."
        )

    ok = crud_client.delete_client(db, client_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return None


@router.post("/{client_id}/upload-photo", response_model=dict)
async def upload_house_photo(
    client_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload house photo for a client.
    
    - Requires authentication (cobrador can upload for their clients, admin/supervisor for any)
    - Max size: 5MB
    - Allowed formats: JPEG, PNG, WEBP
    - Returns the photo URL
    """
    # Verificar que el cliente existe
    db_client = crud_client.get_client(db, client_id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Verificar permisos
    if current_user.role == RoleType.COLLECTOR and db_client.collector_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload photos for your own clients"
        )
    
    # Upload to Cloudinary
    photo_url = await upload_client_photo(file, client_id)
    
    # Update client record with photo URL
    crud_client.update_client(
        db,
        client_id,
        ClientUpdate(house_photo_url=photo_url)
    )
    
    return {
        "client_id": client_id,
        "photo_url": photo_url,
        "message": "Photo uploaded successfully"
    }
