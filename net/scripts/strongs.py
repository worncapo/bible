#!/usr/bin/env python3
"""
Look up a Strong's Concordance entry by its number.

Usage:
    python strongs.py G26          # Greek #26: agape
    python strongs.py H7225        # Hebrew #7225: reshith
    python strongs.py G26 --json
    python strongs.py --search "love"       # Search definitions (Greek+Hebrew)
    python strongs.py --search "love" --greek
"""
import argparse
import json
import sys

from _common import strongs_greek, strongs_hebrew

def lookup(code):
    code = code.upper().strip()
    if code.startswith("G"):
        d = strongs_greek()
    elif code.startswith("H"):
        d = strongs_hebrew()
    else:
        raise ValueError("Code must start with G (Greek) or H (Hebrew)")
    entry = d.get(code)
    if not entry:
        raise ValueError(f"No entry: {code}")
    return {"code": code, **entry}

def search(query, greek=True, hebrew=True, limit=20):
    q = query.lower()
    hits = []
    sources = []
    if greek:
        sources.append(("Greek", strongs_greek()))
    if hebrew:
        sources.append(("Hebrew", strongs_hebrew()))
    for lang, d in sources:
        for code, entry in d.items():
            hay = " ".join(str(v) for v in entry.values()).lower()
            if q in hay:
                hits.append({"code": code, "lang": lang, **entry})
                if len(hits) >= limit:
                    return hits
    return hits

def format_entry(e):
    lines = [f"{e['code']}  {e.get('lemma', '')}  ({e.get('translit', '')})"]
    if "strongs_def" in e:
        lines.append(f"  Definition: {e['strongs_def'].strip()}")
    if "kjv_def" in e:
        lines.append(f"  KJV uses:   {e['kjv_def']}")
    if "derivation" in e:
        lines.append(f"  Derivation: {e['derivation'].strip()}")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("code", nargs="?", help="Strong's code (G### or H####)")
    p.add_argument("--search", dest="search_q", help="Search entries by text")
    p.add_argument("--greek", action="store_true", help="Greek only (with --search)")
    p.add_argument("--hebrew", action="store_true", help="Hebrew only (with --search)")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.search_q:
        g = args.greek or not (args.greek or args.hebrew)
        h = args.hebrew or not (args.greek or args.hebrew)
        hits = search(args.search_q, greek=g, hebrew=h, limit=args.limit)
        if args.json:
            print(json.dumps(hits, ensure_ascii=False, indent=2))
        else:
            if not hits:
                print("No matches.")
            for e in hits:
                print(format_entry(e))
                print()
        return

    if not args.code:
        p.error("Provide a code (e.g. G26) or use --search")
    try:
        e = lookup(args.code)
    except ValueError as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps(e, ensure_ascii=False, indent=2))
    else:
        print(format_entry(e))

if __name__ == "__main__":
    main()
