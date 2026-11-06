<div align="center">

# Bible Skills for Claude

</div>

I made these for my own Bible study. I wanted to be able to ask Claude about a passage, get the actual text, dig into the original Hebrew or Greek, and read translator notes, all without switching apps or tabs. So I built it as a Claude skill, and it worked well enough that I figured I'd put it out there for anyone else who studies this way.

There are two skills: one for the NET Bible (deep study, translator notes, Strong's lexicon) and one for the NIV (clean text, quick lookup).

---

<div align="center">

<a href="https://github.com/worncapo/bible/releases/latest/download/net-bible.skill">
  <img src="https://img.shields.io/badge/Download-NET%20Bible%20Skill-2d6db3?style=for-the-badge" alt="Download NET Bible Skill">
</a>
&nbsp;&nbsp;
<a href="https://github.com/worncapo/bible/releases/latest/download/niv-bible.skill">
  <img src="https://img.shields.io/badge/Download-NIV%20Skill-4a7c3f?style=for-the-badge" alt="Download NIV Skill">
</a>

</div>

---

## How to install

1. Download a skill file above
2. Go to [claude.ai/skills](https://claude.ai/skills), click **Upload skill**, select the file

That's it.

---

## How I use it

The most natural way is just to ask your question and put the skill name at the end. Claude pulls the text and answers in context.

```
What is the context of Romans 3:23? /bible
```

```
What does "sanctified" mean in 1 Corinthians 1:2? Break down the Greek. /bible
```

```
Show me John 1:1 in both translations and compare them. /bible /niv
```

```
Walk me through Genesis 1:1-3 with the translator notes. /bible
```

You can also just call it directly for a quick lookup:

```
/bible Romans 8:28-30
/niv 1 Corinthians 13:4-7
```

---

## What's in each one

**NET Bible (`/bible`)** is the scholar translation, built for study. It comes with translator notes that explain word choices and grammar, study notes with historical and theological context, textual criticism notes, cross-references, and Strong's Greek and Hebrew definitions. Good for going deep on a passage or word.

**NIV (`/niv`)** is the NIV, all 66 books, clean and readable. Good for quick lookups or when you want to compare translations side by side.

---

<div align="center">
<sub>Source in <code>net/</code> and <code>niv/</code>. Skill files are in the <a href="https://github.com/worncapo/bible/releases/latest">latest release</a>.</sub>
</div>
