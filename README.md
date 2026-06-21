# JARVIS — Ahmed Al Akib's University Assistant
## 100% Free, 100% Offline — No API Key, No Signup, No Cost

---

## ✅ What changed
This version needs **zero setup**. No API key, no account, no internet
connection required for the assistant brain. Everything — chat, exams,
projects, notes, cover pages, slide outlines — runs directly in your browser.

The trade-off: the built-in "JARVIS Assistant" is rule-based, not a full AI
model. It's great at organizing your university life (exams, deadlines,
projects, notes, email templates, study plans, cover pages) but it won't
hold an open-ended conversation the way ChatGPT/Claude would. If you ever
want that, the Settings page has notes on how to add a free AI later —
but you don't need to for anything to work today.

---

## 📁 Files
- `jarvis.html` — the app itself. Just double-click to open.
- `jarvis_launcher.py` — optional clap-to-open detector
- `README.md` — this guide

Keep both files in the same folder, e.g. `C:\Users\Akib\JARVIS\`

---

## ⚡ Quick Start (30 seconds)
1. Double-click `jarvis.html`
2. It opens in your browser — that's it, you're done
3. Your name, ID (2024-3-50-024), university (EWU), and email are already filled in

No login. No key. No payment. Ever.

---

## 🎯 What you can do right now

**Dashboard** — live clock, today's stats, upcoming exams and projects at a glance

**JARVIS Assistant (Chat tab)** — type things like:
- `add exam` → jumps to exam tracker
- `new project lab report` → jumps to project creator
- `study plan for data structures` → generates a 7-day study plan
- `email professor about extension` → generates a ready-to-send email draft
- `note: bring calculator tomorrow` → saves instantly to notes
- `remind me to submit assignment` → saves as a tagged reminder
- `what is due soon` → shows your nearest exams/deadlines
- `array`, `oop`, `tcp`, `recursion`, `big o`, etc. → quick CSE concept explainers
- `help` → see all commands

**Projects** — create a project, add a task list, check off tasks, see progress %

**Daily Notes** — quick notes, tagged (class/idea/reminder/todo), searchable by browsing

**Exam Dates** — add subject, date, time, room → automatic countdown in days, color-coded by urgency

**University Mail** — one click opens Gmail or Outlook for 2024-3-50-024@std.ewubd.edu

**Cover Page** — fill assignment title/course/teacher → auto-generates an EWU-style
cover page with your info pre-filled → Print → Save as PDF

**Slides Generator** — type a topic → get a structured slide-by-slide outline
(title slide, intro, key concepts, applications, conclusion, etc.) you can
copy into PowerPoint or Google Slides

---

## 🎙️ "Hello Piko" Voice Wake Word + Voice Commands (optional)

This makes JARVIS open automatically when you say "Hello Piko" — and now
it can also carry your actual command, so you can talk to it like Jarvis:

- **"Hello Piko"** alone → just opens JARVIS
- **"Hello Piko, remind me to submit the lab report"** → opens JARVIS AND
  automatically sends "remind me to submit the lab report" to the assistant
- **"Hello Piko, I have an exam tomorrow"** → opens JARVIS and takes you
  straight to the Exam Dates tab
- If you just say "Hello Piko" with nothing after it, it'll wait a few
  seconds and ask you (silently, via the terminal) — just keep talking
  and it'll pick up your next sentence as the command

### You already have Python 3.11 set up — good, keep using it

In VS Code, make sure your interpreter is still set to 3.11 (bottom-right
status bar should show `3.11.x`).

### Install the extra package needed (if not already done)
```
python -m pip install SpeechRecognition pyaudio
```

### Test your microphone
```
python jarvis_voice.py --test
```

> Note: this uses Google's free speech recognition service in the background,
> so it needs an internet connection to work (the rest of JARVIS does not).

### Run it
```
python jarvis_voice.py
```
Leave this running in the background. Try saying:
- "Hello Piko, make a reminder to bring my calculator"
- "Hello Piko, what is due soon"
- "Hello Piko, study plan for data structures"

You can change the wake word by opening `jarvis_voice.py`, finding this line
near the top, and editing it:
```python
WAKE_WORDS = ["hello piko", "hey piko", "piko"]
```

### Auto-start on boot (Windows)
1. `Win + R` → type `shell:startup` → Enter
2. Right-click → New → Shortcut
3. Target: `pythonw "C:\Users\ahmed\Downloads\JARVIS\jarvis_voice.py"`
4. Name it "JARVIS Voice Listener" → Finish

Now every time you turn on your laptop, the voice listener starts silently
in the background, and saying "Hello Piko" (with or without a command after
it) opens JARVIS and does whatever you asked.

### Auto-start on boot (Mac)
System Settings → General → Login Items → `+` → select `jarvis_voice.py`

---

## 👏 Old clap-detector (jarvis_launcher.py)
This file is still included if you'd rather use clapping instead of voice —
it works the same way, just run `python jarvis_launcher.py --test` to
calibrate and `python jarvis_launcher.py` to run it. Not required if you're
using the voice version above.

---

## 💾 Your data
Everything (notes, projects, exams) is stored in your browser's local storage
on your own laptop — nothing leaves your device, nothing is uploaded anywhere.
If you clear your browser data, you'll lose it, so avoid clearing site data
for this page, or periodically note down anything critical elsewhere.

---

## 🚀 Want a smarter AI later?
If you ever want richer conversational AI (real Q&A, code debugging, essay
help), Google AI Studio (aistudio.google.com) offers a genuinely free API
key — no credit card needed. But this is completely optional; everything
above works without it.

---

Built for Ahmed Al Akib · East West University · CSE Dept. ICE Program · Summer 2026 🎓
