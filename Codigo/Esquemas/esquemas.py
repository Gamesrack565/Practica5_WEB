#Esquemas para la API de gestión de libros utilizando SQLModel.

#Modulos y librerias necesarias.
from sqlmodel import SQLModel
from typing import List, Optional

# --- Esquemas para Categoria ---
#Define el modelo base para 'Categoria' con los campos comunes.
class CategoriaBase(SQLModel):
    #Define el campo 'nombre' como un string (requerido).
    nombre: str
    #Define el campo 'descripcion' como un string opcional, por defecto Nulo.
    descripcion: Optional[str] = None

#Define el esquema para CREAR una Categoria (lo que la API recibe en un POST).
class CategoriaCrear(CategoriaBase):
    #Hereda todos los campos de CategoriaBase y no añade nuevos.
    pass

#Define el esquema para LEER una Categoria (lo que la API devuelve en un GET).
class CategoriaLeer(CategoriaBase):
    #Añade el 'id' a la respuesta, ya que este es generado por la BD.
    id: int

# --- Esquemas para Autor ---
#Define el modelo base para 'Autor'.
class AutorBase(SQLModel):
    #Define el campo 'nombre' como un string.
    nombre: str

#Define el esquema para CREAR un Autor.
class AutorCreacion(AutorBase):
    #No necesita campos adicionales.
    pass

#Define el esquema para LEER un Autor.
class AutorLeer(AutorBase):
    #Añade el 'id' generado por la BD a la respuesta.
    id: int

# --- Esquemas para Direccion ---
#Define el modelo base para 'Direccion'.
class DireccionBase(SQLModel):
    #Define el campo 'calle' como un string.
    calle: str
    #Define el campo 'ciudad_pais' como un string.
    ciudad_pais: str
    #Define el campo 'codigo_postal' como un string.
    codigo_postal: str

#Define el esquema para CREAR una Direccion.
class DireccionCrear(DireccionBase):
    #No necesita campos adicionales.
    pass

#Define el esquema para LEER una Direccion.
class DireccionLeer(DireccionBase):
    #Añade el 'id' generado por la BD a la respuesta.
    id: int

# --- Esquemas para Editorial ---
#Define el modelo base para 'Editorial'.
class EditorialBase(SQLModel):
    #Define el campo 'nombre' como un string.
    nombre: str

#Define el esquema para CREAR una Editorial.
class EditorialCrear(EditorialBase):
    # Al crear una editorial, creamos su dirección al mismo tiempo
    #Espera recibir un objeto 'Direccion' anidado que cumpla con el esquema 'DireccionCrear'.
    direccion: DireccionCrear

#Define el esquema para LEER una Editorial.
class EditorialLeer(EditorialBase):
    #Añade el 'id' generado por la BD.
    id: int
    #Muestra el objeto 'Direccion' completo (anidado) en la respuesta.
    direccion: DireccionLeer # Anidado

#Define el esquema para ACTUALIZAR una Direccion (PATCH).
class DireccionActualizar(SQLModel):
    """Esquema para actualizar solo algunos campos de una dirección"""
    #Define el campo 'calle' como opcional.
    calle: Optional[str] = None
    #Define el campo 'ciudad_pais' como opcional.
    ciudad_pais: Optional[str] = None
    #Define el campo 'codigo_postal' como opcional.
    codigo_postal: Optional[str] = None

#Define el esquema para ACTUALIZAR una Editorial (PATCH).
class EditorialActualizar(SQLModel):
    """Esquema para actualizar una editorial (PATCH)"""
    #Define el campo 'nombre' como opcional.
    nombre: Optional[str] = None
    #Permite actualizar la direccion (o partes de ella) de forma anidada.
    direccion: Optional[DireccionActualizar] = None

# --- Esquemas para PublicoObjetivo ---
#Define el modelo base para 'PublicoObjetivo'.
class PublicoObjetivoBase(SQLModel):
    #Define el campo 'tipo' (ej. "+18", "Infantil").
    tipo: str

#Define el esquema para CREAR un PublicoObjetivo.
class PublicoObjetivoCrear(PublicoObjetivoBase):
    #No necesita campos adicionales.
    pass

#Define el esquema para LEER un PublicoObjetivo.
class PublicoObjetivoLeer(PublicoObjetivoBase):
    #Añade el 'id' generado por la BD.
    id: int

# --- Esquemas para Serie ---
#Define el modelo base para 'Serie'.
class SerieBase(SQLModel):
    #Define el campo 'nombre' como string.
    nombre: str

#Define el esquema para CREAR una Serie.
class SerieCrear(SerieBase):
    #No necesita campos adicionales.
    pass

#Define el esquema para LEER una Serie.
class SerieLeer(SerieBase):
    #Añade el 'id' generado por la BD.
    id: int

# --- Esquemas para Libro (ACTUALIZADO) ---
#Define el modelo base para 'Libro'.
class LibroBase(SQLModel):
    #Define el campo 'isbn' como opcional (aunque el modelo de BD lo genera).
    isbn: Optional[str] = None
    #Define el campo 'titulo' como string (requerido).
    titulo: str
    #Define el campo 'edicion' como string opcional.
    edicion: Optional[str] = None
    #Define el campo 'ano_publicacion' como entero opcional.
    ano_publicacion: Optional[int] = None
    #Define el campo 'paginas' como entero opcional.
    paginas: Optional[int] = None
    #Define el campo 'precio' como float (requerido).
    precio: float
    #Define el campo 'formato' (ej. "Físico", "Digital").
    formato: str

#Define el esquema para CREAR un Libro (entrada POST).
class LibroCreacion(LibroBase):
    # === CAMBIO IMPORTANTE ===
    # Ahora recibimos nombres (strings) en lugar de IDs
    #Espera el *nombre* de la editorial (string) en lugar de un ID.
    editorial_nombre: Optional[str] = None
    #Espera el *tipo* del publico (string) en lugar de un ID.
    publico_objetivo_tipo: Optional[str] = None # 'tipo' es el "nombre" de esta entidad
    #Espera el *nombre* de la serie (string) en lugar de un ID.
    serie_nombre: Optional[str] = None
    
    # Mantenemos el patrón de nombres que ya teníamos
    #Espera una lista de *nombres* de autores (strings).
    autores_nombres: List[str] = []
    #Espera una lista de *nombres* de categorias (strings).
    categorias_nombres: List[str] = []

#Define el esquema base para LEER un Libro (salida GET).
class LibroLeer(LibroBase):
    #Añade el 'id' del libro a la respuesta.
    id: int

#Define un esquema de LECTURA COMPLETA para un Libro.
class LibroLeerCompleto(LibroLeer):
    #Muestra el objeto 'Editorial' completo (anidado).
    editorial: Optional[EditorialLeer] = None
    #Muestra el objeto 'PublicoObjetivo' completo (anidado).
    publico_objetivo: Optional[PublicoObjetivoLeer] = None
    #Muestra el objeto 'Serie' completo (anidado).
    serie: Optional[SerieLeer] = None
    #Muestra una lista de objetos 'Autor' completos (anidado).
    autores: List[AutorLeer] = []
    #Muestra una lista de objetos 'Categoria' completos (anidado).
    categorias: List[CategoriaLeer] = []
    
#Define un esquema de LECTURA COMPLETA para un Autor.
class AutorLeer_con_Libros(AutorLeer):
    #Muestra una lista de los 'Libros' de ese autor (anidado).
    libros: List[LibroLeer] = []

#Reconstruye el modelo para actualizar las referencias anidadas (Forward Refs).
LibroLeerCompleto.model_rebuild()
#Reconstruye el modelo para actualizar las referencias anidadas.
AutorLeer_con_Libros.model_rebuild()
#Reconstruye el modelo para actualizar la referencia a 'DireccionLeer'.
EditorialLeer.model_rebuild()