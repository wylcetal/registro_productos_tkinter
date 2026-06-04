from tkinter import messagebox
from typing import Optional

from form.registro_form_design import FormularRegistroDesign
from services.servicio_producto import ServicioProducto


class FormularioRegistro(FormularRegistroDesign):
    """Controlador de la UI que implementa la lógica del registro."""

    def __init__(self) -> None:
        self.servicio_producto = ServicioProducto()
        super().__init__()

    def _obtener_seleccion_id(self) -> Optional[int]:
        """Obtiene el ID del producto seleccionado en el Treeview.

        Devuelve ``None`` si no hay selección.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        try:
            return int(self.tree.item(seleccion[0])["values"][0])
        except Exception:
            return None

    def registrar_producto(self) -> None:
        nombre = self.campo_nombre.get()
        precio = self.campo_precio.get()

        if not nombre or not precio:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        try:
            precio = float(precio)
            if precio < 0:
                messagebox.showerror("Error", "El precio debe ser positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        try:
            self.servicio_producto.registrar(nombre, precio)
            messagebox.showinfo("Success", "Producto registrado exitosamente.")
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            self.limpiar_campos()

    def actualizar_lista(self) -> None:
        registros = self.tree.get_children()
        for registro in registros:
            self.tree.delete(registro)
        productos = self.servicio_producto.obtener_productos()
        for ref, producto in enumerate(productos):
            color = ("evenrow",) if ref % 2 == 0 else ("oddrow",)
            self.tree.insert(
                parent="",
                index=ref,
                iid=ref,
                text="",
                tags=color,
                values=(producto.id, producto.nombre, f"{producto.precio:.2f}"),
            )

    def al_seleccionar_treeview(self, event) -> None:
        seleccion = event.widget.selection()
        if seleccion:
            item = event.widget.item(seleccion[0], "values")
            if item:
                self.limpiar_campos()
                self.campo_id.config(state="normal")
                self.campo_id.insert(0, item[0])
                self.campo_id.config(state="readonly")
                self.campo_nombre.insert(0, item[1])
                self.campo_precio.insert(0, item[2])
                self.btn_eliminar.pack(**self.obtener_conf_btn_pack())
                self.btn_modificar.pack(**self.obtener_conf_btn_pack())
                self.btn_registro.pack_forget()

    def modificar_producto(self) -> None:
        try:
            id_sel = self._obtener_seleccion_id()
            if id_sel is None:
                messagebox.showerror("Error", "Por favor selecciona una fila.")
                return
            nombre = self.campo_nombre.get()
            precio = self.campo_precio.get()
            try:
                precio = float(precio)
                if precio < 0:
                    messagebox.showerror("Error", "El precio debe ser positivo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")
                return
            self.servicio_producto.modificar(nombre, precio, id_sel)
            self.limpiar_campos()
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Por favor selecciona una fila: {e}")

    def eliminar_producto(self) -> None:
        try:
            id_sel = self._obtener_seleccion_id()
            if id_sel is None:
                messagebox.showerror("Error", "Por favor selecciona una fila.")
                return
            self.servicio_producto.eliminar(id_sel)
            self.limpiar_campos()
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Por favor selecciona una fila: {e}")
