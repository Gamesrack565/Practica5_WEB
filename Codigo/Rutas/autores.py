from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Autores", tags=["Autores"])

# --- Rutas para Autores ---
@router.post("/", response_model=esquemas.AutorLeer)
def crear_autor(
    autor: esquemas.AutorCreacion, 
    session: Session = Depends(get_session)
):
    return servicios.create_autor(session=session, autor_create=autor)


@router.get("/", response_model=List[esquemas.AutorLeer])
def leer_autores(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    autores = servicios.get_autores_todos(session, skip=skip, limit=limit)
    return autores

@router.delete("/{autor_id}", status_code=204)
def eliminar_autor(
    autor_id: int,
    session: Session = Depends(get_session)
):
    db_autor = servicios.get_autor(session, autor_id=autor_id)
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    session.delete(db_autor)
    session.commit()
    return