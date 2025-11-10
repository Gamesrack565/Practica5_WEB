# Rutas/libros.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from Servicios import servicios
from Esquemas import esquemas
from Servicios.database import get_session

router = APIRouter(prefix="/Libros", tags=["Libros"])

# --- Rutas para Libros ---
@router.post("/", response_model=esquemas.LibroLeerCompleto) # Cambiado
def crear_libro(
    libro: esquemas.LibroCreacion, # Cambiado
    session: Session = Depends(get_session)
):
    return servicios.create_libro(session=session, libro_create=libro)

# 1. Endpoint general con paginación
@router.get("/", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
def leer_libros_todos(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_todos(session, skip=skip, limit=limit)
    return libros

# 1. Consultar libros x autor
@router.get("/por-autor", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
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
@router.get("/por-categoria", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
def leer_libros_por_categoria(
    genero: str, # Este 'genero' es ahora el 'nombre' de la categoría
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    libros = servicios.get_libros_por_categoria(
        session, genero=genero, skip=skip, limit=limit
    )
    return libros

# 3. Libros x serie
@router.get("/por-serie", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
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

# (Añade esto en Rutas/libros.py)

@router.get("/isbn/{isbn}", response_model=esquemas.LibroLeerCompleto)
def leer_libro_por_isbn(
    isbn: str,
    session: Session = Depends(get_session)
):
    """Obtiene un libro específico por su ISBN."""
    
    db_libro = servicios.get_libro_por_isbn(session, isbn=isbn)
    
    if not db_libro:
        raise HTTPException(
            status_code=404, 
            detail="Libro con ese ISBN no encontrado"
        )
        
    return db_libro


# 4. Libros x público objetivo
@router.get("/por-publico", response_model=List[esquemas.LibroLeerCompleto]) # Cambiado
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