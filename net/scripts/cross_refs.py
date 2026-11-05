#!/usr/bin/env python3
"""
Look up Treasury of Scripture Knowledge (TSK) cross-references for a verse.

Usage:
    python cross_refs.py "John 3:16"
    python cross_refs.py "Gen 1:1" --limit 10
    python cross_refs.py "Rom 8:28" --with-text   # include NET text for each ref

Notes:
    Each ref has a "votes" score from openbible.info indicating popular
    assessment of how relevant the cross-reference is. Higher = more relevant.
    Default output is sorted by votes descending.
"""
import argparse
import json
import sys

from _common import tsk, net, parse_reference

def lookup(ref_str, limit=None):
    ref = parse_reference(ref_str)
    if not ref["verses"] or len(ref["verses"]) != 1:
        raise ValueError("cross_refs requires a single verse reference, e.g. 'John 3:16'")
    v = ref["verses"][0]
    key = f"{ref['book']}|{ref['chapter']}|{v}"
    # Compact on-disk format: [[ref_str, votes], ...]
    raw = tsk().get(key, [])
    refs = [{"ref": r[0], "votes": r[1]} for r in raw]
    if limit:
        refs = refs[:limit]
    return {
        "ref": f"{ref['book']} {ref['chapter']}:{v}",
        "total": len(raw),
        "returned": len(refs),
        "cross_refs": refs,
    }

def attach_text(result):
    bible = net()
    for r in result["cross_refs"]:
        target = r["ref"]
        # Parse "Book C:V" or "Book C:V-V"
        try:
            if "-" in target.split(":")[-1]:
                first_part, verse_range = target.rsplit(":", 1)
                start_v, end_v = verse_range.split("-")
                parsed = parse_reference(f"{first_part}:{start_v}")
                # Get just the first verse for brevity
                v_data = bible["books"][parsed["book"]]["chapters"][str(parsed["chapter"])].get(start_v)
                r["text"] = v_data["text"] if v_data else None
                r["note"] = f"(range, showing first verse only; range to v{end_v})"
            else:
                parsed = parse_reference(target)
                v = parsed["verses"][0]
                v_data = bible["books"][parsed["book"]]["chapters"][str(parsed["chapter"])].get(str(v))
                r["text"] = v_data["text"] if v_data else None
        except Exception as e:
            r["text"] = None
            r["error"] = str(e)

def format_output(result, with_text=False):
    lines = [f"Cross-references for {result['ref']}  ({result['returned']} of {result['total']} shown)"]
    for r in result["cross_refs"]:
        line = f"  {r['ref']:25s}  (votes: {r['votes']})"
        if with_text and r.get("text"):
            line += f"\n      {r['text']}"
        lines.append(line)
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("reference")
    p.add_argument("--limit", type=int, default=15, help="Max refs to return (default 15)")
    p.add_argument("--with-text", action="store_true", help="Include NET text for each ref")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    try:
        result = lookup(args.reference, limit=args.limit)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.with_text:
        attach_text(result)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result, with_text=args.with_text))

if __name__ == "__main__":
    main()
