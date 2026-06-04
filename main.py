"""Punto de entrada de la aplicación de registro de productos (Tkinter)."""

import logging
import sys
from pathlib import Path

# from form.registro_form import FormularioRegistro
from src.app import create_app

# Agregar el directorio raíz al path para imports
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    """
    Función principal de la aplicación
    """
    try:
        # Crear aplicacion
        # app = FormularioRegistro()
        app = create_app()

        # Ejecutar aplicacion
        # app.mainloop()
        app.run()

    except KeyboardInterrupt:
        print("\nAplicacion interrumpida por el usuario.")
        sys.exit(0)

    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 70)
    print("Sistema de Registro de Productos - Versión 1.0")
    print("=" * 70)
    print()

    main()
