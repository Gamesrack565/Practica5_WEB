# Rutas/editoriales.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Editoriales", tags=["Editoriales"])

@router.post("/", response_model=esquemas.EditorialLeer)
def crear_editorial(
    editorial: esquemas.EditorialCrear, 
    session: Session = Depends(get_session)
):
    return servicios.create_editorial(session=session, editorial_create=editorial)

@router.get("/", response_model=List[esquemas.EditorialLeer])
def leer_editoriales_todas(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    editoriales = servicios.get_editoriales_todas(session, skip=skip, limit=limit)
    return editoriales


# (Añade esto en Rutas/editoriales.py, junto a tus otras rutas)

@router.patch("/{editorial_id}", response_model=esquemas.EditorialLeer)
def actualizar_editorial_ruta(
    editorial_id: int,
    editorial_update: esquemas.EditorialActualizar,
    session: Session = Depends(get_session)
):
    # 1. Busca la editorial
    db_editorial = servicios.get_editorial(session, editorial_id=editorial_id)
    if not db_editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    # 2. Llama al servicio para que haga la actualización
    return servicios.actualizar_editorial(
        session=session, 
        db_editorial=db_editorial, 
        editorial_update=editorial_update
    )



@router.delete("/{editorial_id}", 
    status_code=204 
)
def eliminar_editorial(
    editorial_id: int,
    session: Session = Depends(get_session)
):
    # 1. Obtenemos la editorial
    db_editorial = servicios.get_editorial(session, editorial_id=editorial_id)
    if not db_editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    # 2. Obtenemos la dirección asociada ANTES de borrar
    db_direccion = db_editorial.direccion

    # 3. Borramos ambos
    session.delete(db_editorial)
    if db_direccion:
        session.delete(db_direccion)
    
    # 4. Guardamos
    session.commit()
    
    # 5. Retornamos None (implícito)
    return