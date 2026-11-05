#!/usr/bin/env python3
"""
NIV Bible verse and passage lookup.

Usage:
    python query_verse.py "John 3:16"
    python query_verse.py "Romans 8:28-30"
    python query_verse.py "Psalm 23"
    python query_verse.py "Gen 1:1-5"
    python query_verse.py "1 Cor 13:4-7"
"""
import argparse
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import niv, resolve_book

_REF_RE = re.compile(
    r"^\s*(?P<book>(?:\d\s+)?[A-Za-z][A-Za-z\s]+?)\s+"
    r"(?P<chap>\d+)"
    r"(?::(?P<verses>[\d,\s\-]+))?"
    r"\s*$"
)


def parse_ref(text):
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
    return book, chapter, verses


def lookup(ref_str):
    book, chapter, verses = parse_ref(ref_str)
    data = niv()
    book_data = data["books"].get(book)
    if not book_data:
        raise ValueError(f"Book not found: {book}")
    chap = book_data["chapters"].get(str(chapter))
    if not chap:
        raise ValueError(f"Chapter not found: {book} {chapter}")
    verse_nums = verses if verses else sorted(int(v) for v in chap.keys())
    lines = []
    for v in verse_nums:
        text = chap.get(str(v))
        if text is None:
            lines.append(f"{book} {chapter}:{v} (NIV) [verse not found]")
        else:
            lines.append(f"{v} {text}")
    ref_label = f"{book} {chapter}"
    if verses:
        if len(verses) == 1:
            ref_label += f":{verses[0]}"
        else:
            ref_label += f":{verses[0]}-{verses[-1]}"
    return f"{ref_label} (NIV)\n" + "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("reference", help='e.g. "John 3:16" or "Gen 1:1-5" or "Ps 23"')
    args = p.parse_args()
    try:
        print(lookup(args.reference))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
