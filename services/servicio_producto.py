from typing import List, Optional

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from src.models.entities import Producto
from config import DB_URL


logger = logging.getLogger(__name__)


class ServicioProducto:
    """Servicio de negocio para operaciones CRUD sobre productos.

    Encapsula la interacción con la base de datos mediante SQLAlchemy y
    aplica validaciones básicas de dominio.
    """

    def __init__(self, engine: Optional[Engine] = None) -> None:
        """Inicializa el servicio y el engine de base de datos.

        Permite inyectar un ``Engine`` externo (útil para pruebas). Si no se
        proporciona, se crea usando la URL definida en ``config.DB_URL``.
        """
        self.engine = engine or create_engine(DB_URL, future=True, pool_pre_ping=True)

    def _validar_datos(self, nombre: str, precio: float) -> None:
        """Valida datos de entrada de un producto.

        - ``nombre`` debe tener contenido no vacío tras ``strip``.
        - ``precio`` debe ser mayor o igual que 0.

        Lanza ``ValueError`` si la validación falla.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de producto no puede estar vacío.")
        if precio < 0:
            raise ValueError("El precio debe ser mayor o igual a 0.")

    def registrar(self, nombre: str, precio: float) -> None:
        """Registra un nuevo producto.

        Aplica validaciones de dominio antes de persistir.
        """
        self._validar_datos(nombre, precio)
        producto = Producto(nombre=nombre.strip(), precio=precio)
        with Session(self.engine) as session:
            try:
                session.add(producto)
                session.commit()
                logger.info("Producto registrado: %s", producto)
            except Exception as exc:
                session.rollback()
                logger.exception("Error al registrar el producto: %s", exc)
                raise

    def modificar(self, nombre: str, precio: float, producto_id: int) -> bool:
        """Modifica un producto existente.

        Devuelve ``True`` si la operación fue exitosa, ``False`` si el producto no
        fue encontrado. Propaga excepciones no controladas.
        """
        self._validar_datos(nombre, precio)
        with Session(self.engine) as session:
            try:
                producto: Optional[Producto] = (
                    session.query(Producto).filter_by(id=producto_id).first()
                )
                if producto is None:
                    logger.warning("Producto no encontrado: id=%s", producto_id)
                    return False
                producto.nombre = nombre.strip()
                producto.precio = precio
                session.commit()
                logger.info(
                    "Producto modificado exitosamente: id=%s, nombre=%s",
                    producto_id,
                    nombre,
                )
                return True
            except Exception as exc:
                session.rollback()
                logger.exception("Error al modificar el producto: %s", exc)
                raise

    def obtener_productos(self) -> List[Producto]:
        """Obtiene todos los productos registrados."""
        with Session(self.engine) as session:
            productos = session.query(Producto).all()
        return productos

    def eliminar(self, producto_id: int) -> bool:
        """Elimina un producto por su ``id``.

        Devuelve ``True`` si la eliminación fue exitosa, ``False`` si el producto
        no existe.
        """
        with Session(self.engine) as session:
            try:
                producto: Optional[Producto] = (
                    session.query(Producto).filter_by(id=producto_id).first()
                )
                if producto is None:
                    logger.warning("Producto no encontrado: id=%s", producto_id)
                    return False
                session.delete(producto)
                session.commit()
                logger.info("Producto eliminado: id=%s", producto_id)
                return True
            except Exception as exc:
                session.rollback()
                logger.exception("Error al eliminar el producto: %s", exc)
                raise
