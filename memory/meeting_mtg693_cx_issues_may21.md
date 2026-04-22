---
name: MTG-693 Cx Issues Resolution - May 21 2025
description: Meeting notes from May 21 2025 covering critical Merchant Center issues: missing New Campaign button (mca domain), price edit failures, MCM deal helper errors, campaign edit 503 errors, location null pointer, duplicate threads, deal submission to campaign manager.
type: project
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## Meeting: [MTG-693] Cx Issues Resolution
**Date:** May 21, 2025
**Attendees:** Mayank Jain, Prachi Agrawal, Rohit Jain

---

## Issues Discussed

### 1. New Campaign Button Missing (mca domain)
- **Reporter:** Mayank Jain — button missing for Team Merchant user
- **Root Cause:** New Campaign button is only supported in the **.com domain** — not in the **mca domain merchant**
- **Status:** Prachi confirmed edit option availability after checking

---

### 2. Price Change / Edit Not Available
- **Issue:** No edit option, no open cases, no promotional pricing available on MC opportunity
- **Also:** Unable to change price for merchant logins who are **not the account owner**
- **Note:** Price changes being **disabled in certain countries** was discussed
- **Suspected:** Unified API failure blocking add/edit actions
- **Action:** Screenshot of issue requested

---

### 3. MCM Deal Helper — Redemption Method Error
- **Error:** `"No such element. No value found"` (Mayank) / `"Something went wrong"` (Prachi)
- **Context:** Related to MCM deal helper redemption method
- **Root Cause:** Creation with a specific redemption method is **not supported**
- **Topics discussed:** Deal IDs, redemption instructions, locations

---

### 4. Merchant Center — Edit Campaign Issues (503 Error)
- **Issue:** Merchant unable to edit campaign in MC
- **Error:** `503` error observed
- **Action:** Merchant ID provided for checking logs; tickets requested
- **Also:** Gmail and unified call returning 503 — advised to check deal snapshot for errors

---

### 5. Location Details & Deal Snapshots — Null Pointer Exception
- **Error:** `NullPointerException` related to location details and deal redemption locations
- **Context:** Issue with "bookie deal" — place object / definition IDs involved
- **Action:** Check deal snapshot; Prachi added ID to snapshot, Rohit confirmed receipt

---

### 6. Duplicate Threads & Location IDs
- **Issue:** Duplicate threads identified related to an ongoing issue
- **Action:** Location ID requested; deal IDs and snapshots reviewed; creation date confirmed

---

### 7. Merchant Unable to Submit Deal to Campaign Manager
- **Reporter:** Mayank Jain
- **Action:** Fix requested; contract and MC link reviewed
- **Status:** Prachi confirmed PR approval

---

### 8. Miscellaneous
- Small **validation issue** noted by Rohit Jain
- Mind Body / Book options discussed
- Fix acknowledged; meeting concluded

---

## Key Takeaways
- New Campaign button is **.com domain only** — not available in mca domain
- Price editing restricted when merchant is **not the account owner**
- Specific redemption methods **not supported** in MCM deal helper
- 503 errors → check **deal snapshot** first
- Null pointer on location details tied to **bookie deal** place object issue
