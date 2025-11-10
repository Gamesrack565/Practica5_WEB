# main.py
from fastapi import FastAPI
from Servicios.database import create_db_and_tables
from Rutas import rutas

app = FastAPI(
    title="API de Catálogo de Librería",
    description="Proyecto para gestionar los libros de una librería."
)

@app.on_event("startup")
def on_startup():
    # Esta función se ejecuta al iniciar la app
    # y crea la base de datos y las tablas
    create_db_and_tables()

# Incluimos las rutas que definimos en rutas.py
app.include_router(rutas.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de la Librería"}