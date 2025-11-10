# Esquemas/esquemas.py
from sqlmodel import SQLModel
from typing import List, Optional

# --- Esquemas para Categoria ---
class CategoriaBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCrear(CategoriaBase):
    pass

class CategoriaLeer(CategoriaBase):
    id: int

# --- Esquemas para Autor ---
class AutorBase(SQLModel):
    nombre: str

class AutorCreacion(AutorBase):
    pass

class AutorLeer(AutorBase):
    id: int

# --- Esquemas para Direccion ---
class DireccionBase(SQLModel):
    calle: str
    ciudad_pais: str
    codigo_postal: str

class DireccionCrear(DireccionBase):
    pass

class DireccionLeer(DireccionBase):
    id: int

# --- Esquemas para Editorial ---
class EditorialBase(SQLModel):
    nombre: str

class EditorialCrear(EditorialBase):
    # Al crear una editorial, creamos su dirección al mismo tiempo
    direccion: DireccionCrear

class EditorialLeer(EditorialBase):
    id: int
    direccion: DireccionLeer # Anidado

# (Añade esto al final de Esquemas/esquemas.py)

class DireccionActualizar(SQLModel):
    """Esquema para actualizar solo algunos campos de una dirección"""
    calle: Optional[str] = None
    ciudad_pais: Optional[str] = None
    codigo_postal: Optional[str] = None

class EditorialActualizar(SQLModel):
    """Esquema para actualizar una editorial (PATCH)"""
    nombre: Optional[str] = None
    direccion: Optional[DireccionActualizar] = None

# --- Esquemas para PublicoObjetivo ---
class PublicoObjetivoBase(SQLModel):
    tipo: str

class PublicoObjetivoCrear(PublicoObjetivoBase):
    pass

class PublicoObjetivoLeer(PublicoObjetivoBase):
    id: int

# --- Esquemas para Serie ---
class SerieBase(SQLModel):
    nombre: str

class SerieCrear(SerieBase):
    pass

class SerieLeer(SerieBase):
    id: int

# --- Esquemas para Libro (ACTUALIZADO) ---
class LibroBase(SQLModel):
    isbn: Optional[str] = None
    titulo: str
    edicion: Optional[str] = None
    ano_publicacion: Optional[int] = None
    paginas: Optional[int] = None
    precio: float
    formato: str

class LibroCreacion(LibroBase):
    # === CAMBIO IMPORTANTE ===
    # Ahora recibimos nombres (strings) en lugar de IDs
    editorial_nombre: Optional[str] = None
    publico_objetivo_tipo: Optional[str] = None # 'tipo' es el "nombre" de esta entidad
    serie_nombre: Optional[str] = None
    
    # Mantenemos el patrón de nombres que ya teníamos
    autores_nombres: List[str] = []
    categorias_nombres: List[str] = []

class LibroLeer(LibroBase):
    id: int

# Esquema para leer un libro CON toda la info anidada
class LibroLeerCompleto(LibroLeer):
    editorial: Optional[EditorialLeer] = None
    publico_objetivo: Optional[PublicoObjetivoLeer] = None
    serie: Optional[SerieLeer] = None
    autores: List[AutorLeer] = []
    categorias: List[CategoriaLeer] = []
    
# Esquema para leer un autor CON toda la info de sus libros
class AutorLeer_con_Libros(AutorLeer):
    libros: List[LibroLeer] = []

# Actualizar referencias
LibroLeerCompleto.model_rebuild()
AutorLeer_con_Libros.model_rebuild()
EditorialLeer.model_rebuild()