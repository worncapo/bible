#!/usr/bin/env python3
"""
Retrieve NET Bible passages with optional translator notes.

Usage:
    python query_verse.py "John 3:16"
    python query_verse.py "Genesis 1:1-5"
    python query_verse.py "Psalm 23"
    python query_verse.py "Rom 8:28,38" --notes
    python query_verse.py "John 3:16" --notes --notes-type sn

Flags:
    --notes            Include translator notes (off by default)
    --notes-type TYPE  Restrict to one note type: tn, sn, tc, map, etc.
    --json             Emit JSON instead of formatted text
"""
import argparse
import json
import sys

from _common import net, parse_reference


def get_passage(ref_str):
    ref = parse_reference(ref_str)
    bible = net()
    tr_label = bible["meta"]["name"]
    book_data = bible["books"].get(ref["book"])
    if not book_data:
        raise ValueError(f"Book not found: {ref['book']}")
    chap = book_data["chapters"].get(str(ref["chapter"]))
    if not chap:
        raise ValueError(f"Chapter not found: {ref['book']} {ref['chapter']}")
    verses_wanted = ref["verses"] if ref["verses"] else sorted(int(v) for v in chap.keys())
    results = []
    for v in verses_wanted:
        v_data = chap.get(str(v))
        if not v_data:
            results.append({
                "ref": f"{ref['book']} {ref['chapter']}:{v}",
                "translation": tr_label,
                "text": None,
                "notes": [],
            })
        else:
            results.append({
                "ref": f"{ref['book']} {ref['chapter']}:{v}",
                "translation": tr_label,
                "text": v_data["text"],
                "notes": v_data.get("notes", []),
            })
    return results


def format_output(results, include_notes=False, notes_type=None):
    lines = []
    for r in results:
        if r["text"] is None:
            lines.append(f"{r['ref']} ({r['translation']}) [verse not found]")
            continue
        lines.append(f"{r['ref']} ({r['translation']})  {r['text']}")
        if include_notes and r["notes"]:
            for n in r["notes"]:
                if notes_type and n["type"] != notes_type:
                    continue
                lines.append(f"    [{n['type']}] {n['text']}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("reference", help='e.g. "John 3:16" or "Gen 1:1-5" or "Ps 23"')
    p.add_argument("--notes", action="store_true", help="Include translator notes")
    p.add_argument("--notes-type", help="Restrict to one note type (tn/sn/tc/map/...)")
    p.add_argument("--json", action="store_true", help="Emit JSON")
    args = p.parse_args()

    try:
        results = get_passage(args.reference)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        out = results
        if args.notes_type:
            for r in out:
                r["notes"] = [n for n in r["notes"] if n["type"] == args.notes_type]
        if not args.notes:
            for r in out:
                r["notes"] = []
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_output(results, include_notes=args.notes, notes_type=args.notes_type))


if __name__ == "__main__":
    main()
