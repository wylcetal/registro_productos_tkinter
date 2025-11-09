from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

# Base declarativa para SQLAlchemy
Base = declarative_base()


class ProductoModel(Base):
    """
    Representa el modelo de la tabla 'producto' en la base de datos.

    Atributos:
        id (Integer): Identificador único del producto.
        nombre (String): Nombre del producto (máx 150 caracteres).
        precio (Float): Precio de venta del producto.
    """

    __tablename__ = "producto"
    # Columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150))
    precio = Column(Float)

    def __repr__(self) -> str:
        return (
            f"<ProductoModel(id={self.id}, nombre={self.nombre}, precio={self.precio})>"
        )

    def __str__(self) -> str:
        return f"producto({self.id}, {self.nombre}, {self.precio})"
