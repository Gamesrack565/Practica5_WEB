# esquemas.py
from sqlmodel import SQLModel
from typing import List, Optional
from Modelo.modelo import Libro, Autor, Editorial, Categoria, PublicoObjetivo, Serie

# --- Esquemas para Autor ---
class AutorBase(SQLModel):
    nombre: str

class AutorCreate(AutorBase):
    pass

class AutorRead(AutorBase):
    id: int

# --- Esquemas para Libro ---
class LibroBase(SQLModel):
    isbn: str
    titulo: str
    edicion: Optional[str] = None
    ano_publicacion: Optional[int] = None
    paginas: Optional[int] = None
    precio: float
    formato: str
    editorial: Editorial
    categorias: List[Categoria]
    publico_objetivo: PublicoObjetivo
    serie: Optional[Serie] = None

class LibroCreate(LibroBase):
    # Al crear un libro, pasamos una lista de IDs de autores existentes
    autores_ids: List[int]

# Esquema para LEER un libro (devuelve el libro con sus autores completos)
class LibroRead(LibroBase):
    id: int

# Esquema para leer un libro CON toda la info de sus autores
class LibroReadWithAutores(LibroRead):
    autores: List[AutorRead] = []
    
# Esquema para leer un autor CON toda la info de sus libros
class AutorReadWithLibros(AutorRead):
    libros: List[LibroRead] = []

# Actualizar modelos para que Pydantic pueda leer las relaciones
LibroRead.model_rebuild()
AutorRead.model_rebuild()