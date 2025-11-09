from sqlalchemy import create_engine

import utils.generico as generico
from dominio.modelos import Base

# Crear la base de datos
db_path = generico.crear_db()

# Crear motor de base de datos con configuración optimizada
engine = create_engine(f"sqlite:///{db_path}", echo=True, future=True)

# Crear todas las tablas si no existen
Base.metadata.create_all(engine)
