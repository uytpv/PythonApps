"""Main application window — controls which screen is displayed."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from models import ArbProject
from screen_open import OpenScreen
from screen_editor import EditorScreen

APP_TITLE = "ARB Translation Editor"
APP_WIDTH = 960
APP_HEIGHT = 640

# ── Colour palette ─────────────────────────────────────────────────────────
BG_DARK   = "#1E1E2E"
BG_MID    = "#2A2A3A"
FG_LIGHT  = "#D0D0E8"
ACCENT    = "#7C5CBF"
ACCENT_HO = "#9B7FE0"


class App(tk.Tk):
    """Root application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(800, 500)
        self.configure(bg=BG_DARK)

        self.project = ArbProject()
        self._current_frame: tk.Frame | None = None

        self._show_open_screen()

    # ── Screen switching ────────────────────────────────────────────────────

    def _show_open_screen(self) -> None:
        self._switch_to(OpenScreen(self, self.project, on_open=self._show_editor))

    def _show_editor(self) -> None:
        self._switch_to(EditorScreen(self, self.project, on_back=self._show_open_screen))

    def _switch_to(self, frame: tk.Frame) -> None:
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = frame
        frame.pack(fill="both", expand=True)
