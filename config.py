"""Configuración global de la aplicación.

Centraliza parámetros como la URL de base de datos y niveles de logging.
"""

from utils.generico import crear_db

# URL de conexión SQLite (compatibilidad Windows con rutas POSIX)
DB_URL: str = f"sqlite:///{crear_db().as_posix()}"

# Nivel de logging por defecto (usar en `logging.basicConfig` si se desea)
LOG_LEVEL: str = "INFO"