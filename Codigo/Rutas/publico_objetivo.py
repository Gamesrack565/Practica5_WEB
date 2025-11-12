#Publico objetivo

#Modulos y librerias
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/PublicoObjetivo", tags=["Publico Objetivo"])

#Define el endpoint POST en la raiz (/PublicoObjetivo/), especificando el modelo de respuesta.
@router.post("/", response_model=esquemas.PublicoObjetivoLeer)
#Define la funcion para crear un tipo de publico objetivo.
def crear_publico_objetivo(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'PublicoObjetivoCrear'.
    publico: esquemas.PublicoObjetivoCrear, 
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion al modulo de 'servicios'.
    return servicios.create_publico_objetivo(session=session, publico_create=publico)

#Define el endpoint GET en la raiz (/PublicoObjetivo/), respondiendo con una lista.
@router.get("/", response_model=List[esquemas.PublicoObjetivoLeer])
#Define la funcion para leer todos los tipos de publico.
def leer_publicos_objetivo_todos(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de publicos, pasando la paginacion.
    publicos = servicios.get_publicos_objetivo_todos(session, skip=skip, limit=limit)
    #Devuelve la lista de publicos encontrada.
    return publicos