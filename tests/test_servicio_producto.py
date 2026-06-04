import unittest
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.entities import Base, Producto
from services.servicio_producto import ServicioProducto


class TestServicioProducto(unittest.TestCase):
    def setUp(self) -> None:
        # Engine en memoria para pruebas aisladas
        self.engine = create_engine("sqlite:///:memory:", future=True)
        Base.metadata.create_all(self.engine)
        self.servicio = ServicioProducto(engine=self.engine)

    def tearDown(self) -> None:
        self.engine.dispose()

    def test_registrar_producto_valido(self) -> None:
        self.servicio.registrar("Teclado", 99.9)
        with Session(self.engine) as session:
            productos = session.query(Producto).all()
            self.assertEqual(len(productos), 1)
            self.assertEqual(productos[0].nombre, "Teclado")

    def test_registrar_producto_invalido_precio(self) -> None:
        with self.assertRaises(ValueError):
            self.servicio.registrar("Mouse", -1.0)

    def test_modificar_producto_existente(self) -> None:
        # Prepara producto
        with Session(self.engine) as session:
            p = Producto(nombre="Pantalla", precio=150.0)
            session.add(p)
            session.commit()
            producto_id = p.id
        # Modifica
        ok = self.servicio.modificar("Pantalla HD", 175.5, producto_id)
        self.assertTrue(ok)
        with Session(self.engine) as session:
            p = session.query(Producto).filter_by(id=producto_id).first()
            self.assertIsNotNone(p)
            self.assertEqual(p.nombre, "Pantalla HD")
            self.assertEqual(p.precio, 175.5)

    def test_modificar_producto_no_existente(self) -> None:
        ok = self.servicio.modificar("Nada", 10.0, 999)
        self.assertFalse(ok)

    def test_eliminar_producto_existente(self) -> None:
        with Session(self.engine) as session:
            p = Producto(nombre="Cable", precio=5.0)
            session.add(p)
            session.commit()
            producto_id = p.id
        ok = self.servicio.eliminar(producto_id)
        self.assertTrue(ok)
        with Session(self.engine) as session:
            p = session.query(Producto).filter_by(id=producto_id).first()
            self.assertIsNone(p)

    def test_eliminar_producto_no_existente(self) -> None:
        ok = self.servicio.eliminar(999)
        self.assertFalse(ok)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
