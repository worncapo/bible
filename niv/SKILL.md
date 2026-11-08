---
name: niv
description: NIV Bible verse and passage lookup. Use this skill whenever the user requests scripture in the NIV (New International Version), asks for a verse by reference in NIV, or wants the NIV rendering of any passage. Handles single verses (John 3:16), verse ranges (Romans 8:28-30), and full chapters (Psalm 23). All 66 books are bundled - no downloads or setup required.
---

# NIV Bible Skill

Full NIV text, 66 books, 31,102 verses. Text-only (no translator notes). For NET Bible with translator notes, cross-references, and Strong's lexicon, use the `/bible` skill.

## Session Setup

Resolve the skill root before running any script:

```bash
NIV_ROOT=""
for candidate in \
    "/mnt/skills/plugins/niv" \
    "/mnt/user-data/uploads/niv" \
    "/root/.claude/skills/synced/niv"; do
  if [ -f "$candidate/SKILL.md" ]; then
    NIV_ROOT="$candidate"
    break
  fi
done
if [ -z "$NIV_ROOT" ]; then
  NIV_ROOT=$(find /root/.claude/skills/synced -maxdepth 4 -name "SKILL.md" 2>/dev/null \
    | xargs grep -l "^name: niv$" 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
fi
[ -z "$NIV_ROOT" ] && echo "ERROR: NIV skill root not found" && exit 1
echo "NIV_ROOT=$NIV_ROOT"
```

## Lookup

```bash
cd "$NIV_ROOT" && python3 scripts/query_verse.py "John 3:16"
cd "$NIV_ROOT" && python3 scripts/query_verse.py "Romans 8:28-30"
cd "$NIV_ROOT" && python3 scripts/query_verse.py "Psalm 23"
cd "$NIV_ROOT" && python3 scripts/query_verse.py "Gen 1:1-5"
cd "$NIV_ROOT" && python3 scripts/query_verse.py "1 Cor 13:4-7"
```

Flexible book names work: `Jn`, `john`, `1 Cor`, `1cor`, `ps`, `psalm`, `Psalms`, `Rev`, etc.

## Output Format

Present the script output verbatim inside a blockquote. Single verse example:

> **John 3:16 (NIV)**
> 16 For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.

Multi-verse passages flow as continuous prose with Unicode superscript verse numbers, no line breaks between verses:

> **1 Samuel 6:1-4 (NIV)**
> ¹ When the ark of the LORD had been in Philistine territory seven months, ² the Philistines called for the priests and the diviners and said, "What shall we do with the ark of the LORD? ³ They answered, "If you return the ark of the god of Israel..." ⁴ The Philistines asked, "What guilt offering should we send?"

Always cite `(NIV)` after the reference. Bold the reference header.

## Accepted Book Names

Accepts standard abbreviations, full names, and common alternates. Examples:

| Input | Resolves to |
|---|---|
| `Gen`, `genesis` | Genesis |
| `Ps`, `psalm`, `psalms` | Psalms |
| `Song`, `SOS`, `song of songs`, `canticles` | Song of Solomon |
| `Jn`, `john` | John |
| `1co`, `1 cor`, `1corinthians` | 1 Corinthians |
| `Rev`, `revelation` | Revelation |

Full alias list in `data/references/book_aliases.json`.

## Cross-translation Comparison

To show NIV alongside NET:
1. Run the `/bible` skill for NET text.
2. Run `/niv` for NIV text.
3. Present both with clear labels in the response.
