"""Script para construcción/creación de tablas de base de datos.

Ejecuta la inicialización del esquema usando SQLAlchemy declarativo.
"""

from sqlalchemy import create_engine

import utils.generico as generico
from models.entities import Base


def main() -> None:
    # Crear la base de datos
    db_path = generico.crear_db()

    # Crear motor de base de datos con configuración optimizada y compatibilidad Windows
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}", echo=False, future=True, pool_pre_ping=True
    )

    # Crear todas las tablas si no existen
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
