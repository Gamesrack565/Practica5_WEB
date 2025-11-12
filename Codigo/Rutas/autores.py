#Auores: Rutas para gestionar autores en la aplicacion FastAPI.

#Modulo y librerias
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session


router = APIRouter(prefix="/Autores", tags=["Autores"])

# --- Rutas para Autores ---
#Define el endpoint POST en la raiz (/Autores/), especificando el modelo de respuesta.
@router.post("/", response_model=esquemas.AutorLeer)
#Define la funcion para crear un autor.
def crear_autor(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'AutorCreacion'.
    autor: esquemas.AutorCreacion, 
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion al modulo de 'servicios' y devuelve el resultado.
    return servicios.create_autor(session=session, autor_create=autor)


#Define el endpoint GET en la raiz (/Autores/), respondiendo con una lista de autores.
@router.get("/", response_model=List[esquemas.AutorLeer])
#Define la funcion para leer todos los autores.
def leer_autores(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de autores, pasando la paginacion.
    autores = servicios.get_autores_todos(session, skip=skip, limit=limit)
    #Devuelve la lista de autores encontrada.
    return autores

#Define el endpoint DELETE para un autor especifico, esperando un codigo 204 (No Content) al exito.
@router.delete("/{autor_id}", status_code=204)
#Define la funcion para eliminar un autor.
def eliminar_autor(
    #Recibe el 'autor_id' desde la ruta (path parameter).
    autor_id: int,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session)
):
    #Llama al servicio para obtener el autor por su ID.
    db_autor = servicios.get_autor(session, autor_id=autor_id)
    #Si el autor no se encuentra (devuelve None).
    if not db_autor:
        #Lanza un error HTTP 404 (No Encontrado).
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    #Marca el objeto 'db_autor' para ser eliminado.
    session.delete(db_autor)
    #Confirma (guarda) la eliminacion en la base de datos.
    session.commit()
    #Devuelve la respuesta (automaticamente sera 204 No Content, como se definio).
    return