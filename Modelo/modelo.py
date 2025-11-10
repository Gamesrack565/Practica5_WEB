# modelos.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, JSON, Column

# --- Modelos Anidados (JSON) ---
class Direccion(SQLModel):
    calle: str
    ciudad_pais: str
    codigo_postal: str

class Editorial(SQLModel):
    nombre: str
    direccion: Direccion

class Categoria(SQLModel):
    genero_literario: str

class PublicoObjetivo(SQLModel):
    tipo: str  # +18, Publico en general, Dinámico

class Serie(SQLModel):
    nombre: str

# --- MUEVE LA TABLA LINK AQUÍ ---
# Tabla "link" (asociación) para la relación Muchos a Muchos
# Debe definirse ANTES de Libro y Autor
class LibroAutorLink(SQLModel, table=True):
    libro_id: Optional[int] = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    autor_id: Optional[int] = Field(
        default=None, foreign_key="autor.id", primary_key=True
    )

# --- Modelos de Tabla (Tablas SQL) ---

# Modelo para los Autores (Será una tabla)
class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    # La relación: "libros" es una lista de "Libro"
    # Quita las comillas de link_model=
    libros: List["Libro"] = Relationship(back_populates="autores", link_model=LibroAutorLink)

# Modelo de Tabla para Libros
class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    isbn: str = Field(unique=True, index=True)
    titulo: str
    edicion: Optional[str] = None
    ano_publicacion: Optional[int] = None
    paginas: Optional[int] = None
    precio: float
    formato: str # Físico o digital

    # ... (Datos Anidados) ...
    editorial: Editorial = Field(sa_column=Column(JSON))
    categorias: List[Categoria] = Field(sa_column=Column(JSON))
    publico_objetivo: PublicoObjetivo = Field(sa_column=Column(JSON))
    serie: Optional[Serie] = Field(default=None, sa_column=Column(JSON))

    # --- Relaciones ---
    # Quita las comillas de link_model=
    autores: List[Autor] = Relationship(back_populates="libros", link_model=LibroAutorLink)