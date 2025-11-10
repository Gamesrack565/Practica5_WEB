from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Categorias", tags=["Categorias"])

@router.post("/", response_model=esquemas.CategoriaLeer)
def crear_categoria(
    categoria: esquemas.CategoriaCrear, 
    session: Session = Depends(get_session)
):
    return servicios.create_categoria(session=session, categoria_create=categoria)

@router.get("/", response_model=List[esquemas.CategoriaLeer])
def leer_categorias(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    categorias = servicios.get_categorias_todos(session, skip=skip, limit=limit)
    return categorias

@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(
    categoria_id: int,
    session: Session = Depends(get_session)
):
    db_categoria = servicios.get_categoria(session, categoria_id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    session.delete(db_categoria)
    session.commit()
    return
