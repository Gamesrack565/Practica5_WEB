#Series

#Modulos y librerias
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Series", tags=["Series"])

#Define el endpoint POST en la raiz (/Series/), especificando el modelo de respuesta.
@router.post("/", response_model=esquemas.SerieLeer)
#Define la funcion para crear una serie.
def crear_serie(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'SerieCrear'.
    serie: esquemas.SerieCrear, 
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion al modulo de 'servicios'.
    return servicios.create_serie(session=session, serie_create=serie)

#Define el endpoint GET en la raiz (/Series/), respondiendo con una lista de series.
@router.get("/", response_model=List[esquemas.SerieLeer])
#Define la funcion para leer todas las series.
def leer_series_todas(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de series, pasando la paginacion.
    series = servicios.get_series_todas(session, skip=skip, limit=limit)
    #Devuelve la lista de series encontrada.
    return series