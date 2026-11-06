<div align="center">

# Bible Skills for Claude

</div>

I made these for my own Bible study. I wanted to ask Claude about a passage, get the actual text, dig into the original Hebrew or Greek, and read translator notes, all without switching apps or tabs. Worked well enough that I figured I'd put it out there.

Two skills: one for the NET Bible (deep study, translator notes, Strong's lexicon) and one for the NIV (clean text, quick lookup).

---

<div align="center">

<a href="https://github.com/worncapo/bible/releases/latest/download/net-bible.skill">
  <img src="https://img.shields.io/badge/Download-NET%20Bible-2d6db3?style=for-the-badge" alt="Download NET Bible Skill">
</a>
&nbsp;&nbsp;
<a href="https://github.com/worncapo/bible/releases/latest/download/niv-bible.skill">
  <img src="https://img.shields.io/badge/Download-NIV-4a7c3f?style=for-the-badge" alt="Download NIV Skill">
</a>

</div>

---

## Install

1. Download a skill file above
2. Go to [claude.ai/skills](https://claude.ai/skills), click **Upload skill**, select the file

Done.

---

## How I use it

Ask your question and put the skill name at the end. Claude pulls the text and answers in context.

```
What is the context of Romans 3:23? /bible
What does "sanctified" mean in 1 Corinthians 1:2? Break down the Greek. /bible
Show me John 1:1 in both translations and compare them. /bible /niv
Walk me through Genesis 1:1-3 with the translator notes. /bible
```

Or just call it directly:

```
/bible Romans 8:28-30
/niv 1 Corinthians 13:4-7
```

---

## What's in each one

**NET Bible (`/bible`)** is a scholar translation built for study. Translator notes explaining word choices and grammar, study notes with historical and theological context, textual criticism notes, cross-references, and Strong's Greek and Hebrew definitions. Good for going deep on a passage or word.

**NIV (`/niv`)** is the NIV, all 66 books. Clean and readable. Good for quick lookup or comparing translations.

---

<div align="center">
<sub>Source in <code>net/</code> and <code>niv/</code>. Skill files in the <a href="https://github.com/worncapo/bible/releases/latest">latest release</a>.</sub>
</div>
