<div align="center">

# Bible Skills for Claude

</div>

Earlier this year I made these for my own Bible study. I wanted to be able to ask Claude about a passage and get the actual text. Over time I found I could dig into the original Hebrew or Greek, read translator and study notes... So I built it as a Claude skill, and I've used it a ton, so I felt called to put it out for others as well.

Mind you, none of this is meant to replace prayer, the holy spirit, your own critical thinking, or your relationship with Jesus. Don't be like me and let Claude chats become an idol! Talk and ask God first and foremost. This is just a tool after all.

There are two skills: one for the NET Bible (casual study, translator notes, Strong's lexicon) and one for the NIV (easy to read, quick lookup).
I often use NIV for longer passages and NET for study. Asking about the Hebrew or Greek has been super cool and helped my walk with Christ immensely. It's dope when you actually know what God was intending to say!

---

## How to install

**Step 1.** Download a skill:

<div align="center">

<a href="https://github.com/worncapo/bible/releases/latest/download/net-bible.skill">
  <img src="https://img.shields.io/badge/%E2%AC%87%20NET%20Bible%20Skill-2d6db3?style=for-the-badge" alt="Download NET Bible Skill">
</a>
&nbsp;&nbsp;
<a href="https://github.com/worncapo/bible/releases/latest/download/niv-bible.skill">
  <img src="https://img.shields.io/badge/%E2%AC%87%20NIV%20Skill-4a7c3f?style=for-the-badge" alt="Download NIV Skill">
</a>

</div>

<br>

**Step 2.** Go to [claude.ai/skills](https://claude.ai/skills), click **Upload skill**, select the file


---

## How I use it, in depth

The most natural way is just to ask your question and put the skill name at the end. Claude pulls the text and answers in context.

```
What's the context of Romans 3:23? /bible
```

```
What does "sanctified" mean in 1 Corinthians 1:2? Break down the Greek /bible
```

```
Pull John 1:1 in both translations and compare them /bible /niv
```

```
Walk me through Genesis 1:1-3 with the translator and study notes /bible
```

You can also just call it directly for a quick lookup:

```
/bible Romans 8:28-30
/niv 1 Corinthians 13:4-7
```

---

## What's in each one

**NET Bible (`/bible`)** is the scholar translation, built for study. Definitely my workhorse. It comes with translator notes that explain word choices and grammar, study notes with historical and theological context, textual criticism notes, cross-references, and Strong's Greek and Hebrew definitions. Good for quick pulls or going deep on a passage or word, I use this very often when studying.

**NIV (`/niv`)** is the NIV, all 66 books, clean and readable. I use it for quick lookups, easy reading, or when you want to compare translations side by side.

---

<div align="center">
<sub>Source in <code>net/</code> and <code>niv/</code>. Skill files are in the <a href="https://github.com/worncapo/bible/releases/latest">latest release</a>.</sub>
</div>
