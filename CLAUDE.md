# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the application
python main.py

# Initialize the database (first-time setup)
python build_db.py

# Run all tests
python -m pytest tests/

# Run a single test
python -m pytest tests/test_servicio_producto.py::ServicioProductoTest::test_registrar_producto_valido

# Install dependencies (uses uv)
uv sync
```

## Architecture

This is a Tkinter desktop app for product registration, built with MVC separation. Python 3.13, SQLAlchemy 2.0+, SQLite.

**Entry flow:** `main.py` → `create_app()` factory in `src/app.py` → `SimpleApp` (extends `Application`) → `app.run()` → Tkinter `mainloop()`.

**Layers:**

- **`src/models/entities.py`** — SQLAlchemy ORM. Single `Producto` entity (`id`, `nombre`, `precio`).
- **`services/servicio_producto.py`** — CRUD service. Accepts an optional `Engine` for injection (used in tests). All DB operations go through here.
- **`src/controllers/app_controller.py`** — Bridges UI events to the service layer; calls `FormValidator` before writes.
- **`src/app.py`** — `Application` base class manages the Tkinter window and frame switching. `SimpleApp` subclass builds the full UI (form + Treeview table + buttons).
- **`src/ui/styles.py`** — Centralized ttk dark-theme styling applied at startup.
- **`src/ui/components.py`** — `ConfirmDialog` wrapper for all modal dialogs.
- **`src/utils/config.py`** — Singleton `Config` that reads/writes `config/app_config.json`. Sections: `ThemeConfig`, `WindowConfig`, `AppConfig`.
- **`src/utils/validators.py`** — `FormValidator` static methods; return `ValidationResult(is_valid, error_message)`.

**Database path:** `config.py` (root) calls `utils/generico.py:crear_db()` which creates `db/` and returns the path. `build_db.py` runs `Base.metadata.create_all()` to set up the schema.

**Legacy code:** `form/`, `dominio/`, `aplicacion/` and `utils/util_ventana.py` are leftovers from an earlier architecture. The active code lives in `src/` and `services/`.

**Tests** use `unittest` with an in-memory SQLite engine injected into `ServicioProducto`.
