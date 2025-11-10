# rutas.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter()

# --- Rutas para Autores ---
@router.post("/autores/", response_model=esquemas.AutorRead)
def crear_autor(
    autor: esquemas.AutorCreate, 
    session: Session = Depends(get_session)
):
    return servicios.create_autor(session=session, autor_create=autor)

# --- Rutas para Libros ---
@router.post("/libros/", response_model=esquemas.LibroReadWithAutores)
def crear_libro(
    libro: esquemas.LibroCreate, 
    session: Session = Depends(get_session)
):
    return servicios.create_libro(session=session, libro_create=libro)


# --- Rutas Adicionales (tus endpoints) ---

# 1. Endpoint general con paginación
@router.get("/libros/", response_model=List[esquemas.LibroReadWithAutores])
def leer_libros_todos(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lee todos los libros con paginación.
    - skip: (Query parameter) Cuántos saltar
    - limit: (Query parameter) Cuántos obtener
    """
    libros = servicios.get_libros_todos(session, skip=skip, limit=limit)
    return libros

# 1. (Tu endpoint 1) Consultar libros x autor
@router.get("/libros/por-autor/", response_model=List[esquemas.LibroReadWithAutores])
def leer_libros_por_autor(
    nombre_autor: str,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_por_autor(
        session, nombre_autor=nombre_autor, skip=skip, limit=limit
    )
    return libros

# 2. Libros x categoria
@router.get("/libros/por-categoria/", response_model=List[esquemas.LibroReadWithAutores])
def leer_libros_por_categoria(
    genero: str,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_por_categoria(
        session, genero=genero, skip=skip, limit=limit
    )
    return libros

# (Añade esto al final de Rutas/rutas.py)

# 3. Libros x serie
@router.get("/libros/por-serie/", response_model=List[esquemas.LibroReadWithAutores])
def leer_libros_por_serie(
    nombre_serie: str,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_por_serie(
        session, nombre_serie=nombre_serie, skip=skip, limit=limit
    )
    return libros

# 4. Libros x público objetivo
@router.get("/libros/por-publico/", response_model=List[esquemas.LibroReadWithAutores])
def leer_libros_por_publico(
    tipo_publico: str,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_por_publico(
        session, tipo_publico=tipo_publico, skip=skip, limit=limit
    )
    return libros