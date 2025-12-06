# Importaciones necesarias al inicio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# Importa tus módulos locales
from Servicios.database import create_db_and_tables, engine
from Modelo import modelo
from Servicios import servicios
from Esquemas import esquemas


# --- LÓGICA DE CARGA INICIAL (SEMILLA) ---
def crear_datos_prueba():
    """Crea editoriales, categorías y autores base si no existen."""
    with Session(engine) as session:
        # 1. Verificar si ya hay editoriales (para no duplicar)
        if session.exec(select(modelo.Editorial)).first():
            print("La base de datos ya tiene datos. Saltando carga inicial.")
            return

        print("Base de datos vacía. Creando datos de prueba...")

        # 2. Crear Editoriales (Con sus direcciones obligatorias)
        # Editorial Alfaguara
        dir_alfaguara = esquemas.DireccionCrear(
            calle="Calle Juan Bravo 38", ciudad_pais="Madrid, España", codigo_postal="28006"
        )
        edit_alfaguara = esquemas.EditorialCrear(nombre="Alfaguara", direccion=dir_alfaguara)
        servicios.create_editorial(session, edit_alfaguara)

        # Editorial Salamandra
        dir_salamandra = esquemas.DireccionCrear(
            calle="Av. Diagonal 662", ciudad_pais="Barcelona, España", codigo_postal="08034"
        )
        edit_salamandra = esquemas.EditorialCrear(nombre="Salamandra", direccion=dir_salamandra)
        servicios.create_editorial(session, edit_salamandra)

        # 3. Crear Categorías
        cats = ["Ficción", "Novela", "Terror", "Fantasía", "Ciencia", "Historia"]
        for nombre_cat in cats:
            servicios.create_categoria(session, esquemas.CategoriaCrear(nombre=nombre_cat))

        # 4. Crear Autores
        autores = ["J.K. Rowling", "Miguel de Cervantes", "Stephen King", "Gabriel García Márquez"]
        for nombre_autor in autores:
            servicios.create_autor(session, esquemas.AutorCreacion(nombre=nombre_autor))

        # 5. Crear Públicos Objetivo (Importante para tu esquema)
        publicos = ["General", "+18", "Infantil", "Juvenil"]
        for tipo in publicos:
            servicios.create_publico_objetivo(session, esquemas.PublicoObjetivoCrear(tipo=tipo))

        print("Datos de prueba cargados correctamente.")


# --- CICLO DE VIDA (LIFESPAN) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Crear Tablas
    create_db_and_tables()

    # 2. Cargar Datos de Prueba (NUEVO)
    crear_datos_prueba()

    yield
    print("Apagando aplicación...")


# --- APP FASTAPI ---
app = FastAPI(lifespan=lifespan)

# Configuración CORS (Mantenla como la tenías)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUIR TUS RUTAS ---
# (Asegúrate de importar tus routers aquí, ejemplo:)
from Rutas import libros, autores, editoriales, categorias, publico_objetivo, series

app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(editoriales.router)
app.include_router(categorias.router)
app.include_router(publico_objetivo.router)
app.include_router(series.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)