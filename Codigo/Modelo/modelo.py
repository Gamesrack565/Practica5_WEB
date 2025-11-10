# Modelo/modelo.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import uuid

# --- Tablas Link (Many-to-Many) ---
class LibroAutorLink(SQLModel, table=True):
    libro_id: Optional[int] = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    autor_id: Optional[int] = Field(
        default=None, foreign_key="autor.id", primary_key=True
    )

class LibroCategoriaLink(SQLModel, table=True):
    libro_id: Optional[int] = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    categoria_id: Optional[int] = Field(
        default=None, foreign_key="categoria.id", primary_key=True
    )

# --- Tablas de Entidad ---
class Direccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    calle: str
    ciudad_pais: str
    codigo_postal: str
    
    editorial: Optional["Editorial"] = Relationship(back_populates="direccion")

class Editorial(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    
    direccion_id: int = Field(foreign_key="direccion.id")
    direccion: Direccion = Relationship(back_populates="editorial")
    
    libros: List["Libro"] = Relationship(back_populates="editorial")

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # CAMBIO: Estandarizado a 'nombre' y añadido 'unique=True'
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    
    libros: List["Libro"] = Relationship(
        back_populates="categorias", link_model=LibroCategoriaLink
    )

class PublicoObjetivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(index=True) # +18, Publico en general, Dinámico
    
    libros: List["Libro"] = Relationship(back_populates="publico_objetivo")

class Serie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    libros: List["Libro"] = Relationship(back_populates="serie")

class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    libros: List["Libro"] = Relationship(
        back_populates="autores", link_model=LibroAutorLink
    )

# --- Tabla Principal: Libro ---
class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    isbn: str = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        unique=True, 
        index=True
    )
    titulo: str
    edicion: Optional[str] = None
    ano_publicacion: Optional[int] = None
    paginas: Optional[int] = None
    precio: float
    formato: str # Físico o digital

    # --- Relaciones (Foreign Keys) ---
    editorial_id: Optional[int] = Field(default=None, foreign_key="editorial.id")
    editorial: Optional[Editorial] = Relationship(back_populates="libros")
    
    publico_objetivo_id: Optional[int] = Field(default=None, foreign_key="publicoobjetivo.id")
    publico_objetivo: Optional[PublicoObjetivo] = Relationship(back_populates="libros")
    
    serie_id: Optional[int] = Field(default=None, foreign_key="serie.id")
    serie: Optional[Serie] = Relationship(back_populates="libros")

    # --- Relaciones (Many-to-Many) ---
    autores: List[Autor] = Relationship(
        back_populates="libros", link_model=LibroAutorLink
    )
    categorias: List[Categoria] = Relationship(
        back_populates="libros", link_model=LibroCategoriaLink
    )