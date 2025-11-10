# Rutas/publico_objetivo.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/PublicoObjetivo", tags=["Publico Objetivo"])

@router.post("/", response_model=esquemas.PublicoObjetivoLeer)
def crear_publico_objetivo(
    publico: esquemas.PublicoObjetivoCrear, 
    session: Session = Depends(get_session)
):
    return servicios.create_publico_objetivo(session=session, publico_create=publico)

@router.get("/", response_model=List[esquemas.PublicoObjetivoLeer])
def leer_publicos_objetivo_todos(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    publicos = servicios.get_publicos_objetivo_todos(session, skip=skip, limit=limit)
    return publicos