"""Shared helpers for NIV Bible skill."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

_niv_cache = None
_aliases_cache = None


def niv() -> dict:
    global _niv_cache
    if _niv_cache is None:
        p = DATA / "translations" / "niv.json"
        if not p.exists():
            raise FileNotFoundError(
                f"niv.json not found at {p}. The skill package may be incomplete."
            )
        with open(p, encoding="utf-8") as f:
            _niv_cache = json.load(f)
    return _niv_cache


def resolve_book(name: str):
    global _aliases_cache
    if _aliases_cache is None:
        p = DATA / "references" / "book_aliases.json"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                _aliases_cache = json.load(f)
        else:
            _aliases_cache = {}
    key = name.strip().lower()
    if key in _aliases_cache:
        return _aliases_cache[key]
    for book in niv()["books"]:
        if book.lower() == key:
            return book
    return None
