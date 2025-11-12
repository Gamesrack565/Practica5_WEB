#Editoriales

#Librerias y modulos necesarios
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session


router = APIRouter(prefix="/Editoriales", tags=["Editoriales"])

#Define el endpoint POST en la raiz (/Editoriales/), especificando el modelo de respuesta.
@router.post("/", response_model=esquemas.EditorialLeer)
#Define la funcion para crear una editorial.
def crear_editorial(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'EditorialCrear'.
    editorial: esquemas.EditorialCrear, 
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion (incluyendo la creacion anidada de la direccion) al modulo de 'servicios'.
    return servicios.create_editorial(session=session, editorial_create=editorial)

#Define el endpoint GET en la raiz (/Editoriales/), respondiendo con una lista de editoriales.
@router.get("/", response_model=List[esquemas.EditorialLeer])
#Define la funcion para leer todas las editoriales.
def leer_editoriales_todas(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de editoriales, pasando la paginacion.
    editoriales = servicios.get_editoriales_todas(session, skip=skip, limit=limit)
    #Devuelve la lista de editoriales encontrada.
    return editoriales


# (Añade esto en Rutas/editoriales.py, junto a tus otras rutas)

#Define el endpoint PATCH para una editorial especifica, especificando el modelo de respuesta.
@router.patch("/{editorial_id}", response_model=esquemas.EditorialLeer)
#Define la funcion para actualizar una editorial.
def actualizar_editorial_ruta(
    #Recibe el 'editorial_id' desde la ruta (path parameter).
    editorial_id: int,
    #Recibe los datos de actualizacion (del body) que coinciden con el esquema.
    editorial_update: esquemas.EditorialActualizar,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session)
):
    # 1. Busca la editorial
    #Llama al servicio 'get_editorial' para encontrar la editorial por su ID.
    db_editorial = servicios.get_editorial(session, editorial_id=editorial_id)
    #Si el servicio devuelve None (no se encontro).
    if not db_editorial:
        #Lanza un error HTTP 404 (No Encontrado).
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    # 2. Llama al servicio para que haga la actualización
    #Delega la logica de actualizacion (incluyendo la direccion anidada) al modulo de 'servicios'.
    return servicios.actualizar_editorial(
        #Pasa la sesion actual al servicio.
        session=session, 
        #Pasa la editorial ya encontrada al servicio.
        db_editorial=db_editorial, 
        #Pasa los datos de actualizacion al servicio.
        editorial_update=editorial_update
    )

#Define el endpoint DELETE para una editorial especifica, esperando un codigo 204 (No Content).
@router.delete("/{editorial_id}", 
    #Define el codigo de estado HTTP para una eliminacion exitosa.
    status_code=204 
)
#Define la funcion para eliminar una editorial.
def eliminar_editorial(
    #Recibe el 'editorial_id' desde la ruta.
    editorial_id: int,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session)
):
    # 1. Obtenemos la editorial
    #Llama al servicio para obtener la editorial por su ID.
    db_editorial = servicios.get_editorial(session, editorial_id=editorial_id)
    #Si no se encuentra.
    if not db_editorial:
        #Lanza un error 404.
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    # 2. Obtenemos la dirección asociada ANTES de borrar
    #Accede a la direccion asociada a la editorial (cargada por la relacion).
    db_direccion = db_editorial.direccion

    # 3. Borramos ambos
    #Marca la editorial para ser eliminada (la BD deberia borrar en cascada las FK en Libro).
    session.delete(db_editorial)
    #Si la editorial tenia una direccion asociada.
    if db_direccion:
        #Marca tambien la direccion para ser eliminada (limpieza de la relacion 1-a-1).
        session.delete(db_direccion)
    
    # 4. Guardamos
    #Confirma (guarda) la eliminacion de ambos registros en la BD.
    session.commit()
    
    # 5. Retornamos None (implícito)
    #Devuelve la respuesta (automaticamente sera 204 No Content).
    return