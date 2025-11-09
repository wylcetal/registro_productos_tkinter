from pathlib import Path


def crear_db():
    base_dir = Path(__file__).resolve().parent.parent
    db_dir = base_dir / "db"
    db_dir.mkdir(exist_ok=True, parents=True)
    db_path = db_dir / "registro_producto.db"
    return db_path
