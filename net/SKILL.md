---
name: bible
description: NET Bible lookup with translator notes, cross-references, and Strong's lexicon entries. Use this skill whenever the user asks for scripture, a Bible verse, a passage, wants to look up a reference, or needs translator notes (tn), study notes (sn), or textual criticism notes (tc). Handles single verses (John 3:16), verse ranges (Romans 8:28-30), full chapters (Psalm 23), comma-separated verses (Rom 8:28,38), and word or topic searches. For NIV text, use the /niv skill.
---

# NET Bible Skill

Full NET Bible text with translator notes, cross-references, and Strong's lexicon. Data loads from local disk, no network required at lookup time.

## Session Setup

Resolve the skill root, then verify the data file exists:

```bash
BIBLE_ROOT=""
for candidate in \
    "/mnt/skills/plugins/bible" \
    "/mnt/user-data/uploads/bible" \
    "/root/.claude/skills/synced/bible"; do
  if [ -f "$candidate/SKILL.md" ]; then
    BIBLE_ROOT="$candidate"
    break
  fi
done
if [ -z "$BIBLE_ROOT" ]; then
  BIBLE_ROOT=$(find /root/.claude/skills/synced -maxdepth 4 -name "SKILL.md" 2>/dev/null \
    | xargs grep -l "^name: bible$" 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
fi
[ -z "$BIBLE_ROOT" ] && echo "ERROR: Bible skill root not found" && exit 1
echo "BIBLE_ROOT=$BIBLE_ROOT"
ls "$BIBLE_ROOT/data/translations/"
```

## Auto-Repair

If scripts are missing or outdated, regenerate them (run once per session if needed):

```bash
# Regenerate _common.py
cat > "$BIBLE_ROOT/scripts/_common.py" << 'PYEOF'
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


def tsk(book: str, chapter: int, verse: int) -> list:
    global _tsk_cache
    p = DATA / "cross_references" / "tsk.json"
    if not p.exists():
        return []
    if _tsk_cache is None:
        with open(p, encoding="utf-8") as f:
            _tsk_cache = json.load(f)
    return _tsk_cache.get(book, {}).get(str(chapter), {}).get(str(verse), [])


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
PYEOF
echo "_common.py written"
```

```bash
# Regenerate query_verse.py
cat > "$BIBLE_ROOT/scripts/query_verse.py" << 'PYEOF'
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
PYEOF
echo "query_verse.py written"
```

```bash
# Regenerate search.py
cat > "$BIBLE_ROOT/scripts/search.py" << 'PYEOF'
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
PYEOF
echo "search.py written"
```

## Verse Lookup

```bash
cd "$BIBLE_ROOT/scripts" && python3 query_verse.py "John 3:16"
cd "$BIBLE_ROOT/scripts" && python3 query_verse.py "Genesis 1:1-5"
cd "$BIBLE_ROOT/scripts" && python3 query_verse.py "Psalm 23"
cd "$BIBLE_ROOT/scripts" && python3 query_verse.py "Rom 8:28,38" --notes
cd "$BIBLE_ROOT/scripts" && python3 query_verse.py "John 3:16" --notes --notes-type sn
```

## Search

```bash
cd "$BIBLE_ROOT/scripts" && python3 search.py "fear of the Lord"
cd "$BIBLE_ROOT/scripts" && python3 search.py "shepherd" --book Psalms
cd "$BIBLE_ROOT/scripts" && python3 search.py "faith hope love" --all-words --nt
cd "$BIBLE_ROOT/scripts" && python3 search.py "word.*God" --regex --limit 10
```

## Note Types

| Code | Meaning |
|------|---------|
| `tn` | Translator's note — word choice, grammar, alternate rendering |
| `sn` | Study note — context, background, theological significance |
| `tc` | Textual criticism — manuscript variants |
| `map` | Map reference |

## Output Format

Present NET text inline in the response. Format:

> **John 3:16 (NET)**
> "For this is the way God loved the world: He gave his one and only Son, so that everyone who believes in him will not perish but have eternal life."

For study notes, include them below the verse text under a **Notes** heading.

## Data Architecture

```
references/
  book_aliases.json     # book name abbreviations and aliases
data/
  translations/
    net.json            # ~22 MB — full NET text + notes (not bundled; must be present)
  cross_references/
    tsk.json            # Treasury of Scripture Knowledge (optional)
  lexicons/
    strongs_greek.json  # Greek lexicon (optional)
    strongs_hebrew.json # Hebrew lexicon (optional)
scripts/
  _common.py            # shared helpers
  query_verse.py        # verse/passage lookup
  search.py             # full-text search
  cross_refs.py         # cross-reference lookup
  strongs.py            # Strong's lexicon lookup
```

net.json is not bundled due to size (~22 MB). It must be present in `data/translations/` for this skill to work. If missing, the scripts will print a clear error with the expected path.

## Limitations

- NET Bible only. For NIV text, use the `/niv` skill.
- Translator notes, TSK cross-references, and Strong's entries require the corresponding optional data files.
