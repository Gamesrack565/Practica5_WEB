#CATALOGO DE LIBRERIA

#Equipo: 
# Beltran Suacedo Axel ALejandro
# Ceron Samperio Lizeth Monserrat
# Higuera Pineda ANgel Abraham
# Lorenzo Silva Abad Rey


from fastapi import FastAPI
from Servicios.database import create_db_and_tables
from Rutas import libros, autores, categorias, editoriales, publico_objetivo, series

app = FastAPI(
    title="API de Catálogo de Librería",
    description="Practica 5: Catalógo de Librería",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    #Esta función se ejecuta al iniciar la app
    #y crea la base de datos y las tablas
    create_db_and_tables()

#Incluimos las rutas que definimos en rutas.py
app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(editoriales.router)       
app.include_router(publico_objetivo.router) 
app.include_router(series.router)          


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de la Librería"}