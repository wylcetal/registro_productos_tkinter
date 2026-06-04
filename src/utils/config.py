"""
Sistema de configuración persistente usando JSON
Implementa patrón Singleton para garantizar única instancia
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ThemeConfig:
    """Configuración del tema visual"""

    background_color: str = "#f7f8fa"
    component_color: str = "#2d2d2d"
    text_color: str = "#485159"
    accent_color: str = "#007acc"
    error_color: str = "#f44336"
    success_color: str = "#4caf50"
    warning_color: str = "#ff9800"
    title_font_family: str = "Roboto"
    font_family: str = "Times"
    font_size: int = 14
    title_font_size: int = 20


@dataclass
class WindowConfig:
    """Configuración de la ventana principal"""

    width: int = 880
    height: int = 540
    min_width: int = 600
    min_height: int = 400
    center_on_start: bool = True
    remember_size: bool = True
    remember_position: bool = True


@dataclass
class AppConfig:
    """Configuración general de la aplicación"""

    language: str = "es"
    auto_backup: bool = True
    backup_interval_days: int = 7
    show_statistics: bool = True
    confirm_delete: bool = True
    show_welcome_screen: bool = True
    max_recent_tests: int = 10


class Config:
    """
    Gestor de configuración de la aplicación (Singleton)
    Guarda y carga configuración desde archivo JSON
    """

    _instance: Optional["Config"] = None
    _config_file: Path = Path.cwd() / "config" / "app_config.json"

    def __new__(cls) -> "Config":
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Inicializa la configuración"""
        if self._initialized:
            return

        self._initialized = True

        # Configuraciones por defecto
        self.theme = ThemeConfig()
        self.window = WindowConfig()
        self.app = AppConfig()

        # Cargar configuración guardada
        self.load()

    def load(self) -> None:
        """Carga la configuración desde el archivo JSON"""
        if not self._config_file.exists():
            # Si no existe, crear con valores por defecto
            self.save()
            return

        try:
            with open(self._config_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Cargar cada sección
            if "theme" in data:
                self.theme = ThemeConfig(**data["theme"])

            if "window" in data:
                self.window = WindowConfig(**data["window"])

            if "app" in data:
                self.app = AppConfig(**data["app"])

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error al cargar configuración: {e}")
            # Usar valores por defecto en caso de error
            self.reset_to_defaults()

    def save(self) -> None:
        """Guarda la configuración actual en el archivo JSON"""
        # Crear directorio si no existe
        self._config_file.parent.mkdir(parents=True, exist_ok=True)

        # Preparar datos para guardar
        data = {
            "theme": asdict(self.theme),
            "window": asdict(self.window),
            "app": asdict(self.app),
        }

        # Guardar en archivo
        with open(self._config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def reset_to_defaults(self) -> None:
        """Restaura la configuración a valores por defecto"""
        self.theme = ThemeConfig()
        self.window = WindowConfig()
        self.app = AppConfig()
        self.save()

    def update_window(self, **kwargs) -> None:
        """Actualiza configuración de ventana"""
        for key, value in kwargs.items():
            if hasattr(self.window, key):
                setattr(self.window, key, value)
        self.save()

    @property
    def config_file_path(self) -> Path:
        """Retorna la ruta del archivo de configuración"""
        return self._config_file


# Instancia global de configuración
config = Config()
