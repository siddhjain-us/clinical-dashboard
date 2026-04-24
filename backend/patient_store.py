from __future__ import annotations

import json
import threading
from pathlib import Path


class PatientStore:
    """Thread-safe patient list with JSON file persistence (demo / hackathon scope)."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = threading.Lock()
        self._data: list[dict] = []
        self._load()

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            with open(self._path, encoding="utf-8") as f:
                self._data = json.load(f)
        except (json.JSONDecodeError, OSError):
            self._data = []

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=0)

    def all(self) -> list[dict]:
        with self._lock:
            return [dict(p) for p in self._data]

    def count(self) -> int:
        with self._lock:
            return len(self._data)

    def append_sorted(self, patient: dict, score_key: str = "composite_score") -> None:
        with self._lock:
            self._data.append(patient)
            self._data.sort(key=lambda p: p.get(score_key, 0), reverse=True)
            self._save()

    def get(self, patient_id: str) -> dict | None:
        with self._lock:
            for p in self._data:
                if p.get("patient_id") == patient_id:
                    return dict(p)
            return None

    def iter_for_stats(self) -> list[dict]:
        with self._lock:
            return [dict(p) for p in self._data]
