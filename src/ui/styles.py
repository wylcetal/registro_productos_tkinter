"""
Sistema de estilos modernos usando ttk
Centraliza todos los estilos visuales de la aplicación
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict

from src.utils.config import config

COLORS: Dict[str, str] = {
    "bg": "#0f111a",
    "surface": "#1a1d2e",
    "card": "#252840",
    "accent": "#6366f1",
    "accent_hover": "#4f46e5",
    "accent_light": "#c7d2fe",
    "text": "#e8ecf1",
    "text_secondary": "#9ca3af",
    "error": "#f87171",
    "error_hover": "#ef4444",
    "success": "#4ade80",
    "success_hover": "#22c55e",
    "warning": "#fbbf24",
    "warning_hover": "#f59e0b",
    "secondary": "#4b5563",
    "secondary_hover": "#374151",
    "border": "#2d3252",
    "row_even": "#1a1d2e",
    "row_odd": "#20243a",
    "row_selected": "#4f46e5",
}


class ModernStyles:
    """Gestor de estilos modernos para la aplicación"""

    COLORS = COLORS

    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style()
        self.theme_config = config.theme

        self._configure_theme()
        self._configure_buttons()
        self._configure_entries()
        self._configure_labels()
        self._configure_frames()
        self._configure_treeview()
        self._configure_scrollbar()

    def _configure_theme(self):
        available_themes = self.style.theme_names()
        if "clam" in available_themes:
            self.style.theme_use("clam")

        self.style.configure(
            ".",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["surface"],
            troughcolor=COLORS["bg"],
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 11),
        )

    def _configure_buttons(self):
        for name, bg, hover, fg in [
            ("Accent", COLORS["accent"], COLORS["accent_hover"], "white"),
            ("Danger", COLORS["error"], COLORS["error_hover"], "white"),
            ("Secondary", COLORS["secondary"], COLORS["secondary_hover"], "white"),
            ("Warning", COLORS["warning"], COLORS["warning_hover"], "#111111"),
        ]:
            self.style.configure(
                f"{name}.TButton",
                background=bg,
                foreground=fg,
                borderwidth=0,
                focuscolor="none",
                padding=(20, 10),
                font=("Segoe UI", 11, "bold"),
                relief="flat",
            )
            self.style.map(
                f"{name}.TButton",
                background=[("active", hover), ("pressed", hover)],
                foreground=[("active", fg)],
            )

    def _configure_entries(self):
        self.style.configure(
            "Modern.TEntry",
            foreground=COLORS["text"],
            fieldbackground=COLORS["card"],
            insertcolor=COLORS["text"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 11),
            padding=(8, 6),
        )
        self.style.map(
            "Modern.TEntry",
            fieldbackground=[("focus", COLORS["card"]), ("readonly", COLORS["surface"])],
        )

    def _configure_labels(self):
        self.style.configure(
            "Title.TLabel",
            background=COLORS["accent"],
            foreground="white",
            font=("Segoe UI", 14, "bold"),
            padding=(0, 16),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["text_secondary"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "SectionTitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=("Segoe UI", 11, "bold"),
            padding=(0, 4),
        )

    def _configure_frames(self):
        self.style.configure("Main.TFrame", background=COLORS["bg"])
        self.style.configure("Surface.TFrame", background=COLORS["surface"])
        self.style.configure("Card.TFrame", background=COLORS["card"])
        # Legacy
        self.style.configure("Card1.TFrame", background=COLORS["accent"])
        self.style.configure("Card2.TFrame", background=COLORS["surface"])

    def _configure_treeview(self):
        self.style.configure(
            "Modern.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["surface"],
            borderwidth=0,
            font=("Segoe UI", 11),
            rowheight=32,
        )
        self.style.configure(
            "Modern.Treeview.Heading",
            background=COLORS["card"],
            foreground=COLORS["text_secondary"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 8),
        )
        self.style.map(
            "Modern.Treeview",
            background=[("selected", COLORS["row_selected"])],
            foreground=[("selected", "white")],
        )
        self.style.map(
            "Modern.Treeview.Heading",
            background=[("active", COLORS["border"])],
        )

    def _configure_scrollbar(self):
        self.style.configure(
            "Modern.Vertical.TScrollbar",
            background=COLORS["card"],
            troughcolor=COLORS["surface"],
            borderwidth=0,
            arrowcolor=COLORS["text_secondary"],
            relief="flat",
            width=8,
        )
        self.style.map(
            "Modern.Vertical.TScrollbar",
            background=[("active", COLORS["accent"])],
        )

    @staticmethod
    def _darken_color(hex_color: str, factor: float = 0.8) -> str:
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    @staticmethod
    def _lighten_color(hex_color: str, factor: float = 1.2) -> str:
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        lightened = tuple(min(int(c * factor), 255) for c in rgb)
        return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"

    def get_colors(self) -> Dict[str, str]:
        """Return colors merged with theme config (if available)."""
        base = self.COLORS.copy()
        try:
            theme = self.theme_config
            if theme:
                base.update(
                    {
                        "accent": getattr(theme, "accent_color", base["accent"]),
                        "error": getattr(theme, "error_color", base["error"]),
                        "success": getattr(theme, "success_color", base["success"]),
                        "warning": getattr(theme, "warning_color", base["warning"]),
                    }
                )
        except Exception:
            pass
        return base
