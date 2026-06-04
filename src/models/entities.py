from sqlalchemy import Column, Float, Integer, String, CheckConstraint
from sqlalchemy.orm import declarative_base

# Base declarativa para SQLAlchemy
Base = declarative_base()


class Producto(Base):
    """
    Representa el modelo de la tabla 'producto' en la base de datos.

    Atributos:
        id (Integer): Identificador único del producto.
        nombre (String): Nombre del producto (máx 150 caracteres).
        precio (Float): Precio de venta del producto.
    """

    __tablename__ = "producto"
    __table_args__ = (CheckConstraint("precio >= 0", name="ck_precio_no_negativo"),)

    # Columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    precio = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Producto(id={self.id}, nombre={self.nombre}, precio={self.precio})>"

    def __str__(self) -> str:
        return f"producto({self.id}, {self.nombre}, {self.precio})"

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
        }
