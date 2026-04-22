---
name: DCT Cx Issue Tracker & Resolution Playbook
description: Recurring DCT customer experience issues with root causes and resolution steps — Add option CA restriction, live deal visibility (mls-rin), price update CE, deal edit on live deal, emoji stuck case, contract loading.
type: reference
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## DCT Cx Issue Tracker & Resolution Playbook

### Purpose
Quick reference for support, engineering, and product teams to document recurring customer issues, root causes, and resolution steps.

---

## Issue Log

### 1. NAM Merchant Unable to Add New Deal Option
- **Summary:** "Add" option link unavailable for NAM merchant trying to add a new deal option
- **Root Cause:** Merchant is from **CA (Canada)** — CA is **not in the whitelisted countries** for "Add Option"
- **Resolution:** Add Option is not permitted for CA merchants — expected behavior, not a bug
- **Thread:** https://chat.google.com/room/AAAA1_WDuMU/ybKQ1vO_AFw

---

### 2. Live Deal Not Showing Up in Merchant Center
- **Summary:** Opportunity just launched but not visible in MC
- **Root Cause:** Live deal listing is handled by **mls-rin** service — not a DCT/MC issue
- **Resolution:** Tag **@mls-rin** team to investigate
- **Thread:** https://chat.google.com/room/AAAA1_WDuMU/eHdXfrcSIvI

---

### 3. Price Update Not Working — Campaign Editor
- **Summary:** Price update failing in Campaign Editor
- **Jira:** https://groupondev.atlassian.net/browse/DL-3223
- **Resolution:** Under investigation (tracked in Jira DL-3223)

---

### 4. Deal Edit Option Not Showing on Live Deal
- **Summary:** Edit option not appearing for a live deal
- **Resolution:** *(pending — document with steps when resolved)*

---

### 5. Stuck Case — Emoji in Description / Highlight
- **Summary:** Case stuck due to emoji used in deal description or highlight field
- **Resolution:** *(pending — document with steps when resolved)*

---

### 6. Contract Not Loading on CB
- **Summary:** Contract page not loading in CB (Campaign Builder)
- **Resolution:** *(pending — document with steps when resolved)*

---

## Key Patterns / Notes
- **CA (Canada)** is not whitelisted for "Add Option" in CE — do not treat as a bug
- **Live deal visibility** issues → always check with **mls-rin** team first
- **Emoji in text fields** can cause stuck cases — advise merchants to avoid special characters
- **Price changes** in CE → track against DL-3223 for known failure states
