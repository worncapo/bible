"""Shared helpers for NET Bible skill."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REF  = ROOT / "references"

_net_cache     = None
_tsk_cache     = None
_strongs_g     = None
_strongs_h     = None
_aliases_cache = None


def _load_aliases():
    global _aliases_cache
    if _aliases_cache is None:
        p = REF / "book_aliases.json"
        if p.exists():
            with open(p, encoding="utf-8") as f:
                _aliases_cache = json.load(f)
        else:
            _aliases_cache = {}
    return _aliases_cache


def net() -> dict:
    global _net_cache
    if _net_cache is None:
        p = DATA / "translations" / "net.json"
        if not p.exists():
            raise FileNotFoundError(
                f"net.json not found at {p}. "
                "Download it from https://netbible.org/download and place it at "
                f"{p}"
            )
        with open(p, encoding="utf-8") as f:
            _net_cache = json.load(f)
    return _net_cache


def resolve_book(name: str):
    key = name.strip().lower()
    al = _load_aliases()
    if key in al:
        return al[key]
    for book in net()["books"]:
        if book.lower() == key:
            return book
    return None


_REF_RE = re.compile(
    r"^\s*(?P<book>(?:\d\s*)?[A-Za-z][A-Za-z\s]*?)\s+"
    r"(?P<chap>\d+)"
    r"(?::(?P<verses>[\d,\-\s]+))?"
    r"\s*$"
)


def parse_reference(text: str) -> dict:
    m = _REF_RE.match(text.strip())
    if not m:
        raise ValueError(f"Cannot parse reference: {text!r}")
    book = resolve_book(m.group("book").strip())
    if not book:
        raise ValueError(f"Unknown book: {m.group('book').strip()!r}")
    chapter = int(m.group("chap"))
    verses_str = m.group("verses")
    verses = None
    if verses_str:
        verses = []
        for part in verses_str.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                verses.extend(range(int(a.strip()), int(b.strip()) + 1))
            else:
                verses.append(int(part))
    return {"book": book, "chapter": chapter, "verses": verses}


def tsk(key: str) -> list:
    global _tsk_cache
    p = DATA / "cross_references" / "tsk.json"
    if not p.exists():
        return []
    if _tsk_cache is None:
        with open(p, encoding="utf-8") as f:
            _tsk_cache = json.load(f)
    return _tsk_cache.get(key, [])


def strongs_greek(number: int) -> dict:
    global _strongs_g
    p = DATA / "lexicons" / "strongs_greek.json"
    if not p.exists():
        return {}
    if _strongs_g is None:
        with open(p, encoding="utf-8") as f:
            _strongs_g = json.load(f)
    return _strongs_g.get(str(number), {})


def strongs_hebrew(number: int) -> dict:
    global _strongs_h
    p = DATA / "lexicons" / "strongs_hebrew.json"
    if not p.exists():
        return {}
    if _strongs_h is None:
        with open(p, encoding="utf-8") as f:
            _strongs_h = json.load(f)
    return _strongs_h.get(str(number), {})
