# Bible Skills for Claude

Two Claude skills for in-chat scripture lookup. Install each as a .skill file at [claude.ai/skills](https://claude.ai/skills).

---

## NET Skill (
et/)

Full NET Bible with translator notes, cross-references, and Strong's lexicon.

- Verse lookup: single verses, ranges, full chapters, comma-separated
- Full-text search with regex, word, and phrase modes
- Translator notes (tn), study notes (sn), textual criticism notes (tc)
- TSK cross-references and Strong's Greek/Hebrew lexicon (optional data files)

> **Note:** 
et.json (~22 MB) is bundled. The skill is fully self-contained.

---

## NIV Skill (
iv/)

Full NIV text, all 66 books, 31,102 verses. Text-only, no translator notes.

- Fully bundled — 
iv.json is included, no downloads or setup required
- Verse lookup: single verses, ranges, full chapters
- Flexible book name input (abbreviations, full names, common alternates)

---

## Usage

Invoke by name in any Claude chat:

```
/bible John 3:16
/bible Romans 8:28-30 --notes
/niv Psalm 23
```

For cross-translation comparison, run both skills and present side by side.
