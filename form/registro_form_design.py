import tkinter as tk
from tkinter import messagebox, ttk

from utils.util_ventana import centrar_ventana

COLOR_FONDO = "#fff"
COLOR_FONDO_BUSQUEDA = "#f7f8fa"


class FormularRegistroDesign(tk.Tk):
    """Ventana base que define el diseño y controles del registro de productos."""

    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.crear_paneles()
        self.crear_controles()

    def config_window(self) -> None:
        """Configura parámetros generales de la ventana."""
        self.title("Registro de Productos")
        w, h = 880, 540
        centrar_ventana(self, w, h)
        self.configure(bg=COLOR_FONDO_BUSQUEDA)

    def obtener_conf_btn_pack(self) -> dict:
        """Configuración de empaquetado para botones de acciones."""
        return {"side": tk.RIGHT, "padx": 10, "pady": 10}

    def crear_paneles(self) -> None:
        self.marco_titulo = tk.Frame(self, bg=COLOR_FONDO_BUSQUEDA, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill="both")

        self.marco_registro = tk.Frame(self, bg=COLOR_FONDO, height=50)
        self.marco_registro.pack(side=tk.TOP, fill="both", pady=10)

        self.marco_acciones = tk.Frame(self, bg=COLOR_FONDO, height=50)
        self.marco_acciones.pack(side=tk.TOP, fill="both")

        self.marco_productos = tk.Frame(self, bg=COLOR_FONDO)
        self.marco_productos.pack(
            side=tk.TOP, fill="both", padx=30, pady=15, expand=True
        )

    def crear_controles(self) -> None:
        title = tk.Label(
            self.marco_titulo,
            text="REGISTRO DE PRODUCTO",
            font=("Roboto", 20),
            fg="#485159",
            bg=COLOR_FONDO_BUSQUEDA,
            pady=20,
        )
        title.pack(expand=True, fill=tk.BOTH)

        # Id
        etiqueta_id = tk.Label(
            self.marco_registro,
            text="Id:",
            font=("Times", 14),
            fg="#666a88",
            bg=COLOR_FONDO,
            width=5,
        )
        etiqueta_id.pack(side="left", padx=5, pady=10)

        self.campo_id = ttk.Entry(
            self.marco_registro,
            font=("Times", 14),
            state="readonly",
            width=5,
        )
        self.campo_id.pack(side="left", padx=5, pady=10)

        # Producto
        etiqueta_nombre = tk.Label(
            self.marco_registro,
            text="Producto:",
            font=("Times", 14),
            fg="#666a88",
            bg=COLOR_FONDO,
        )
        etiqueta_nombre.pack(side="left", padx=5, pady=10)

        self.campo_nombre = ttk.Entry(
            self.marco_registro,
            font=("Times", 14),
        )
        self.campo_nombre.pack(side="left", padx=5, pady=10)

        # Precio
        etiqueta_precio = tk.Label(
            self.marco_registro,
            text="Precio:",
            font=("Times", 14),
            fg="#666a88",
            bg=COLOR_FONDO,
        )
        etiqueta_precio.pack(side="left", padx=5, pady=10)

        self.campo_precio = ttk.Entry(
            self.marco_registro,
            font=("Times", 14),
        )
        self.campo_precio.pack(side="left", padx=5, pady=10)

        # Validación en tiempo real para precio (solo números y punto)
        self.campo_precio.configure(
            validate="key",
            validatecommand=(self.register(self._validar_precio_entry), "%P"),
        )

        self.btn_registro = tk.Button(
            self.marco_acciones,
            text="Registrar",
            font=("Times", 13),
            bg="#51aded",
            bd=0,
            fg="#fff",
            padx=15,
            command=self.registrar_producto,
        )
        self.btn_registro.pack(**self.obtener_conf_btn_pack())
        self.btn_registro.bind("<Return>", lambda event: self.registrar_producto())

        self.btn_eliminar = tk.Button(
            self.marco_acciones,
            text="Eliminar",
            font=("Times", 13),
            bg="#ed5153",
            bd=0,
            fg="#fff",
            padx=15,
            command=self.eliminar_producto,
        )
        self.btn_eliminar.pack(**self.obtener_conf_btn_pack())
        self.btn_eliminar.bind("<Return>", lambda event: self.eliminar_producto())
        self.btn_eliminar.pack_forget()

        self.btn_modificar = tk.Button(
            self.marco_acciones,
            text="Modificar",
            font=("Times", 13),
            bg="#536270",
            bd=0,
            fg="#fff",
            padx=15,
            command=self.modificar_producto,
        )
        self.btn_modificar.pack(**self.obtener_conf_btn_pack())
        self.btn_modificar.bind("<Return>", lambda event: self.modificar_producto())
        self.btn_modificar.pack_forget()

        self.btn_limpiar_campos = tk.Button(
            self.marco_acciones,
            text="Limpiar Campos",
            font=("Times", 13),
            bg="#e39531",
            bd=0,
            fg="#fff",
            padx=15,
            command=self.limpiar_campos,
        )
        self.btn_limpiar_campos.pack(**self.obtener_conf_btn_pack())
        self.btn_limpiar_campos.bind("<Return>", lambda event: self.limpiar_campos())

        # Tabla
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="#f8fafb", foreground="#111")
        style.configure("Treeview.Heading", background="#4b6e6b", foreground="#fff")
        style.map("Treeview", background=[("selected", "#cde7e2")])

        tree_scroll = ttk.Scrollbar(self.marco_productos, orient="vertical")
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.marco_productos,
            show="headings",
            yscrollcommand=tree_scroll.set,
        )
        self.tree["columns"] = ["Id", "Nombre", "Precio"]
        self.tree.column("#0", width=0)
        self.tree.column("Id", anchor="center", width=80, stretch=False)
        self.tree.column("Nombre", anchor="w", width=420)
        self.tree.column("Precio", anchor="e", width=120, stretch=False)

        self.tree.heading("#0", text="")
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")

        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_treeview)

        self.tree.tag_configure("oddrow", background="#fdf6e3")
        self.tree.tag_configure("evenrow", background="#eef7f2")

        self.actualizar_lista()

    def actualizar_lista(self) -> None:
        pass

    def registrar_producto(self) -> None:
        pass

    def eliminar_producto(self) -> None:
        pass

    def modificar_producto(self) -> None:
        pass

    def al_seleccionar_treeview(self, event: tk.Event) -> None:
        pass

    def limpiar_campos(self) -> None:
        """Limpia los campos de entrada del formulario y resetea acciones."""
        try:
            self.campo_id.config(state="normal")
            self.campo_id.delete(0, tk.END)
            self.campo_id.config(state="readonly")
            self.campo_nombre.delete(0, tk.END)
            self.campo_precio.delete(0, tk.END)
            self.btn_eliminar.pack_forget()
            self.btn_modificar.pack_forget()
            self.btn_registro.pack(**self.obtener_conf_btn_pack())
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar los campos: {e}")

    def _validar_precio_entry(self, nuevo_valor: str) -> bool:
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
