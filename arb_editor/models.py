"""Data models for ARB file management."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ArbFile:
    """Represents a single .arb localization file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.locale: str = path.stem  # e.g. "app_en" or "intl_vi"
        self.data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load JSON data from the .arb file."""
        text = self.path.read_text(encoding="utf-8")
        self.data = json.loads(text)

    def get_keys(self) -> list[str]:
        """Return translation keys (exclude metadata keys starting with @@ or @)."""
        return [k for k in self.data if not k.startswith("@")]

    def get_value(self, key: str) -> str:
        """Get translation value for a key."""
        return str(self.data.get(key, ""))

    def set_value(self, key: str, value: str) -> None:
        """Set/update a translation value."""
        self.data[key] = value

    def rename_key(self, old_key: str, new_key: str) -> None:
        """Rename a key, preserving order and associated metadata."""
        if old_key not in self.data or old_key == new_key:
            return
        # Rebuild ordered dict with renamed key
        new_data: dict[str, Any] = {}
        for k, v in self.data.items():
            if k == old_key:
                new_data[new_key] = v
            elif k == f"@{old_key}":
                new_data[f"@{new_key}"] = v
            else:
                new_data[k] = v
        self.data = new_data

    def remove_key(self, key: str) -> None:
        """Remove a key and its metadata."""
        self.data.pop(key, None)
        self.data.pop(f"@{key}", None)

    def save(self) -> None:
        """Write data back to the .arb file, sorted alphabetically."""
        # Sort by base key name, placing @metadata exactly after its base key
        sorted_keys = sorted(
            self.data.keys(),
            key=lambda k: (k.lstrip('@').lower(), 1 if k.startswith('@') else 0)
        )
        self.data = {k: self.data[k] for k in sorted_keys}
        
        text = json.dumps(self.data, ensure_ascii=False, indent=2)
        self.path.write_text(text, encoding="utf-8")

    @property
    def display_name(self) -> str:
        """Human-readable name for display."""
        return self.path.name


class ArbProject:
    """Manages a collection of .arb files as a project."""

    def __init__(self) -> None:
        self.files: list[ArbFile] = []

    def add_file(self, path: Path) -> ArbFile | None:
        """Add an ARB file; returns None if already added."""
        # Avoid duplicates
        for f in self.files:
            if f.path == path:
                return None
        arb = ArbFile(path)
        self.files.append(arb)
        return arb

    def remove_file(self, arb: ArbFile) -> None:
        """Remove a file from the project."""
        self.files = [f for f in self.files if f is not arb]

    def all_keys(self) -> list[str]:
        """Return the union of all keys across all files, preserving insertion order."""
        seen: dict[str, None] = {}
        for arb in self.files:
            for k in arb.get_keys():
                seen[k] = None
        return list(seen.keys())

    def rename_key_everywhere(self, old_key: str, new_key: str) -> None:
        """Rename a key in all loaded files."""
        for arb in self.files:
            arb.rename_key(old_key, new_key)

    def add_key_everywhere(self, key: str, default_value: str = "") -> bool:
        """Add a key to all loaded files if it doesn't already exist."""
        if key in self.all_keys():
            return False
        for arb in self.files:
            arb.set_value(key, default_value)
        return True

    def delete_key_everywhere(self, key: str) -> None:
        """Delete a key from all loaded files."""
        for arb in self.files:
            arb.remove_key(key)

    def save_all(self) -> None:
        """Save every file in the project."""
        for arb in self.files:
            arb.save()
