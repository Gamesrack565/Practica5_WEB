#Libros

#Modulos y librerias
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session


router = APIRouter(prefix="/Libros", tags=["Libros"])

# --- Rutas para Libros ---
#Define el endpoint POST en la raiz (/Libros/), especificando el modelo de respuesta (completo).
@router.post("/", response_model=esquemas.LibroLeerCompleto) # Cambiado
#Define la funcion para crear un libro.
def crear_libro(
    #Define que el cuerpo (body) de la peticion debe seguir el esquema 'LibroCreacion'.
    libro: esquemas.LibroCreacion, # Cambiado
    #Inyecta la dependencia de la sesion de la base de datos.
    session: Session = Depends(get_session)
):
    #Delega la logica de creacion (buscar/crear relaciones por nombre) al modulo de 'servicios'.
    return servicios.create_libro(session=session, libro_create=libro)

# 1. Endpoint general con paginación
#Define el endpoint GET en la raiz (/Libros/), respondiendo con una lista de libros completos.
@router.get("/", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
#Define la funcion para leer todos los libros.
def leer_libros_todos(
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' (para paginacion), con valor minimo 0.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' (para paginacion), con minimo 1 y maximo 100.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio para obtener la lista de libros, pasando la paginacion.
    libros = servicios.get_libros_todos(session, skip=skip, limit=limit)
    #Devuelve la lista de libros encontrada.
    return libros
# 1. Consultar libros x autor
#Define el endpoint GET en /por-autor, respondiendo con una lista de libros completos.
@router.get("/por-autor", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
#Define la funcion para leer libros filtrados por autor.
def leer_libros_por_autor(
    #Recibe el 'nombre_autor' como parametro de consulta (query parameter).
    nombre_autor: str,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' para paginacion.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' para paginacion.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio que contiene la logica de filtrado por autor.
    libros = servicios.get_libros_por_autor(
        session, nombre_autor=nombre_autor, skip=skip, limit=limit
    )
    #Devuelve la lista de libros filtrada.
    return libros

# 2. Libros x categoria
#Define el endpoint GET en /por-categoria.
@router.get("/por-categoria", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
#Define la funcion para leer libros filtrados por categoria.
def leer_libros_por_categoria(
    #Recibe el 'genero' (nombre de la categoria) como parametro de consulta.
    genero: str, # Este 'genero' es ahora el 'nombre' de la categoría
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' para paginacion.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' para paginacion.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio que contiene la logica de filtrado por categoria.
    libros = servicios.get_libros_por_categoria(
        session, genero=genero, skip=skip, limit=limit
    )
    #Devuelve la lista de libros filtrada.
    return libros

# 3. Libros x serie
#Define el endpoint GET en /por-serie.
@router.get("/por-serie", response_model=List[esquemas.LibroLeerCompleto]) 
#Define la funcion para leer libros filtrados por serie.
def leer_libros_por_serie(
    #Recibe el 'nombre_serie' como parametro de consulta.
    nombre_serie: str,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' para paginacion.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' para paginacion.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio que contiene la logica de filtrado por serie.
    libros = servicios.get_libros_por_serie(
        session, nombre_serie=nombre_serie, skip=skip, limit=limit
    )
    #Devuelve la lista de libros filtrada.
    return libros

# (Añade esto en Rutas/libros.py)

#Define el endpoint GET para buscar un libro por su ISBN (parametro de ruta).
@router.get("/isbn/{isbn}", response_model=esquemas.LibroLeerCompleto)
#Define la funcion para leer un libro por ISBN.
def leer_libro_por_isbn(
    #Recibe el 'isbn' desde la ruta (path parameter).
    isbn: str,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session)
):
    """Obtiene un libro específico por su ISBN."""
    #Llama al servicio que busca el libro por ISBN.
    db_libro = servicios.get_libro_por_isbn(session, isbn=isbn)
    #Si el servicio devuelve None (no se encontro).
    if not db_libro:
        #Lanza un error HTTP 404 (No Encontrado).
        raise HTTPException(
            status_code=404, 
            detail="Libro con ese ISBN no encontrado"
        )
    #Devuelve el libro encontrado.
    return db_libro


# 4. Libros x público objetivo
#Define el endpoint GET en /por-publico.
@router.get("/por-publico", response_model=List[esquemas.LibroLeerCompleto]) 
#Define la funcion para leer libros filtrados por publico.
def leer_libros_por_publico(
    #Recibe el 'tipo_publico' como parametro de consulta.
    tipo_publico: str,
    #Inyecta la dependencia de la sesion.
    session: Session = Depends(get_session),
    #Define el parametro de consulta 'skip' para paginacion.
    skip: int = Query(0, ge=0),
    #Define el parametro de consulta 'limit' para paginacion.
    limit: int = Query(10, ge=1, le=100)
):
    #Llama al servicio que contiene la logica de filtrado por publico.
    libros = servicios.get_libros_por_publico(
        session, tipo_publico=tipo_publico, skip=skip, limit=limit
    )
    #Devuelve la lista de libros filtrada.
    return libros