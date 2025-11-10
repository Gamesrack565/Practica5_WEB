# Servicios/servicios.py
from sqlmodel import Session, select
from typing import List, Optional
from Modelo import modelo
from Esquemas import esquemas
from fastapi import HTTPException

# --- Funciones Helper "Get by Name" ---

def get_autor_por_nombre(session: Session, nombre: str) -> Optional[modelo.Autor]:
    statement = select(modelo.Autor).where(modelo.Autor.nombre == nombre)
    return session.exec(statement).first()

def get_categoria_por_nombre(session: Session, nombre: str) -> Optional[modelo.Categoria]:
    statement = select(modelo.Categoria).where(modelo.Categoria.nombre == nombre)
    return session.exec(statement).first()

def get_editorial_por_nombre(session: Session, nombre: str) -> Optional[modelo.Editorial]:
    statement = select(modelo.Editorial).where(modelo.Editorial.nombre == nombre)
    return session.exec(statement).first()

def get_publico_objetivo_por_tipo(session: Session, tipo: str) -> Optional[modelo.PublicoObjetivo]:
    statement = select(modelo.PublicoObjetivo).where(modelo.PublicoObjetivo.tipo == tipo)
    return session.exec(statement).first()

def get_serie_por_nombre(session: Session, nombre: str) -> Optional[modelo.Serie]:
    statement = select(modelo.Serie).where(modelo.Serie.nombre == nombre)
    return session.exec(statement).first()

# --- Servicios de Creación (Nuevos) ---

def create_direccion(session: Session, direccion_create: esquemas.DireccionCrear) -> modelo.Direccion:
    db_direccion = modelo.Direccion.model_validate(direccion_create)
    session.add(db_direccion)
    session.commit()
    session.refresh(db_direccion)
    return db_direccion

def create_editorial(session: Session, editorial_create: esquemas.EditorialCrear) -> modelo.Editorial:
    # 1. Validar que no exista
    if get_editorial_por_nombre(session, editorial_create.nombre):
        raise HTTPException(status_code=409, detail="La editorial ya existe")
    
    # 2. Crear la Dirección primero
    db_direccion = create_direccion(session, editorial_create.direccion)
    
    # 3. Crear la Editorial y asignarle el ID de la dirección
    editorial_data = editorial_create.model_dump(exclude={"direccion"})
    db_editorial = modelo.Editorial(**editorial_data, direccion_id=db_direccion.id)
    
    session.add(db_editorial)
    session.commit()
    session.refresh(db_editorial)
    return db_editorial

def get_editorial(session: Session, editorial_id: int) -> modelo.Editorial | None:
    """Busca una editorial por su ID."""
    return session.get(modelo.Editorial, editorial_id)

def get_editoriales_todas(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Editorial]:
    """Obtiene una lista de todas las editoriales, con paginación."""
    statement = select(modelo.Editorial).offset(skip).limit(limit)
    return session.exec(statement).all()

# (Añade esto en Servicios/servicios.py, junto a las otras funciones de Editorial)

def actualizar_editorial(
    session: Session, 
    db_editorial: modelo.Editorial, 
    editorial_update: esquemas.EditorialActualizar
) -> modelo.Editorial:
    
    # 1. Convierte el esquema de actualización en un diccionario
    #    exclude_unset=True es la CLAVE: solo incluye campos que el usuario envió
    update_data = editorial_update.model_dump(exclude_unset=True)

    # 2. Maneja la actualización de la dirección (si se envió)
    if "direccion" in update_data:
        # Saca los datos de la dirección del diccionario principal
        direccion_data = update_data.pop("direccion")
        
        # Obtiene el objeto de dirección existente
        db_direccion = db_editorial.direccion
        
        if db_direccion:
            # Actualiza cada campo de la dirección
            for key, value in direccion_data.items():
                setattr(db_direccion, key, value)
            session.add(db_direccion)

    # 3. Actualiza los campos restantes de la editorial (ej. "nombre")
    for key, value in update_data.items():
        setattr(db_editorial, key, value)

    # 4. Guarda todo en la base de datos
    session.add(db_editorial)
    session.commit()
    session.refresh(db_editorial)
    
    return db_editorial

def create_publico_objetivo(session: Session, publico_create: esquemas.PublicoObjetivoCrear) -> modelo.PublicoObjetivo:
    if get_publico_objetivo_por_tipo(session, publico_create.tipo):
        raise HTTPException(status_code=409, detail="El tipo de público ya existe")
    
    db_publico = modelo.PublicoObjetivo.model_validate(publico_create)
    session.add(db_publico)
    session.commit()
    session.refresh(db_publico)
    return db_publico

def get_publicos_objetivo_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.PublicoObjetivo]:
    statement = select(modelo.PublicoObjetivo).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_serie(session: Session, serie_create: esquemas.SerieCrear) -> modelo.Serie:
    if get_serie_por_nombre(session, serie_create.nombre):
        raise HTTPException(status_code=409, detail="La serie ya existe")
    
    db_serie = modelo.Serie.model_validate(serie_create)
    session.add(db_serie)
    session.commit()
    session.refresh(db_serie)
    return db_serie

def get_series_todas(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Serie]:
    statement = select(modelo.Serie).offset(skip).limit(limit)
    return session.exec(statement).all()

# --- Servicios de Autor y Categoria (Existentes) ---

def create_autor(session: Session, autor_create: esquemas.AutorCreacion) -> modelo.Autor:
    if get_autor_por_nombre(session, autor_create.nombre):
        raise HTTPException(status_code=409, detail="El autor ya existe")
        
    db_autor = modelo.Autor.model_validate(autor_create)
    session.add(db_autor)
    session.commit()
    session.refresh(db_autor)
    return db_autor

def get_autor(session: Session, autor_id: int) -> modelo.Autor | None:
    return session.get(modelo.Autor, autor_id)

def get_autores_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Autor]:
    statement = select(modelo.Autor).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_categoria(session: Session, categoria_create: esquemas.CategoriaCrear) -> modelo.Categoria:
    if get_categoria_por_nombre(session, categoria_create.nombre):
        raise HTTPException(status_code=409, detail="La categoría ya existe")
    
    db_categoria = modelo.Categoria.model_validate(categoria_create)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria

def get_categoria(session: Session, categoria_id: int) -> modelo.Categoria | None:
    return session.get(modelo.Categoria, categoria_id)

def get_categorias_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Categoria]:
    statement = select(modelo.Categoria).offset(skip).limit(limit)
    return session.exec(statement).all()


# --- Servicio create_libro (ACTUALIZADO) ---

def create_libro(session: Session, libro_create: esquemas.LibroCreacion) -> modelo.Libro:
    
    # 1. Separar los datos
    libro_data = libro_create.model_dump(exclude={
        "autores_nombres", "categorias_nombres",
        "editorial_nombre", "publico_objetivo_tipo", "serie_nombre"
    })
    db_libro = modelo.Libro(**libro_data)
    
    # 2. Asignar Editorial por NOMBRE
    if libro_create.editorial_nombre:
        editorial = get_editorial_por_nombre(session, libro_create.editorial_nombre)
        if not editorial:
            raise HTTPException(status_code=404, detail=f"Editorial '{libro_create.editorial_nombre}' no encontrada")
        db_libro.editorial = editorial # Asignamos el objeto, no el ID

    # 3. Asignar Publico Objetivo por TIPO
    if libro_create.publico_objetivo_tipo:
        publico = get_publico_objetivo_por_tipo(session, libro_create.publico_objetivo_tipo)
        if not publico:
            raise HTTPException(status_code=404, detail=f"Público '{libro_create.publico_objetivo_tipo}' no encontrado")
        db_libro.publico_objetivo = publico

    # 4. Asignar Serie por NOMBRE
    if libro_create.serie_nombre:
        serie = get_serie_por_nombre(session, libro_create.serie_nombre)
        if not serie:
            raise HTTPException(status_code=404, detail=f"Serie '{libro_create.serie_nombre}' no encontrada")
        db_libro.serie = serie

    # 5. Asignar Autores por NOMBRE
    for autor_nombre in libro_create.autores_nombres:
        autor = get_autor_por_nombre(session, autor_nombre)
        if not autor:
            raise HTTPException(status_code=404, detail=f"Autor '{autor_nombre}' no encontrado")
        db_libro.autores.append(autor)
            
    # 6. Asignar Categorías por NOMBRE
    for categoria_nombre in libro_create.categorias_nombres:
        categoria = get_categoria_por_nombre(session, categoria_nombre)
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Categoría '{categoria_nombre}' no encontrada")
        db_libro.categorias.append(categoria)
            
    # 7. Guardar en la BD
    session.add(db_libro)
    session.commit()
    session.refresh(db_libro)
    return db_libro

# --- Servicios "Get Libros" (Sin cambios, ya funcionaban con JOIN) ---
# ... (get_libros_todos, get_libros_por_autor, etc. van aquí) ...
# (Asegúrate de que tus funciones 'get_libros_por...' estén aquí)

def get_libros_todos(session: Session, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    statement = select(modelo.Libro).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_libros_por_autor(session: Session, nombre_autor: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    statement = (
        select(modelo.Libro).join(modelo.LibroAutorLink).join(modelo.Autor)
        .where(modelo.Autor.nombre == nombre_autor).offset(skip).limit(limit)
    )
    return session.exec(statement).all()

def get_libros_por_categoria(session: Session, genero: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    statement = (
        select(modelo.Libro).join(modelo.LibroCategoriaLink).join(modelo.Categoria)
        .where(modelo.Categoria.nombre == genero).offset(skip).limit(limit)
    )
    return session.exec(statement).all()

def get_libros_por_serie(session: Session, nombre_serie: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    statement = (
        select(modelo.Libro).join(modelo.Serie)
        .where(modelo.Serie.nombre == nombre_serie).offset(skip).limit(limit)
    )
    return session.exec(statement).all()

def get_libros_por_publico(session: Session, tipo_publico: str, skip: int = 0, limit: int = 10) -> List[modelo.Libro]:
    statement = (
        select(modelo.Libro).join(modelo.PublicoObjetivo)
        .where(modelo.PublicoObjetivo.tipo == tipo_publico).offset(skip).limit(limit)
    )
    return session.exec(statement).all()

# (Añade esto en Servicios/servicios.py)

def get_libro_por_isbn(session: Session, isbn: str) -> Optional[modelo.Libro]:
    """Busca un libro por su ISBN."""
    statement = select(modelo.Libro).where(modelo.Libro.isbn == isbn)
    libro = session.exec(statement).first()
    return libro