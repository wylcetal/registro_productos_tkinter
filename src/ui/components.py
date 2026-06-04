"""
Componentes UI reutilizables con ttk
Widgets personalizados para la aplicación
"""

from tkinter import messagebox


class ConfirmDialog:
    """Diálogo de confirmación personalizado"""

    @staticmethod
    def ask(title: str, message: str) -> bool:
        """
        Muestra un diálogo de confirmación

        Args:
            title: Título del diálogo
            message: Mensaje a mostrar

        Returns:
            True si el usuario confirma, False en caso contrario
        """
        return messagebox.askyesno(title, message)

    @staticmethod
    def show_error(title: str, message: str):
        """Muestra un diálogo de error"""
        messagebox.showerror(title, message)

    @staticmethod
    def show_success(title: str, message: str):
        """Muestra un diálogo de éxito"""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title: str, message: str):
        """Muestra un diálogo de advertencia"""
        messagebox.showwarning(title, message)

    @staticmethod
    def show_info(title: str, message: str):
        """Muestra un diálogo de información"""
        messagebox.showinfo(title, message)
