from pathlib import Path


def crear_db() -> Path:
    """Crea (si no existe) y devuelve la ruta del archivo de base de datos.

    La base se ubica en la carpeta ``db`` del proyecto.
    """
    base_dir = Path(__file__).resolve().parent.parent
    db_dir = base_dir / "db"
    db_dir.mkdir(exist_ok=True, parents=True)
    db_path = db_dir / "registro_producto.db"
    return db_path
