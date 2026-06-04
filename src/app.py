"""
Gestor principal de la aplicación
Coordina ventanas y navegación entre vistas
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Optional

from src.controllers.app_controller import AppController
from src.ui.styles import COLORS, ModernStyles
from src.utils.config import config
from src.utils.validators import FormValidator


class Application(tk.Tk):
    """
    Aplicación principal
    Gestiona ventanas, navegación y ciclo de vida de la aplicación
    """

    def __init__(self):
        super().__init__()
        self._configure_window()
        self.styles = ModernStyles(self)
        self.controller = AppController(self)
        self.validator = FormValidator()

        self.container = ttk.Frame(self, style="Main.TFrame")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames: Dict[str, tk.Frame] = {}

    def _configure_window(self):
        self.title("Registro de Productos")
        window_config = config.window
        self.geometry(f"{window_config.width}x{window_config.height}")
        self.minsize(window_config.min_width, window_config.min_height)
        self.configure(bg=COLORS["bg"])
        if window_config.center_on_start:
            self._center_window()

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")

    def show_frame(self, frame_name: str):
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            self.current_frame = frame

    def register_frame(self, frame_name: str, frame: tk.Frame):
        self.frames[frame_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.mainloop()

    def on_closing(self):
        if config.window.remember_size:
            config.update_window(width=self.winfo_width(), height=self.winfo_height())
        if config.window.remember_position:
            config.update_window(x=self.winfo_x(), y=self.winfo_y())
        self.destroy()


class SimpleApp(Application):
    """
    Aplicación con interfaz de gestión de productos
    """

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._create_home_view()
        self._crear_controles()

    def _create_home_view(self):
        home_frame = ttk.Frame(self.container, style="Main.TFrame")
        self.register_frame("home", home_frame)

        # ── Header bar ────────────────────────────────────────────────────
        header = tk.Frame(home_frame, bg=COLORS["accent"], height=56)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        dots_frame = tk.Frame(header, bg=COLORS["accent"])
        dots_frame.pack(side="left", padx=18)
        for dot_color in ("#ff5f57", "#febc2e", "#28c840"):
            c = tk.Canvas(
                dots_frame, width=12, height=12,
                bg=COLORS["accent"], highlightthickness=0,
            )
            c.pack(side="left", padx=3)
            c.create_oval(1, 1, 11, 11, fill=dot_color, outline="")

        tk.Label(
            header,
            text="REGISTRO DE PRODUCTOS",
            bg=COLORS["accent"], fg="white",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left", padx=8)

        tk.Label(
            header,
            text="  ·  Sistema de Inventario",
            bg=COLORS["accent"], fg=COLORS["accent_light"],
            font=("Segoe UI", 10),
        ).pack(side="left")

        # ── Main content ──────────────────────────────────────────────────
        content = ttk.Frame(home_frame, style="Main.TFrame")
        content.pack(fill="both", expand=True, padx=24, pady=16)

        # ── Form card ─────────────────────────────────────────────────────
        form_outer = tk.Frame(content, bg=COLORS["surface"])
        form_outer.pack(fill="x", pady=(0, 10))

        tk.Frame(form_outer, bg=COLORS["accent"], width=4).pack(side="left", fill="y")

        form_inner = tk.Frame(form_outer, bg=COLORS["surface"])
        form_inner.pack(side="left", fill="both", expand=True, padx=18, pady=14)
        self.marco_registro = form_inner

        # ── Action buttons ────────────────────────────────────────────────
        self.marco_acciones = tk.Frame(content, bg=COLORS["bg"])
        self.marco_acciones.pack(fill="x", pady=(0, 14))

        # ── Products table ────────────────────────────────────────────────
        table_section = ttk.Frame(content, style="Main.TFrame")
        table_section.pack(fill="both", expand=True)

        ttk.Label(
            table_section,
            text="Listado de Productos",
            style="SectionTitle.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        self.marco_productos = ttk.Frame(table_section, style="Main.TFrame")
        self.marco_productos.pack(fill="both", expand=True)

        self.show_frame("home")

    def _crear_controles(self):
        # ── ID ────────────────────────────────────────────────────────────
        id_col = tk.Frame(self.marco_registro, bg=COLORS["surface"])
        id_col.pack(side="left", padx=(0, 20))
        tk.Label(
            id_col, text="ID",
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")
        self.campo_id = ttk.Entry(id_col, style="Modern.TEntry", state="readonly", width=6)
        self.campo_id.pack()

        # ── Nombre ────────────────────────────────────────────────────────
        nombre_col = tk.Frame(self.marco_registro, bg=COLORS["surface"])
        nombre_col.pack(side="left", padx=(0, 20))
        tk.Label(
            nombre_col, text="NOMBRE DEL PRODUCTO",
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")
        self.campo_nombre = ttk.Entry(nombre_col, style="Modern.TEntry", width=36)
        self.campo_nombre.pack()

        # ── Precio ────────────────────────────────────────────────────────
        precio_col = tk.Frame(self.marco_registro, bg=COLORS["surface"])
        precio_col.pack(side="left")
        tk.Label(
            precio_col, text="PRECIO ($)",
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")
        self.campo_precio = ttk.Entry(precio_col, style="Modern.TEntry", width=14)
        self.campo_precio.pack()
        self.campo_precio.configure(
            validate="key",
            validatecommand=(self.register(self.controller.validar_precio_entry), "%P"),
        )

        # ── Buttons (grid layout keeps positions stable on show/hide) ─────
        _btn = {
            "font": ("Segoe UI", 10, "bold"),
            "bd": 0, "relief": "flat",
            "cursor": "hand2",
            "highlightthickness": 0,
            "padx": 18, "pady": 9,
        }

        self.btn_registro = tk.Button(
            self.marco_acciones, text="＋  Registrar",
            bg=COLORS["accent"], fg="white",
            activebackground=COLORS["accent_hover"], activeforeground="white",
            command=self._registrar_producto, **_btn,
        )
        self.btn_registro.grid(row=0, column=0, padx=(0, 8))
        self._add_hover(self.btn_registro, COLORS["accent"], COLORS["accent_hover"])

        self.btn_modificar = tk.Button(
            self.marco_acciones, text="✎  Modificar",
            bg=COLORS["secondary"], fg="white",
            activebackground=COLORS["secondary_hover"], activeforeground="white",
            command=self._modificar_producto, **_btn,
        )
        self.btn_modificar.grid(row=0, column=1, padx=(0, 8))
        self._add_hover(self.btn_modificar, COLORS["secondary"], COLORS["secondary_hover"])

        self.btn_eliminar = tk.Button(
            self.marco_acciones, text="✕  Eliminar",
            bg=COLORS["error"], fg="white",
            activebackground=COLORS["error_hover"], activeforeground="white",
            command=self._eliminar_producto, **_btn,
        )
        self.btn_eliminar.grid(row=0, column=2, padx=(0, 8))
        self._add_hover(self.btn_eliminar, COLORS["error"], COLORS["error_hover"])

        self.btn_limpiar_campos = tk.Button(
            self.marco_acciones, text="↺  Limpiar",
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            activebackground=COLORS["card"], activeforeground=COLORS["text"],
            command=self.limpiar_campos, **_btn,
        )
        self.btn_limpiar_campos.grid(row=0, column=3)
        self._add_hover(self.btn_limpiar_campos, COLORS["surface"], COLORS["card"])

        # Initially hide edit/delete buttons
        self.btn_modificar.grid_remove()
        self.btn_eliminar.grid_remove()

        # ── Treeview ──────────────────────────────────────────────────────
        tree_scroll = ttk.Scrollbar(
            self.marco_productos, orient="vertical",
            style="Modern.Vertical.TScrollbar",
        )
        tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.marco_productos,
            show="headings",
            style="Modern.Treeview",
            yscrollcommand=tree_scroll.set,
        )
        tree_scroll.configure(command=self.tree.yview)

        self.tree["columns"] = ["Id", "Nombre", "Precio"]
        self.tree.column("Id", anchor="center", width=70, stretch=False)
        self.tree.column("Nombre", anchor="w", width=460)
        self.tree.column("Precio", anchor="e", width=140, stretch=False)
        self.tree.heading("Id", text="ID")
        self.tree.heading("Nombre", text="Nombre del Producto")
        self.tree.heading("Precio", text="Precio")

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._al_seleccionar_treeview)

        self.tree.tag_configure("evenrow", background=COLORS["row_even"])
        self.tree.tag_configure("oddrow", background=COLORS["row_odd"])

        self._actualizar_lista()

    @staticmethod
    def _add_hover(btn: tk.Button, normal_bg: str, hover_bg: str) -> None:
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=normal_bg))

    def obtener_seleccion_id(self, seleccion) -> Optional[int]:
        if not seleccion:
            return None
        try:
            return int(self.tree.item(seleccion[0])["values"][0])
        except Exception:
            return None

    def _registrar_producto(self):
        self.controller.registrar_producto(
            self.campo_nombre.get(), self.campo_precio.get()
        )
        self._actualizar_lista()
        self.limpiar_campos()

    def _actualizar_lista(self):
        for registro in self.tree.get_children():
            self.tree.delete(registro)
        productos = self.controller.actualizar_lista()
        if productos:
            for ref, producto in enumerate(productos):
                tag = ("evenrow",) if ref % 2 == 0 else ("oddrow",)
                self.tree.insert(
                    parent="", index=ref, iid=ref,
                    text="", tags=tag,
                    values=(producto.id, producto.nombre, f"{producto.precio:.2f}"),
                )

    def _eliminar_producto(self):
        seleccion = self.tree.selection()
        self.controller.eliminar_producto(self.obtener_seleccion_id(seleccion))
        self._actualizar_lista()
        self.limpiar_campos()

    def _modificar_producto(self):
        seleccion = self.tree.selection()
        self.controller.modificar_producto(
            self.obtener_seleccion_id(seleccion),
            self.campo_nombre.get(),
            self.campo_precio.get(),
        )
        self._actualizar_lista()
        self.limpiar_campos()

    def _al_seleccionar_treeview(self, event):
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
                self.btn_modificar.grid()
                self.btn_eliminar.grid()
                self.btn_registro.grid_remove()

    def limpiar_campos(self):
        try:
            self.campo_id.config(state="normal")
            self.campo_id.delete(0, tk.END)
            self.campo_id.config(state="readonly")
            self.campo_nombre.delete(0, tk.END)
            self.campo_precio.delete(0, tk.END)
            self.btn_modificar.grid_remove()
            self.btn_eliminar.grid_remove()
            self.btn_registro.grid()
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar los campos: {e}")


def create_app() -> Application:
    return SimpleApp()
