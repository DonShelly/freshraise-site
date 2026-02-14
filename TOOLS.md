# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## API Rate Limits

- **Brave Search API**: 1 request/second max — space out searches accordingly

## Notion — Schema & Workspace Hygiene

- **Canonical Notion schema (source of truth):** https://www.notion.so/Notion-Schema-Source-of-Truth-307072a76392814aa7e8dd3eb9a6cc4e
- **Rule:** If the schema changes, update the Notion schema page first, then follow it everywhere (Ops/Main/Tech).

## Notion — Business Separation

- Keep **10K MRR** files/pages in a **separate Notion section** from the **runway-generation business** materials (e.g., FreshRaise UK). These are two distinct businesses and should not be mixed.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
