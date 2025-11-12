#Modelos de la base de datos para la aplicacion de gestion de libros.

#Librerias y modulos necesarios.
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
#Importa la biblioteca 'uuid' para generar identificadores unicos (para el ISBN).
import uuid

# --- Tablas Link (Many-to-Many) ---
#Define la tabla de enlace (asociativa) para la relacion Libro <-> Autor.
class LibroAutorLink(SQLModel, table=True):
    #Define el campo 'libro_id' como clave foranea a 'libro.id' y parte de la clave primaria.
    libro_id: Optional[int] = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    #Define el campo 'autor_id' como clave foranea a 'autor.id' y parte de la clave primaria.
    autor_id: Optional[int] = Field(
        default=None, foreign_key="autor.id", primary_key=True
    )

#Define la tabla de enlace (asociativa) para la relacion Libro <-> Categoria.
class LibroCategoriaLink(SQLModel, table=True):
    #Define el campo 'libro_id' como clave foranea a 'libro.id' y parte de la clave primaria.
    libro_id: Optional[int] = Field(
        default=None, foreign_key="libro.id", primary_key=True
    )
    #Define el campo 'categoria_id' como clave foranea a 'categoria.id' y parte de la clave primaria.
    categoria_id: Optional[int] = Field(
        default=None, foreign_key="categoria.id", primary_key=True
    )

# --- Tablas de Entidad ---
#Define el modelo de la tabla 'direccion' en la BD.
class Direccion(SQLModel, table=True):
    #Define la clave primaria 'id' como un entero opcional autogenerado.
    id: Optional[int] = Field(default=None, primary_key=True)
    #Define el campo 'calle' como un string.
    calle: str
    #Define el campo 'ciudad_pais' como un string.
    ciudad_pais: str
    #Define el campo 'codigo_postal' como un string.
    codigo_postal: str
    
    #Define la relacion inversa (uno-a-uno) con 'Editorial'.
    editorial: Optional["Editorial"] = Relationship(back_populates="direccion")

#Define el modelo de la tabla 'editorial'.
class Editorial(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    #Define el campo 'nombre' como un string.
    nombre: str
    
    #Define la clave foranea 'direccion_id' que apunta a 'direccion.id'.
    direccion_id: int = Field(foreign_key="direccion.id")
    #Define la relacion (uno-a-uno) con 'Direccion'.
    direccion: Direccion = Relationship(back_populates="editorial")
    
    #Define la relacion (uno-a-muchos) con 'Libro' (una editorial tiene muchos libros).
    libros: List["Libro"] = Relationship(back_populates="editorial")

#Define el modelo de la tabla 'categoria'.
class Categoria(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # CAMBIO: Estandarizado a 'nombre' y añadido 'unique=True'
    #Define el campo 'nombre', indexado y con restriccion unica.
    nombre: str = Field(index=True, unique=True)
    #Define el campo 'descripcion' como un string opcional.
    descripcion: Optional[str] = None
    
    #Define la relacion muchos-a-muchos con 'Libro', usando 'LibroCategoriaLink' como tabla de enlace.
    libros: List["Libro"] = Relationship(
        back_populates="categorias", link_model=LibroCategoriaLink
    )

#Define el modelo de la tabla 'publicoobjetivo'.
class PublicoObjetivo(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    #Define el campo 'tipo' (ej. +18, Publico en general), y lo marca como indexado.
    tipo: str = Field(index=True) # +18, Publico en general, Dinámico
    
    #Define la relacion (uno-a-muchos) con 'Libro' (un publico tiene muchos libros).
    libros: List["Libro"] = Relationship(back_populates="publico_objetivo")

#Define el modelo de la tabla 'serie'.
class Serie(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    #Define el campo 'nombre' como string y lo marca como indexado.
    nombre: str = Field(index=True)
    
    #Define la relacion (uno-a-muchos) con 'Libro' (una serie tiene muchos libros).
    libros: List["Libro"] = Relationship(back_populates="serie")

#Define el modelo de la tabla 'autor'.
class Autor(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    #Define el campo 'nombre' como string y lo marca como indexado.
    nombre: str = Field(index=True)
    
    #Define la relacion muchos-a-muchos con 'Libro', usando 'LibroAutorLink' como tabla de enlace.
    libros: List["Libro"] = Relationship(
        back_populates="autores", link_model=LibroAutorLink
    )

# --- Tabla Principal: Libro ---
#Define el modelo de la tabla principal 'libro'.
class Libro(SQLModel, table=True):
    #Define la clave primaria 'id'.
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Define el campo 'isbn' como un string.
    isbn: str = Field(
        #Usa 'uuid.uuid4' para generar un ISBN por defecto si no se proporciona uno.
        default_factory=lambda: str(uuid.uuid4()), 
        #Asegura que el ISBN sea unico en la tabla.
        unique=True, 
        #Crea un indice en este campo para busquedas rapidas.
        index=True
    )
    #Define el campo 'titulo' como un string.
    titulo: str
    #Define el campo 'edicion' como un string opcional.
    edicion: Optional[str] = None
    #Define el campo 'ano_publicacion' como un entero opcional.
    ano_publicacion: Optional[int] = None
    #Define el campo 'paginas' como un entero opcional.
    paginas: Optional[int] = None
    #Define el campo 'precio' como un numero de punto flotante.
    precio: float
    #Define el campo 'formato' (ej. Fisico o digital).
    formato: str

    # --- Relaciones (Foreign Keys) ---
    #Define la clave foranea 'editorial_id' (opcional) que apunta a 'editorial.id'.
    editorial_id: Optional[int] = Field(default=None, foreign_key="editorial.id")
    #Define la relacion (muchos-a-uno) con 'Editorial'.
    editorial: Optional[Editorial] = Relationship(back_populates="libros")
    
    #Define la clave foranea 'publico_objetivo_id' (opcional).
    publico_objetivo_id: Optional[int] = Field(default=None, foreign_key="publicoobjetivo.id")
    #Define la relacion (muchos-a-uno) con 'PublicoObjetivo'.
    publico_objetivo: Optional[PublicoObjetivo] = Relationship(back_populates="libros")
    
    #Define la clave foranea 'serie_id' (opcional).
    serie_id: Optional[int] = Field(default=None, foreign_key="serie.id")
    #Define la relacion (muchos-a-uno) con 'Serie'.
    serie: Optional[Serie] = Relationship(back_populates="libros")

    # --- Relaciones (Many-to-Many) ---
    #Define la relacion muchos-a-muchos con 'Autor', usando 'LibroAutorLink'.
    autores: List[Autor] = Relationship(
        back_populates="libros", link_model=LibroAutorLink
    )
    #Define la relacion muchos-a-muchos con 'Categoria', usando 'LibroCategoriaLink'.
    categorias: List[Categoria] = Relationship(
        back_populates="libros", link_model=LibroCategoriaLink
    )