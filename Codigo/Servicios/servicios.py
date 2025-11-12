#Sevicios: La parte más larga de todas

#Modulos y librerias necesarias
from sqlmodel import Session, select
from typing import List, Optional
from Modelo import modelo
from Esquemas import esquemas
from fastapi import HTTPException

# --- Funciones Helper "Get by Name" ---

#Define una funcion de ayuda para buscar un Autor por su nombre.
def get_autor_por_nombre(session: Session, nombre: str) -> Optional[modelo.Autor]:
    #Crea una consulta para seleccionar un Autor donde el nombre coincida.
    statement = select(modelo.Autor).where(modelo.Autor.nombre == nombre)
    #Ejecuta la consulta en la sesion y devuelve el primer resultado (o None).
    return session.exec(statement).first()

#Define una funcion de ayuda para buscar una Categoria por su nombre.
def get_categoria_por_nombre(session: Session, nombre: str) -> Optional[modelo.Categoria]:
    #Crea una consulta para seleccionar una Categoria donde el nombre coincida.
    statement = select(modelo.Categoria).where(modelo.Categoria.nombre == nombre)
    #Ejecuta la consulta y devuelve el primer resultado.
    return session.exec(statement).first()

#Define una funcion de ayuda para buscar una Editorial por su nombre.
def get_editorial_por_nombre(session: Session, nombre: str) -> Optional[modelo.Editorial]:
    #Crea una consulta para seleccionar una Editorial donde el nombre coincida.
    statement = select(modelo.Editorial).where(modelo.Editorial.nombre == nombre)
    #Ejecuta la consulta y devuelve el primer resultado.
    return session.exec(statement).first()

#Define una funcion de ayuda para buscar un PublicoObjetivo por su tipo.
def get_publico_objetivo_por_tipo(session: Session, tipo: str) -> Optional[modelo.PublicoObjetivo]:
    #Crea una consulta para seleccionar un PublicoObjetivo donde el tipo coincida.
    statement = select(modelo.PublicoObjetivo).where(modelo.PublicoObjetivo.tipo == tipo)
    #Ejecuta la consulta y devuelve el primer resultado.
    return session.exec(statement).first()

#Define una funcion de ayuda para buscar una Serie por su nombre.
def get_serie_por_nombre(session: Session, nombre: str) -> Optional[modelo.Serie]:
    #Crea una consulta para seleccionar una Serie donde el nombre coincida.
    statement = select(modelo.Serie).where(modelo.Serie.nombre == nombre)
    #Ejecuta la consulta y devuelve el primer resultado.
    return session.exec(statement).first()

# --- Servicios de Creación (Nuevos) ---

#Define el servicio para crear una nueva Direccion.
def create_direccion(session: Session, direccion_create: esquemas.DireccionCrear) -> modelo.Direccion:
    #Convierte el esquema de entrada (Pydantic) al modelo de BD (SQLModel).
    db_direccion = modelo.Direccion.model_validate(direccion_create)
    #Anade el nuevo objeto a la sesion.
    session.add(db_direccion)
    #Guarda los cambios en la BD.
    session.commit()
    #Refresca el objeto para obtener el ID asignado por la BD.
    session.refresh(db_direccion)
    #Devuelve la direccion recien creada.
    return db_direccion

#Define el servicio para crear una nueva Editorial (con su direccion anidada).
def create_editorial(session: Session, editorial_create: esquemas.EditorialCrear) -> modelo.Editorial:
    # 1. Validar que no exista
    #Usa la funcion de ayuda para verificar si la editorial ya existe.
    if get_editorial_por_nombre(session, editorial_create.nombre):
        #Si existe, lanza un error 409 (Conflicto).
        raise HTTPException(status_code=409, detail="La editorial ya existe")
    
    # 2. Crear la Dirección primero
    #Llama al servicio de crear direccion con los datos anidados de la solicitud.
    db_direccion = create_direccion(session, editorial_create.direccion)
    
    # 3. Crear la Editorial y asignarle el ID de la dirección
    #Convierte los datos de la editorial a un diccionario, excluyendo la direccion anidada.
    editorial_data = editorial_create.model_dump(exclude={"direccion"})
    #Crea la instancia del modelo Editorial, pasando los datos y el 'direccion_id' obtenido.
    db_editorial = modelo.Editorial(**editorial_data, direccion_id=db_direccion.id)
    
    #Anade la nueva editorial a la sesion.
    session.add(db_editorial)
    #Guarda los cambios.
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_editorial)
    #Devuelve la editorial recien creada.
    return db_editorial

#Define el servicio para obtener una Editorial por su ID.
def get_editorial(session: Session, editorial_id: int) -> modelo.Editorial | None:
    """Busca una editorial por su ID."""
    #Usa el metodo .get() de la sesion para buscar por clave primaria.
    return session.get(modelo.Editorial, editorial_id)

#Define el servicio para obtener una lista paginada de todas las Editoriales.
def get_editoriales_todas(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Editorial]:
    """Obtiene una lista de todas las editoriales, con paginación."""
    #Crea una consulta para seleccionar Editoriales, aplicando 'offset' (skip) y 'limit'.
    statement = select(modelo.Editorial).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para actualizar una Editorial (PATCH).
def actualizar_editorial(
    #Recibe la sesion de la BD.
    session: Session, 
    #Recibe el objeto de la editorial que ya fue buscado en la BD.
    db_editorial: modelo.Editorial, 
    #Recibe los datos de actualizacion desde la API.
    editorial_update: esquemas.EditorialActualizar
) -> modelo.Editorial:
    
    # 1. Convierte el esquema de actualización en un diccionario
    # 'exclude_unset=True' es la CLAVE: solo incluye campos que el usuario envió.
    update_data = editorial_update.model_dump(exclude_unset=True)

    # 2. Maneja la actualización de la dirección (si se envió)
    #Comprueba si 'direccion' (la actualizacion anidada) esta en los datos enviados.
    if "direccion" in update_data:
        #Saca los datos de la direccion del diccionario principal.
        direccion_data = update_data.pop("direccion")
        
        #Obtiene el objeto de direccion existente desde la relacion de la editorial.
        db_direccion = db_editorial.direccion
        
        #Si la editorial tiene una direccion asociada.
        if db_direccion:
            #Actualiza cada campo de la direccion (calle, ciudad, etc.).
            for key, value in direccion_data.items():
                setattr(db_direccion, key, value)
            #Anade la direccion modificada a la sesion.
            session.add(db_direccion)

    # 3. Actualiza los campos restantes de la editorial (ej. "nombre")
    #Itera sobre los datos restantes en 'update_data' (solo 'nombre', si se envio).
    for key, value in update_data.items():
        setattr(db_editorial, key, value)

    # 4. Guarda todo en la base de datos
    #Anade la editorial modificada a la sesion.
    session.add(db_editorial)
    #Guarda los cambios (tanto en editorial como en direccion).
    session.commit()
    #Refresca el objeto editorial.
    session.refresh(db_editorial)
    
    #Devuelve la editorial actualizada.
    return db_editorial

#Define el servicio para crear un PublicoObjetivo.
def create_publico_objetivo(session: Session, publico_create: esquemas.PublicoObjetivoCrear) -> modelo.PublicoObjetivo:
    #Usa la funcion de ayuda para verificar si el 'tipo' de publico ya existe.
    if get_publico_objetivo_por_tipo(session, publico_create.tipo):
        #Si existe, lanza un error 409 (Conflicto).
        raise HTTPException(status_code=409, detail="El tipo de público ya existe")
    
    #Convierte el esquema de entrada al modelo de BD.
    db_publico = modelo.PublicoObjetivo.model_validate(publico_create)
    #Anade el objeto a la sesion.
    session.add(db_publico)
    #Guarda los cambios.
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_publico)
    #Devuelve el objeto recien creado.
    return db_publico

#Define el servicio para obtener una lista paginada de PublicoObjetivo.
def get_publicos_objetivo_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.PublicoObjetivo]:
    #Crea una consulta seleccionando PublicoObjetivo, aplicando 'offset' y 'limit'.
    statement = select(modelo.PublicoObjetivo).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para crear una Serie.
def create_serie(session: Session, serie_create: esquemas.SerieCrear) -> modelo.Serie:
    #Usa la funcion de ayuda para verificar si la serie ya existe por nombre.
    if get_serie_por_nombre(session, serie_create.nombre):
        #Si existe, lanza un error 409 (Conflicto).
        raise HTTPException(status_code=409, detail="La serie ya existe")
    
    #Convierte el esquema de entrada al modelo de BD.
    db_serie = modelo.Serie.model_validate(serie_create)
    #Anade el objeto a la sesion.
    session.add(db_serie)
    #Guarda los cambios.
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_serie)
    #Devuelve el objeto recien creado.
    return db_serie

#Define el servicio para obtener una lista paginada de Series.
def get_series_todas(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Serie]:
    #Crea una consulta seleccionando Serie, aplicando 'offset' y 'limit'.
    statement = select(modelo.Serie).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

# --- Servicios de Autor y Categoria (Existentes) ---

#Define el servicio para crear un Autor.
def create_autor(session: Session, autor_create: esquemas.AutorCreacion) -> modelo.Autor:
    #Usa la funcion de ayuda para verificar si el autor ya existe por nombre.
    if get_autor_por_nombre(session, autor_create.nombre):
        #Si existe, lanza un error 409 (Conflicto).
        raise HTTPException(status_code=409, detail="El autor ya existe")
        
    #Convierte el esquema de entrada al modelo de BD.
    db_autor = modelo.Autor.model_validate(autor_create)
    #Anade el objeto a la sesion.
    session.add(db_autor)
    #Guarda los cambios.
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_autor)
    #Devuelve el objeto recien creado.
    return db_autor

#Define el servicio para obtener un Autor por su ID.
def get_autor(session: Session, autor_id: int) -> modelo.Autor | None:
    #Usa el metodo .get() de la sesion para buscar por clave primaria.
    return session.get(modelo.Autor, autor_id)

#Define el servicio para obtener una lista paginada de Autores.
def get_autores_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Autor]:
    #Crea una consulta seleccionando Autor, aplicando 'offset' y 'limit'.
    statement = select(modelo.Autor).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para crear una Categoria.
def create_categoria(session: Session, categoria_create: esquemas.CategoriaCrear) -> modelo.Categoria:
    #Usa la funcion de ayuda para verificar si la categoria ya existe por nombre.
    if get_categoria_por_nombre(session, categoria_create.nombre):
        #Si existe, lanza un error 409 (Conflicto).
        raise HTTPException(status_code=409, detail="La categoría ya existe")
    
    #Convierte el esquema de entrada al modelo de BD.
    db_categoria = modelo.Categoria.model_validate(categoria_create)
    #Anade el objeto a la sesion.
    session.add(db_categoria)
    #Guarda los cambios.
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_categoria)
    #Devuelve el objeto recien creado.
    return db_categoria

#Define el servicio para obtener una Categoria por su ID.
def get_categoria(session: Session, categoria_id: int) -> modelo.Categoria | None:
    #Usa el metodo .get() de la sesion para buscar por clave primaria.
    return session.get(modelo.Categoria, categoria_id)

#Define el servicio para obtener una lista paginada de Categorias.
def get_categorias_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Categoria]:
    #Crea una consulta seleccionando Categoria, aplicando 'offset' y 'limit'.
    statement = select(modelo.Categoria).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()


# --- Servicio create_libro (ACTUALIZADO) ---

#Define el servicio para crear un Libro (logica compleja de relaciones).
def create_libro(session: Session, libro_create: esquemas.LibroCreacion) -> modelo.Libro:
    
    # 1. Separar los datos
    #Convierte el esquema de entrada a un diccionario, excluyendo los campos de relacion (nombres).
    libro_data = libro_create.model_dump(exclude={
        "autores_nombres", "categorias_nombres",
        "editorial_nombre", "publico_objetivo_tipo", "serie_nombre"
    })
    #Crea la instancia del modelo Libro solo con los datos base (titulo, precio, etc.).
    db_libro = modelo.Libro(**libro_data)
    
    # 2. Asignar Editorial por NOMBRE
    #Si se proporciono un nombre de editorial.
    if libro_create.editorial_nombre:
        #Usa la funcion de ayuda para buscar la editorial por su nombre.
        editorial = get_editorial_por_nombre(session, libro_create.editorial_nombre)
        #Si la editorial no se encuentra.
        if not editorial:
            #Lanza un error 404.
            raise HTTPException(status_code=404, detail=f"Editorial '{libro_create.editorial_nombre}' no encontrada")
        #Asigna el objeto 'editorial' completo a la relacion del libro.
        db_libro.editorial = editorial # Asignamos el objeto, no el ID

    # 3. Asignar Publico Objetivo por TIPO
    #Si se proporciono un tipo de publico.
    if libro_create.publico_objetivo_tipo:
        #Usa la funcion de ayuda para buscar el publico por su tipo.
        publico = get_publico_objetivo_por_tipo(session, libro_create.publico_objetivo_tipo)
        #Si no se encuentra.
        if not publico:
            #Lanza un error 404.
            raise HTTPException(status_code=404, detail=f"Público '{libro_create.publico_objetivo_tipo}' no encontrado")
        #Asigna el objeto 'publico' completo a la relacion del libro.
        db_libro.publico_objetivo = publico

    # 4. Asignar Serie por NOMBRE
    #Si se proporciono un nombre de serie.
    if libro_create.serie_nombre:
        #Usa la funcion de ayuda para buscar la serie por su nombre.
        serie = get_serie_por_nombre(session, libro_create.serie_nombre)
        #Si no se encuentra.
        if not serie:
            #Lanza un error 404.
            raise HTTPException(status_code=404, detail=f"Serie '{libro_create.serie_nombre}' no encontrada")
        #Asigna el objeto 'serie' completo a la relacion del libro.
        db_libro.serie = serie

    # 5. Asignar Autores por NOMBRE
    #Itera sobre la lista de nombres de autores proporcionada.
    for autor_nombre in libro_create.autores_nombres:
        #Usa la funcion de ayuda para buscar cada autor por su nombre.
        autor = get_autor_por_nombre(session, autor_nombre)
        #Si el autor no se encuentra.
        if not autor:
            #Lanza un error 404.
            raise HTTPException(status_code=404, detail=f"Autor '{autor_nombre}' no encontrado")
        #Anade el objeto 'autor' encontrado a la lista 'autores' del libro (M2M).
        db_libro.autores.append(autor)
            
    # 6. Asignar Categorías por NOMBRE
    #Itera sobre la lista de nombres de categorias proporcionada.
    for categoria_nombre in libro_create.categorias_nombres:
        #Usa la funcion de ayuda para buscar cada categoria por su nombre.
        categoria = get_categoria_por_nombre(session, categoria_nombre)
        #Si la categoria no se encuentra.
        if not categoria:
            #Lanza un error 404.
            raise HTTPException(status_code=404, detail=f"Categoría '{categoria_nombre}' no encontrada")
        #Anade el objeto 'categoria' encontrado a la lista 'categorias' del libro (M2M).
        db_libro.categorias.append(categoria)
            
    # 7. Guardar en la BD
    #Anade el objeto 'db_libro' (con todas sus relaciones) a la sesion.
    session.add(db_libro)
    #Guarda los cambios (SQLModel/SQLAlchemy se encarga de las tablas de enlace).
    session.commit()
    #Refresca el objeto para obtener su ID.
    session.refresh(db_libro)
    #Devuelve el libro recien creado.
    return db_libro

# --- Servicios "Get Libros" ---

#Define el servicio para obtener una lista paginada de todos los Libros.
def get_libros_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    #Crea una consulta seleccionando Libro, aplicando 'offset' y 'limit'.
    statement = select(modelo.Libro).offset(skip).limit(limit)
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para obtener libros filtrados por autor (con JOIN).
def get_libros_por_autor(session: Session, nombre_autor: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    #Crea una consulta compleja con JOINs.
    statement = (
        #Selecciona 'Libro'
        select(modelo.Libro)
        #Une con la tabla de enlace 'LibroAutorLink'.
        .join(modelo.LibroAutorLink)
        #Une con la tabla 'Autor'.
        .join(modelo.Autor)
        #Filtra donde el nombre del Autor coincida.
        .where(modelo.Autor.nombre == nombre_autor)
        #Aplica paginacion.
        .offset(skip).limit(limit)
    )
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para obtener libros filtrados por categoria (con JOIN).
def get_libros_por_categoria(session: Session, genero: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    #Crea una consulta compleja con JOINs.
    statement = (
        #Selecciona 'Libro'
        select(modelo.Libro)
        #Une con la tabla de enlace 'LibroCategoriaLink'.
        .join(modelo.LibroCategoriaLink)
        #Une con la tabla 'Categoria'.
        .join(modelo.Categoria)
        #Filtra donde el nombre de la Categoria coincida (variable 'genero').
        .where(modelo.Categoria.nombre == genero)
        #Aplica paginacion.
        .offset(skip).limit(limit)
    )
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para obtener libros filtrados por serie (con JOIN).
def get_libros_por_serie(session: Session, nombre_serie: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    #Crea una consulta con JOIN (SQLModel infiere el JOIN simple).
    statement = (
        #Selecciona 'Libro'
        select(modelo.Libro)
        #Une con la tabla 'Serie' (usando la FK 'serie_id').
        .join(modelo.Serie)
        #Filtra donde el nombre de la Serie coincida.
        .where(modelo.Serie.nombre == nombre_serie)
        #Aplica paginacion.
        .offset(skip).limit(limit)
    )
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

#Define el servicio para obtener libros filtrados por publico (con JOIN).
def get_libros_por_publico(session: Session, tipo_publico: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    #Crea una consulta con JOIN.
    statement = (
        #Selecciona 'Libro'
        select(modelo.Libro)
        #Une con la tabla 'PublicoObjetivo' (usando la FK).
        .join(modelo.PublicoObjetivo)
        #Filtra donde el tipo de PublicoObjetivo coincida.
        .where(modelo.PublicoObjetivo.tipo == tipo_publico)
        #Aplica paginacion.
        .offset(skip).limit(limit)
    )
    #Ejecuta la consulta y devuelve todos los resultados.
    return session.exec(statement).all()

# (Añade esto en Servicios/servicios.py)

#Define el servicio para obtener un Libro por su ISBN.
def get_libro_por_isbn(session: Session, isbn: str) -> Optional[modelo.Libro]:
    """Busca un libro por su ISBN."""
    #Crea una consulta para seleccionar un Libro donde el ISBN coincida.
    statement = select(modelo.Libro).where(modelo.Libro.isbn == isbn)
    #Ejecuta la consulta y devuelve el primer resultado (o None).
    libro = session.exec(statement).first()
    #Devuelve el libro encontrado.
    return libro