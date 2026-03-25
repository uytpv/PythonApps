"""Screen 2 — ARB key/value editor (similar to BabelEdit layout)."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Callable
import threading

from deep_translator import GoogleTranslator

from models import ArbProject

# ── Colours ─────────────────────────────────────────────────────────────────
BG_DARK      = "#1E1E2E"
BG_MID       = "#2A2A3A"
BG_SIDEBAR   = "#252535"
BG_ITEM      = "#2E2E42"
BG_SEL       = "#7C5CBF"
BG_SEL_HO    = "#9B7FE0"
BG_ENTRY     = "#1A1A2E"
FG_LIGHT     = "#D0D0E8"
FG_DIM       = "#8888AA"
FG_SEL       = "#FFFFFF"
ACCENT       = "#7C5CBF"
ACCENT_HO    = "#9B7FE0"
BORDER       = "#3A3A55"
GREEN_SOFT   = "#27AE60"
RED_SOFT     = "#C0424A"

FONT_UI   = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_KEY  = ("Consolas", 11)
FONT_VAL  = ("Segoe UI", 11)


class EditorScreen(tk.Frame):
    """
    Full editor screen:
    ┌──────────────────────────────────────────────────────┐
    │ Toolbar: ← Back | filename labels | Save             │
    ├───────────────────┬──────────────────────────────────┤
    │  Key list (left)  │  Translation values (right)      │
    └───────────────────┴──────────────────────────────────┘
    """

    def __init__(
        self,
        master: tk.Widget,
        project: ArbProject,
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(master, bg=BG_DARK)
        self.project = project
        self.on_back = on_back
        self._keys: list[str] = []
        self._selected_idx: int = -1
        # Tracks which key is being renamed to prevent recursive updates
        self._renaming: bool = False
        self._build_ui()
        self._load_keys()

    # ────────────────────────────────────────────────────────────────────────
    # UI construction
    # ────────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._build_toolbar()
        self._build_body()

    def _build_toolbar(self) -> None:
        bar = tk.Frame(self, bg=BG_MID, pady=8, padx=12)
        bar.pack(fill="x", side="top")

        # Back button
        back_btn = tk.Button(
            bar,
            text="← Back",
            command=self.on_back,
            font=FONT_UI,
            bg=BG_DARK,
            fg=FG_DIM,
            activebackground=BG_DARK,
            activeforeground=FG_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            bd=0,
        )
        back_btn.pack(side="left")

        # File names
        names = "  |  ".join(f.display_name for f in self.project.files)
        tk.Label(
            bar,
            text=names,
            font=FONT_UI,
            fg=FG_DIM,
            bg=BG_MID,
        ).pack(side="left", padx=20)

        # Save button (right-aligned)
        save_btn = tk.Button(
            bar,
            text="💾  Save All",
            command=self._save_all,
            font=FONT_BOLD,
            bg=GREEN_SOFT,
            fg="white",
            activebackground="#2ECC71",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=6,
            bd=0,
        )
        save_btn.pack(side="right")

    def _build_body(self) -> None:
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # ── Left: key list ────────────────────────────────────────────────
        left = tk.Frame(body, bg=BG_SIDEBAR, width=260)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        lbl_row = tk.Frame(left, bg=BG_SIDEBAR, pady=8, padx=10)
        lbl_row.pack(fill="x")
        tk.Label(lbl_row, text="Translation IDs", font=FONT_BOLD, fg=FG_DIM, bg=BG_SIDEBAR).pack(side="left")

        # Search box
        search_frame = tk.Frame(left, bg=BG_SIDEBAR, padx=8, pady=4)
        search_frame.pack(fill="x")

        # Delete Key Button
        del_btn = tk.Button(
            search_frame,
            text="−",
            font=FONT_BOLD,
            bg=RED_SOFT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._on_delete_key,
            width=2,
            bd=0,
        )
        del_btn.pack(side="right", padx=(4, 0))

        # Add Key Button
        add_btn = tk.Button(
            search_frame,
            text="+",
            font=FONT_BOLD,
            bg=ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._on_add_key,
            width=2,
            bd=0,
        )
        add_btn.pack(side="right", padx=(4, 0))

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter_keys())
        search_entry = tk.Entry(
            search_frame, textvariable=self._search_var,
            font=FONT_UI, bg=BG_ENTRY, fg=FG_LIGHT, insertbackground=FG_LIGHT,
            relief="flat", bd=4, highlightthickness=1,
            highlightcolor=ACCENT, highlightbackground=BORDER,
        )
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.insert(0, "")
        # Placeholder
        search_entry.insert(0, "Search keys…")
        search_entry.config(fg=FG_DIM)
        search_entry.bind("<FocusIn>", lambda e: self._on_search_focus_in(search_entry))
        search_entry.bind("<FocusOut>", lambda e: self._on_search_focus_out(search_entry))

        # Key listbox with scrollbar
        list_frame = tk.Frame(left, bg=BG_SIDEBAR)
        list_frame.pack(fill="both", expand=True, padx=0, pady=4)

        sb = tk.Scrollbar(list_frame, bg=BG_MID, troughcolor=BG_DARK)
        sb.pack(side="right", fill="y")

        self.key_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=sb.set,
            bg=BG_SIDEBAR,
            fg=FG_LIGHT,
            selectbackground=ACCENT,
            selectforeground=FG_SEL,
            activestyle="none",
            font=FONT_KEY,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.key_listbox.pack(fill="both", expand=True)
        sb.config(command=self.key_listbox.yview)
        self.key_listbox.bind("<<ListboxSelect>>", self._on_key_select)

        # ── Right: detail panel ───────────────────────────────────────────
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        # Key edit area
        key_panel = tk.Frame(right, bg=BG_MID, padx=20, pady=14)
        key_panel.pack(fill="x")

        tk.Label(key_panel, text="Key", font=FONT_BOLD, fg=FG_DIM, bg=BG_MID).pack(anchor="w")

        self._key_var = tk.StringVar()
        self._key_entry = tk.Entry(
            key_panel,
            textvariable=self._key_var,
            font=("Consolas", 14, "bold"),
            bg=BG_ENTRY,
            fg=FG_LIGHT,
            insertbackground=FG_LIGHT,
            relief="flat",
            bd=6,
            highlightthickness=1,
            highlightcolor=ACCENT,
            highlightbackground=BORDER,
        )
        self._key_entry.pack(fill="x", pady=(6, 0))
        self._key_var.trace_add("write", self._on_key_changed)

        # Values scroll area
        values_outer = tk.Frame(right, bg=BG_DARK)
        values_outer.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tk.Label(values_outer, text="Translations", font=FONT_BOLD, fg=FG_DIM, bg=BG_DARK, pady=8).pack(anchor="w")

        # Canvas + inner frame for scrollable locale rows
        canvas = tk.Canvas(values_outer, bg=BG_DARK, highlightthickness=0)
        v_scroll = tk.Scrollbar(values_outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._values_frame = tk.Frame(canvas, bg=BG_DARK)
        self._canvas_window = canvas.create_window((0, 0), window=self._values_frame, anchor="nw")

        self._values_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self._canvas_window, width=e.width),
        )
        # Mouse-wheel scrolling (only if mouse is over values_outer)
        def _on_mousewheel(event):
            try:
                w = canvas.winfo_containing(event.x_root, event.y_root)
                w_name = str(w)
                outer_name = str(values_outer)
                if w_name == outer_name or w_name.startswith(outer_name + "."):
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")
            except Exception:
                pass

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Store reference to canvas for mouse-wheel unbind on destroy
        self._canvas = canvas

        # Value widgets — one Entry per locale file
        self._value_vars: list[tk.StringVar] = []
        self._value_entries: list[tk.Entry] = []
        for i, arb in enumerate(self.project.files):
            row = tk.Frame(self._values_frame, bg=BG_DARK, pady=6)
            row.pack(fill="x")

            locale_lbl = tk.Label(
                row,
                text=arb.display_name,
                font=FONT_BOLD,
                fg=ACCENT_HO,
                bg=BG_DARK,
                width=18,
                anchor="w",
            )
            locale_lbl.pack(side="left", padx=(0, 10))

            var = tk.StringVar()
            entry = tk.Entry(
                row,
                textvariable=var,
                font=FONT_VAL,
                bg=BG_ENTRY,
                fg=FG_LIGHT,
                insertbackground=FG_LIGHT,
                relief="flat",
                bd=6,
                highlightthickness=1,
                highlightcolor=ACCENT,
                highlightbackground=BORDER,
            )
            entry.pack(side="left", fill="x", expand=True)

            idx = i  # capture for closure
            
            btn_auto = tk.Button(
                row,
                text="Auto",
                font=("Consolas", 10, "bold"),
                bg=ACCENT,
                fg=BG_DARK,
                activebackground=ACCENT_HO,
                activeforeground=BG_DARK,
                relief="flat",
                cursor="hand2",
                command=lambda i=idx: self._auto_translate(i)
            )
            btn_auto.pack(side="left", padx=(10, 0))

            var.trace_add("write", lambda *_, i=idx: self._on_value_changed(i))

            self._value_vars.append(var)
            self._value_entries.append(entry)

        # Initially clear
        self._set_detail_state(enabled=False)

    # ────────────────────────────────────────────────────────────────────────
    # Data loading
    # ────────────────────────────────────────────────────────────────────────

    def _load_keys(self) -> None:
        self._keys = self.project.all_keys()
        self._refresh_listbox(self._keys)

    def _refresh_listbox(self, keys: list[str]) -> None:
        self.key_listbox.delete(0, "end")
        for k in keys:
            self.key_listbox.insert("end", k)

    # ────────────────────────────────────────────────────────────────────────
    # Selection & display
    # ────────────────────────────────────────────────────────────────────────

    def _on_key_select(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        sel = self.key_listbox.curselection()
        if not sel:
            return
        self._selected_idx = sel[0]
        displayed_key = self.key_listbox.get(self._selected_idx)
        self._show_key(displayed_key)

    def _show_key(self, key: str) -> None:
        """Populate right panel with data for selected key."""
        self._set_detail_state(enabled=True)

        # Update key entry without triggering rename logic
        self._renaming = True
        self._key_var.set(key)
        self._renaming = False

        # Update value entries
        for i, arb in enumerate(self.project.files):
            self._value_vars[i].set(arb.get_value(key))

    def _set_detail_state(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self._key_entry.config(state=state)
        for entry in self._value_entries:
            entry.config(state=state)

    # ────────────────────────────────────────────────────────────────────────
    # Editing callbacks
    # ────────────────────────────────────────────────────────────────────────

    def _on_key_changed(self, *_: object) -> None:
        """Rename the key in all files when user edits the key entry."""
        if self._renaming or self._selected_idx < 0:
            return
        new_key = self._key_var.get().strip()
        if not new_key:
            return
        old_key = self.key_listbox.get(self._selected_idx)
        if new_key == old_key:
            return
        # Rename in all files
        self.project.rename_key_everywhere(old_key, new_key)
        # Update master key list
        if old_key in self._keys:
            idx = self._keys.index(old_key)
            self._keys[idx] = new_key
        # Update listbox
        self.key_listbox.delete(self._selected_idx)
        self.key_listbox.insert(self._selected_idx, new_key)
        self.key_listbox.selection_set(self._selected_idx)

    def _on_value_changed(self, file_idx: int) -> None:
        """Save updated value to the model immediately."""
        if self._selected_idx < 0:
            return
        key = self.key_listbox.get(self._selected_idx)
        value = self._value_vars[file_idx].get()
        self.project.files[file_idx].set_value(key, value)

    def _on_delete_key(self) -> None:
        if self._selected_idx < 0:
            return
        key = self._keys[self._selected_idx]
        if messagebox.askyesno("Delete key", f"Delete '{key}' from all files?"):
            self.project.delete_key_everywhere(key)
            self._keys.remove(key)
            self._filter_keys()
            
            if self._keys:
                new_idx = min(self._selected_idx, len(self._keys) - 1)
                self.key_listbox.selection_set(new_idx)
                self.key_listbox.event_generate("<<ListboxSelect>>")
            else:
                self._selected_idx = -1
                self._set_detail_state(enabled=False)

    def _on_add_key(self) -> None:
        from tkinter import simpledialog
        new_key = simpledialog.askstring("Add Key", "Enter new translation key:", parent=self)
        if not new_key:
            return
        new_key = new_key.strip()
        if not new_key:
            return
            
        if self.project.add_key_everywhere(new_key):
            self._keys = self.project.all_keys()
            self._filter_keys()
            # Select the new key
            try:
                items = self.key_listbox.get(0, "end")
                if new_key in items:
                    idx = items.index(new_key)
                    self.key_listbox.selection_clear(0, "end")
                    self.key_listbox.selection_set(idx)
                    self.key_listbox.see(idx)
                    self._selected_idx = idx
                    self._show_key(new_key)
            except ValueError:
                pass
        else:
            messagebox.showwarning("Duplicate", f"Key '{new_key}' already exists.")

    def _auto_translate(self, target_idx: int) -> None:
        """
        Translates from the first non-empty locale into the target locale.
        """
        # 1. Find the first non-empty value to translate from
        source_text = ""
        for i, var in enumerate(self._value_vars):
            if i != target_idx and var.get().strip():
                source_text = var.get().strip()
                break
                
        if not source_text:
            messagebox.showinfo("Auto Translate", "No source text available to translate.")
            return
            
        # 2. Extract locale code from ARB file stem (e.g., 'app_fr' -> 'fr', 'es' -> 'es')
        target_arb = self.project.files[target_idx]
        target_locale = target_arb.locale.split('_')[-1].lower()
        
        # 3. Perform translation in a background thread
        def _do_translate() -> None:
            try:
                translator = GoogleTranslator(source='auto', target=target_locale)
                translated = translator.translate(source_text)
                
                # Update UI in main thread
                if translated:
                    self.after(0, lambda: self._value_vars[target_idx].set(translated))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Translation Error", f"Failed to translate:\n{e}"))
                
        t = threading.Thread(target=_do_translate, daemon=True)
        t.start()

    # ────────────────────────────────────────────────────────────────────────
    # Search
    # ────────────────────────────────────────────────────────────────────────

    _PLACEHOLDER = "Search keys…"

    def _on_search_focus_in(self, entry: tk.Entry) -> None:
        if entry.get() == self._PLACEHOLDER:
            entry.delete(0, "end")
            entry.config(fg=FG_LIGHT)

    def _on_search_focus_out(self, entry: tk.Entry) -> None:
        if not entry.get():
            entry.insert(0, self._PLACEHOLDER)
            entry.config(fg=FG_DIM)

    def _filter_keys(self) -> None:
        query = self._search_var.get().lower()
        if query == self._PLACEHOLDER.lower():
            query = ""
        filtered = [k for k in self._keys if query in k.lower()] if query else self._keys
        self._refresh_listbox(filtered)
        self._selected_idx = -1
        self._set_detail_state(enabled=False)
        self._key_var.set("")
        for var in self._value_vars:
            var.set("")

    # ────────────────────────────────────────────────────────────────────────
    # Save
    # ────────────────────────────────────────────────────────────────────────

    def _save_all(self) -> None:
        try:
            # Capture selected key to restore it
            selected_key = None
            if self._selected_idx >= 0:
                selected_key = self.key_listbox.get(self._selected_idx)
                
            self.project.save_all()
            
            # After save, reload the keys (which may have been sorted) and refresh the list
            self._keys = self.project.all_keys()
            self._filter_keys()
            
            # Restore selection if applicable
            if selected_key:
                items = self.key_listbox.get(0, "end")
                if selected_key in items:
                    idx = items.index(selected_key)
                    self.key_listbox.selection_clear(0, "end")
                    self.key_listbox.selection_set(idx)
                    self.key_listbox.see(idx)
                    self._selected_idx = idx
                    self._show_key(selected_key)
                    
            messagebox.showinfo("Saved", "All files have been saved successfully.")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))
