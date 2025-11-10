# database.py
from sqlmodel import SQLModel, create_engine, Session

# Usaremos un archivo de base de datos SQLite
DATABASE_URL = "sqlite:///./libreria.db"

# El "engine" es el punto de conexión central
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Esto crea todas las tablas definidas con SQLModel
    SQLModel.metadata.create_all(engine)

# Función "Dependency" para obtener una sesión de BD por cada petición
def get_session():
    with Session(engine) as session:
        yield session