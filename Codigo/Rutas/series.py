# Rutas/series.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Series", tags=["Series"])

@router.post("/", response_model=esquemas.SerieLeer)
def crear_serie(
    serie: esquemas.SerieCrear, 
    session: Session = Depends(get_session)
):
    return servicios.create_serie(session=session, serie_create=serie)

@router.get("/", response_model=List[esquemas.SerieLeer])
def leer_series_todas(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    series = servicios.get_series_todas(session, skip=skip, limit=limit)
    return series