from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from dominio.modelos import ProductoModel
from utils.generico import crear_db


class ServicioProducto:
    def __init__(self) -> None:
        # Crear la base de datos si no existe
        db_path = crear_db()
        self.engine = create_engine(f"sqlite:///{db_path}")

    def registrar(self, nombre: str, precio: float) -> None:
        producto = ProductoModel(nombre=nombre, precio=precio)
        with Session(self.engine) as session:
            session.add(producto)
            session.commit()

    def modificar(self, nombre: str, precio: float, producto_id: int) -> None:
        try:
            with Session(self.engine) as session:
                producto = (
                    session.query(ProductoModel).filter_by(id=producto_id).first()
                )
                producto.nombre = nombre
                producto.precio = precio
                session.commit()
                print(f"El producto {nombre}ha sido modificado exitosamente")
                return True
        except NoResultFound:
            print(f"Producto con ID {producto_id} no encontrado")
            return False
        except Exception as e:  # Capturar cualquier otra excepción
            print(f"Error al modificar el producto: {e}")
            return False

    def obtener_productos(self) -> List[ProductoModel]:
        with Session(self.engine) as session:
            productos = session.query(ProductoModel).all()
        return productos

    def eliminar(self, producto_id: int) -> bool:
        try:
            with Session(self.engine) as session:
                producto = (
                    session.query(ProductoModel).filter_by(id=producto_id).first()
                )
                session.delete(producto)
                session.commit()
                print(f"Producto con ID {producto_id} eliminado exitosamente")
                return True
        except NoResultFound:
            print(f"Producto con ID {producto_id} no encontrado")
            session.rollback()  # Deshacer cambios en caso de error
            return False
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            session.rollback()  # Deshacer cambios en caso de error
            return False
