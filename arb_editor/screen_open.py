"""Screen 1 — Open ARB files."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Callable

from models import ArbProject

# ── Colours ─────────────────────────────────────────────────────────────────
BG_DARK   = "#1E1E2E"
BG_MID    = "#2A2A3A"
BG_ITEM   = "#31314A"
FG_LIGHT  = "#D0D0E8"
FG_DIM    = "#8888AA"
ACCENT    = "#7C5CBF"
ACCENT_HO = "#9B7FE0"
RED_SOFT  = "#C0424A"


class OpenScreen(tk.Frame):
    """File-picker screen for selecting .arb files."""

    def __init__(
        self,
        master: tk.Widget,
        project: ArbProject,
        on_open: Callable[[], None],
    ) -> None:
        super().__init__(master, bg=BG_DARK)
        self.project = project
        self.on_open = on_open
        self._build_ui()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Header
        header = tk.Frame(self, bg=BG_DARK, pady=24)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🌐  ARB Translation Editor",
            font=("Segoe UI", 22, "bold"),
            fg=FG_LIGHT,
            bg=BG_DARK,
        ).pack()

        tk.Label(
            header,
            text="Add one or more .arb locale files to begin editing",
            font=("Segoe UI", 11),
            fg=FG_DIM,
            bg=BG_DARK,
        ).pack(pady=(4, 0))

        # File list card
        card = tk.Frame(self, bg=BG_MID, padx=20, pady=16, bd=0)
        card.pack(fill="both", expand=True, padx=60, pady=(0, 10))

        tk.Label(
            card,
            text="Selected files",
            font=("Segoe UI", 10, "bold"),
            fg=FG_DIM,
            bg=BG_MID,
        ).pack(anchor="w", pady=(0, 8))

        # Listbox container
        list_frame = tk.Frame(card, bg=BG_DARK, bd=1, relief="flat")
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg=BG_MID, troughcolor=BG_DARK)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=BG_DARK,
            fg=FG_LIGHT,
            selectbackground=ACCENT,
            selectforeground=FG_LIGHT,
            activestyle="none",
            font=("Consolas", 11),
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.listbox.pack(fill="both", expand=True, padx=2, pady=2)
        scrollbar.config(command=self.listbox.yview)

        # Reload from project state (if navigating back)
        for arb in self.project.files:
            self.listbox.insert("end", arb.display_name)

        # Buttons row below list
        btn_row = tk.Frame(card, bg=BG_MID, pady=10)
        btn_row.pack(fill="x")

        self._btn(btn_row, "＋  Add File", self._add_file, ACCENT, ACCENT_HO).pack(side="left", padx=(0, 8))
        self._btn(btn_row, "✕  Remove Selected", self._remove_selected, RED_SOFT, "#D9515A").pack(side="left")

        # Open editor button
        bottom = tk.Frame(self, bg=BG_DARK, pady=20)
        bottom.pack(fill="x")

        open_btn = tk.Button(
            bottom,
            text="Open Editor →",
            command=self._open_editor,
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HO,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=28,
            pady=10,
            bd=0,
        )
        open_btn.pack()

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _btn(
        parent: tk.Widget,
        text: str,
        cmd: Callable[[], None],
        bg: str,
        hover: str,
    ) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            font=("Segoe UI", 10),
            bg=bg,
            fg="white",
            activebackground=hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=6,
            bd=0,
        )
        return btn

    # ── Actions ──────────────────────────────────────────────────────────────

    def _add_file(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select .arb file(s)",
            filetypes=[("ARB files", "*.arb"), ("All files", "*.*")],
        )
        for p in paths:
            arb = self.project.add_file(Path(p))
            if arb:
                self.listbox.insert("end", arb.display_name)

    def _remove_selected(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        arb = self.project.files[idx]
        self.project.remove_file(arb)
        self.listbox.delete(idx)

    def _open_editor(self) -> None:
        if not self.project.files:
            messagebox.showwarning("No files", "Please add at least one .arb file.")
            return
        self.on_open()
