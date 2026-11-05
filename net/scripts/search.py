#!/usr/bin/env python3
"""
Full-text search across the NET Bible.

Usage:
    python search.py "fear of the Lord"
    python search.py "shepherd" --book Psalms
    python search.py "faith works" --all-words
    python search.py "the word was God" --limit 20

Flags:
    --book NAME  Restrict to one book (canonical name or alias)
    --ot         Old Testament only (Genesis-Malachi)
    --nt         New Testament only (Matthew-Revelation)
    --all-words  Match verses containing ALL terms (default: phrase match)
    --regex      Treat query as a regex (case-insensitive)
    --limit N    Max results (default 50)
    --json       Emit JSON
"""
import argparse
import json
import re
import sys

from _common import net, resolve_book

NT_BOOKS = {
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
}


def iter_verses(book_filter=None, ot=False, nt=False):
    bible = net()
    for book_name, book in bible["books"].items():
        if book_filter and book_name != book_filter:
            continue
        if ot and book_name in NT_BOOKS:
            continue
        if nt and book_name not in NT_BOOKS:
            continue
        for ch_num, chap in book["chapters"].items():
            for v_num, v_data in chap.items():
                yield book_name, int(ch_num), int(v_num), v_data["text"]


def search(query, book=None, ot=False, nt=False, all_words=False, regex=False, limit=50):
    if regex:
        pattern = re.compile(query, re.IGNORECASE)
        def match(text):
            return bool(pattern.search(text))
    elif all_words:
        terms = [t.lower() for t in re.findall(r"\w+", query)]
        def match(text):
            low = text.lower()
            return all(t in low for t in terms)
    else:
        q = query.lower()
        def match(text):
            return q in text.lower()

    book_resolved = resolve_book(book) if book else None
    if book and not book_resolved:
        raise ValueError(f"Unknown book: {book}")

    hits = []
    for b, c, v, text in iter_verses(book_filter=book_resolved, ot=ot, nt=nt):
        if match(text):
            hits.append({"ref": f"{b} {c}:{v}", "text": text})
            if len(hits) >= limit:
                break
    return hits


def format_output(hits, query):
    if not hits:
        return f'No matches for {query!r}.'
    lines = [f"{len(hits)} match(es):"]
    for h in hits:
        lines.append(f"  {h['ref']:30s}  {h['text']}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--book")
    p.add_argument("--ot", action="store_true")
    p.add_argument("--nt", action="store_true")
    p.add_argument("--all-words", action="store_true")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    try:
        hits = search(
            args.query,
            book=args.book,
            ot=args.ot,
            nt=args.nt,
            all_words=args.all_words,
            regex=args.regex,
            limit=args.limit,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except re.error as e:
        print(f"Regex error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        print(format_output(hits, args.query))


if __name__ == "__main__":
    main()
