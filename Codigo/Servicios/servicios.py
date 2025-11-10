# servicios.py
from sqlmodel import Session, select
from typing import List
from Modelo import modelo
from Esquemas import esquemas

# --- Servicios para Autores ---
def create_autor(session: Session, autor_create: esquemas.AutorCreate) -> modelo.Autor:
    db_autor = modelo.Autor.model_validate(autor_create)
    session.add(db_autor)
    session.commit()
    session.refresh(db_autor)
    return db_autor

def get_autor(session: Session, autor_id: int) -> modelo.Autor | None:
    return session.get(modelo.Autor, autor_id)

# --- Servicios para Libros ---
def create_libro(session: Session, libro_create: esquemas.LibroCreate) -> modelo.Libro:
    # 1. Creamos el objeto Libro sin los autores
    libro_data = libro_create.model_dump(exclude={"autores_ids"})
    db_libro = modelo.Libro(**libro_data)
    
    # 2. Buscamos los autores por ID y los asignamos
    for autor_id in libro_create.autores_ids:
        autor = get_autor(session, autor_id)
        if autor:
            db_libro.autores.append(autor)
            
    # 3. Guardamos en la BD
    session.add(db_libro)
    session.commit()
    session.refresh(db_libro)
    return db_libro

# --- Endpoints Adicionales ---

def get_libros_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    """Consulta todos los libros, con paginación."""
    statement = select(modelo.Libro).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_libros_por_autor(session: Session, nombre_autor: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    """Consulta libros por nombre de autor, con paginación."""
    statement = (
        select(modelo.Libro)
        .join(modelo.LibroAutorLink)
        .join(modelo.Autor)
        .where(modelo.Autor.nombre == nombre_autor)
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()

def get_libros_por_categoria(session: Session, genero: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    """Consulta libros por categoría (género)."""
    # Esta consulta es más compleja porque el JSON
    # JSON_CONTAINS o similar es dependiente de la BD (SQLite, Postgres, etc.)
    # Por ahora, lo hacemos en Python (menos eficiente, pero funciona)
    
    # Esta es una simplificación. Idealmente, Categoria sería su propia tabla.
    todos_los_libros = session.exec(select(modelo.Libro)).all()
    libros_filtrados = []
    for libro in todos_los_libros:
        for cat in libro.categorias:
            if cat.genero_literario.lower() == genero.lower():
                libros_filtrados.append(libro)
                break
    
    return libros_filtrados[skip : skip + limit]

# (Añade esto al final de Servicios/servicios.py)

def get_libros_por_serie(session: Session, nombre_serie: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    """Consulta libros por nombre de serie."""
    
    # Obtenemos todos los libros
    todos_los_libros = session.exec(select(modelo.Libro)).all()
    
    libros_filtrados = []
    for libro in todos_los_libros:
        # Importante: Verificamos que 'libro.serie' no sea None
        # y luego comparamos el nombre
        if libro.serie and libro.serie.nombre.lower() == nombre_serie.lower():
            libros_filtrados.append(libro)
            
    # Aplicamos paginación a la lista filtrada
    return libros_filtrados[skip : skip + limit]


def get_libros_por_publico(session: Session, tipo_publico: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    """Consulta libros por público objetivo."""
    
    # Obtenemos todos los libros
    todos_los_libros = session.exec(select(modelo.Libro)).all()
    
    libros_filtrados = []
    for libro in todos_los_libros:
        # El modelo dice que publico_objetivo siempre existe,
        # así que podemos comparar directamente
        if libro.publico_objetivo.tipo.lower() == tipo_publico.lower():
            libros_filtrados.append(libro)
            
    # Aplicamos paginación a la lista filtrada
    return libros_filtrados[skip : skip + limit]