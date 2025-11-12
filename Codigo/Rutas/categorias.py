#Categorias: Rutas para gestionar categorias de libros

#Modulos y librerias
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session


router = APIRouter(prefix="/Categorias", tags=["Categorias"])

#Define el endpoint POST en la raiz (/Categorias/), especificando el modelo de respuesta.
@router.post("/", response_model=esquemas.CategoriaLeer)
#Define la funcion para crear una categoria.
def crear_categoria(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'CategoriaCrear'.
    categoria: esquemas.CategoriaCrear, 
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion (incluyendo la validacion de nombre unico) al modulo de 'servicios'.
    return servicios.create_categoria(session=session, categoria_create=categoria)

#Define el endpoint GET en la raiz (/Categorias/), respondiendo con una lista de categorias.
@router.get("/", response_model=List[esquemas.CategoriaLeer])
#Define la funcion para leer todas las categorias.
def leer_categorias(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de categorias, pasando la paginacion.
    categorias = servicios.get_categorias_todos(session, skip=skip, limit=limit)
    #Devuelve la lista de categorias encontrada.
    return categorias

#Define el endpoint DELETE para una categoria especifica, esperando un codigo 204 (No Content) al exito.
@router.delete("/{categoria_id}", status_code=204)
#Define la funcion para eliminar una categoria.
def eliminar_categoria(
    #Recibe el 'categoria_id' desde la ruta (path parameter).
    categoria_id: int,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session)
):
    #Llama al servicio para obtener la categoria por su ID.
    db_categoria = servicios.get_categoria(session, categoria_id=categoria_id)
    #Si la categoria no se encuentra (devuelve None).
    if not db_categoria:
        #Lanza un error HTTP 404 (No Encontrado).
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    #Marca el objeto 'db_categoria' para ser eliminado.
    session.delete(db_categoria)
    #Confirma (guarda) la eliminacion en la base de datos.
    session.commit()
    #Devuelve la respuesta (automaticamente sera 204 No Content).
    return