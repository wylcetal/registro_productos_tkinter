"""
Controlador principal de la aplicación
Implementa el patrón MVC - Coordina vistas y lógica de negocio
"""

import tkinter as tk

from services.servicio_producto import ServicioProducto
from src.ui.components import ConfirmDialog
from src.utils.validators import FormValidator


class AppController:
    """
    Controlador principal de la aplicación
    Sigue el principio de Responsabilidad Única (SOLID)
    Coordina entre servicios de negocio y vistas
    """

    def __init__(self, root: tk.Tk):
        """
        Inicializa el controlador de la aplicación

        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root

        # Servicios
        self.test_product = ServicioProducto()

        # Validador
        self.validator = FormValidator()

    # ==================== GESTIÓN DE PRODUCTO ====================
    def obtener_conf_btn_pack(self) -> dict:
        """Configuración de empaquetado para botones de acciones."""
        return {"side": tk.RIGHT, "padx": 10, "pady": 10}

    def registrar_producto(self, nombre: str, precio: str):
        # validar nombre
        validation = self.validator.validate_product_name(nombre)
        if not validation.is_valid:
            ConfirmDialog.show_error("Error", validation.error_message)
            return False

        # validar precio
        validation = self.validator.validate_float(precio, min_value=0)
        if not validation.is_valid:
            ConfirmDialog.show_error("Error", validation.error_message)
            return False

        try:
            precio = float(precio)
            self.test_product.registrar(nombre, precio)
            ConfirmDialog.show_info("Success", "Producto registrado exitosamente.")
        except ValueError as e:
            ConfirmDialog.show_error("Error", str(e))
        except Exception as e:
            ConfirmDialog.show_error("Error", f"Ocurrió un error: {e}")

    def actualizar_lista(self):
        try:
            productos = self.test_product.obtener_productos()
            if not productos:
                ConfirmDialog.show_error("Error", "No hay productos registrados.")
            return productos
        except Exception as e:
            ConfirmDialog.show_error("Error", f"Ocurrió un error: {e}")

    def modificar_producto(self, id_sel, nombre: str, precio: str):
        # validar nombre
        validation = self.validator.validate_product_name(nombre)
        if not validation.is_valid:
            ConfirmDialog.show_error("Error", validation.error_message)
            return False

        # validar precio
        validation = self.validator.validate_float(precio, min_value=0)
        if not validation.is_valid:
            ConfirmDialog.show_error("Error", validation.error_message)
            return False

        try:
            precio = float(precio)
            id_sel = int(id_sel)
            self.test_product.modificar(nombre, precio, id_sel)
            ConfirmDialog.show_info("Success", "Producto modificado exitosamente.")
        except ValueError as e:
            ConfirmDialog.show_error("Error", str(e))
        except Exception as e:
            ConfirmDialog.show_error("Error", f"Ocurrió un error: {e}")

    def eliminar_producto(self, id_sel):
        try:
            if id_sel is None:
                ConfirmDialog.show_error("Error", "Por favor selecciona una fila.")
                return
            self.test_product.eliminar(id_sel)
            ConfirmDialog.show_info("Success", "Producto eliminado exitosamente.")
        except Exception as e:
            ConfirmDialog.show_error("Error", f"Por favor selecciona una fila: {e}")

    def validar_precio_entry(self, nuevo_valor: str) -> bool:
        """Valida el contenido del campo precio (solo números y punto).

        Permite vacío para que el usuario pueda borrar, y valida formato float.
        """
        if nuevo_valor == "":
            return True
        try:
            float(nuevo_valor)
            return True
        except ValueError:
            self.bell()
            return False
