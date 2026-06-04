import tkinter as tk


def centrar_ventana(
    ventana: tk.Tk, aplicacion_ancho: int, aplicacion_largo: int
) -> str:
    """Centra la ventana en la pantalla con el ancho y alto dados."""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (aplicacion_ancho / 2))
    y = int((pantalla_largo / 2) - (aplicacion_largo / 2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
