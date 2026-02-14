# Notion Schema

**Owner:** Ops Agent  
**Last Updated:** 2026-02-14

This schema defines the structure for our Notion workspace. It's dynamic — update it as new patterns emerge, but always follow it for consistency.

---

## Naming Conventions

### Pages
- **Task pages:** Verb-first, specific action (`Investigate Sophie Zoho credential`, `Generate DNS records`)
- **Reference pages:** Noun-first (`FreshRaise UK — Sample List (Feb 14, 2026)`)
- **Date suffix:** Use ISO format in parentheses when relevant: `(Feb 14, 2026)` or `(2026-02-14)`

### Databases (Data Sources)
- **Title:** CAPS for main identifier, then description (`ELSOLVE Review Inbox`, `FRESHDATA UK Startups`)
- **Keep names short** — full context goes in description

---

## Standard Page Structure

### Task Pages
```
📋 [Task Title]
├── Status: [To Do / In Progress / Done / Blocked]
├── Context: [1-2 sentences]
├── Details: [Full description]
├── Outcome: [What was done]
└── Related: [Links to other pages]
```

### Reference/Report Pages
```
🚀 [Report Title]
├── Summary heading
├── Key metrics/table
├── Detailed sections (H2)
├── Subsections (H3)
├── Callouts for tips/warnings
└── Footer with date/source
```

---

## Icon Conventions

| Type | Icon |
|------|------|
| Task | 📋 |
| Report/List | 🚀 |
| Meeting | 📅 |
| Credential/Secret | 🔐 |
| Research | 🔬 |
| Warning/Alert | ⚠️ |
| Decision | ✅ |
| Blocked | 🚫 |

---

## Database Properties (Standard)

### Task Database
- **Name** (title) — Task description
- **Status** (select) — To Do, In Progress, Done, Blocked
- **Priority** (select) — P0, P1, P2, P3
- **Assignee** (select) — Main, Ops, Tech, CEO
- **Due** (date) — Optional
- **Tags** (multi-select) — Contextual labels

### Lead/Startup Database
- **Company** (title)
- **Funding** (text)
- **Stage** (select)
- **Sector** (select)
- **Location** (text)
- **Founders** (text)
- **Hiring Heat** (select) — 🔥🔥🔥, 🔥🔥, 🔥, ⚡, 🌱
- **URL** (url)
- **LinkedIn** (url)
- **Notes** (rich_text)

---

## Block Patterns

### For Lists
- Use **tables** for structured data (5+ items with multiple attributes)
- Use **bulleted lists** for simple lists
- Use **numbered lists** for ordered steps or rankings

### For Emphasis
- **Callouts** with emoji for tips, warnings, key info
- **Dividers** to separate major sections
- **Bold** for labels, not for entire sentences

### For Links
- Inline links for references
- Link blocks for related pages

---

## Business Separation (Hard Rule)

- Keep **10K MRR** files/pages in a **separate Notion section** from the **runway-generation business** materials (e.g., FreshRaise UK). These are two distinct businesses and should not be mixed.

---

## Maintenance Rules

1. **Before creating a page:** Search for existing similar pages
2. **Before creating a database:** Check if an existing one fits
3. **After major changes:** Update this schema if new patterns emerge
4. **Quarterly:** Review and clean up orphan pages

---

*This schema is enforced by the Ops agent. Ping Ops if you're unsure about structure.*
