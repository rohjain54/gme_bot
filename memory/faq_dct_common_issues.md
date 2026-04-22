---
name: DCT Common Issues - Sales Rep Challenges & Resolutions
description: Common DCT (Deal Creation Tool) issues faced by sales reps: access problems, failed submissions, PDS issues, deal restructuring, sync issues, and known limitations/improvements.
type: reference
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## Summary: Common Sales Rep Challenges with DCT

### Top-Level Issues (Strong Adoption Push)
- **Access Problems**: Reps frequently can't access DCT; unexplained errors or inability to reach certain Merchant Centers.
- **Failed Submissions**: DCT allows actions that fail at submission:
  - Linking opportunities in incorrect stages
  - Modifying outdated drafts
  - Choosing inactive PDS
- **Deal Restructuring**: Changing deal info post-submission is unclear for reps.
- **New BDs (US)**: Follow structured sales process involving SF opportunity stage changes — cannot use Link Opportunity feature.
- **Missing PDS**: PDS options reported as missing.
- **Sync Issues**: SF ↔ DCT data inconsistencies after updates — expected to escalate.
- **Unclear sales process**: Too much freedom across tools.
- **Error messages**: Difficult to debug without ENG support.

---

## Catfood Environment Active — How to Disable
**Symptom**: Seeing catfood/test environment instead of production.
**Fix**:
1. Open Chrome Extensions → find **Modheader**.
2. Click the extension → small black screen with catfood list.
3. **Uncheck** the checkbox next to the catfood name.
4. Refresh the page → regular production environment restored.

---

## New Merchant — No Primary Services Set Up
**Symptom**: Clicking "Resume" shows standard DCT flow (Bookable/Non-bookable → PDS → Template).
**When this screen shows**: Until Primary Service is added OR until first deal is CW.
**Flow**: At end of flow — timing/trigger currently unclear.

---

## Linking Opp in Wrong Stage
**Scenario 1**: Attempt to link an Opp in a stage other than **Prospecting** → fails.
- DCT only supports linking when Opp is in Prospecting stage.
- Once Opp leaves Prospecting, it cannot be linked to DCT.

## Editing Old Draft Deal
**Scenario 2**: Attempt to edit an old/outdated draft → fails at submission.
- DCT allows the edit but fails on submit.

---

## Merchant Doesn't Have MC Created
**Fix**: Go to SF Account → generate **Merchant Permalink**.

---

## Account is DNR or Outside Local LOB
**Symptom**: "New Campaign" button not visible.
**Fix**: Request DNR lift via the regular process.

---

## PDS Missing / Inactive
**Issue**: PDS options missing or inactive in DCT.
**Known missing examples**: "Axe Throwing", "CoolSculpting", "Injection - Xeomin".
**Status**: PDS list is being updated — missing options will be added.
**Also**: PDS can be changed at the Opp level in SF directly.

---

## "Please Insert SF Opportunity ID" Error
**Fix**: Only SF Opportunity ID works — no other ID format is accepted.

---

## Page Refresh Needed / Short Disturbance
**Symptom**: Error during flow / page not loading correctly.
**Fix**: Refresh the page — usually a short-term Merchant Center disturbance. Should resolve after refresh.

---

## First Draft Started Then Exited — Resume Screen on Reopen
**Symptom**: Reopening DCT shows resume screen after exiting first draft for new merchant.
**Fix**: Click "Resume" OR "Build a new campaign" to re-enter DCT flow.

---

## RBAC Access Missing
**Fix**: Contact **Veronika** to grant RBAC access.
- Note: All new reps should receive RBAC access (currently manual process).

---

## CC Fee Modification in DCT
**Issue**: Cannot modify CC fee inside DCT.
**Fix**: CC fee must be changed in **Salesforce (SF)**.

---

## Changing Deal Payment Method
**Issue**: Cannot change from "pay on redemption" to "pay on view" in DCT.
**Status**: DCT only supports redemption payment — POV support planned for future release.

---

## Viewing Uploaded Pictures for Approvals
**Issue**: Photos uploaded via DCT not visible in SF.
**Current**: Photos only available in DCT draft preview.
**Status**: Feature request to make visible in SF.

---

## Error Message During Campaign Creation (Catfood Modheader)
**Fix**: Disable old catfood modheader (see Catfood section above).

---

## Accessing MC from SF — Login Issue
**Issue**: Reps get errors logging into Merchant Center.
**Fix**: Access MC from the **Account level** in SF, not from Opportunity level.

---

## Editing Margin Splits
**Issue**: "Merchant Margin" box not editable.
**Fix**: Field is informational only — use the **Merchant Gets** field instead.

---

## Editing After Submission for Approval
**Issue**: Cannot edit via DCT after submission.
**Current workaround**: Edits must be made in SF or DW; DCT edits planned for future.

---

## DCT Only Supports US Local Merchants
- DCT is **US only** — not for Toronto/Canada merchants.
- DCT is for **local deals only** — not for Enterprise accounts.

---

## Deal Restructure / Changing Deal Info Post-Submission
**Issue**: Reps unclear on steps to restructure deal or change deal info after submission.
**Current**: Use SF or DW for edits post-submission.

---

## Known Improvements Backlog (DCT)
- Auto-generate content (remove need to click "Inspire me")
- Add Notes to Editorial field
- Disable merchant drafts for editing
- Automated PDS assignment
- Options auto-ordered cheapest first
- Character count displayed per field
- Auto-populate Primary Contact from SF
- Draft preview → open in Unified flow
- Bulk change all options
- Custom Fine Print field should be larger/expandable
- Remove "Build a new AI campaign" button for internal users
- Automate permalink creation or show SF error when MC has no permalink
- Video upload: allow social media link instead of file upload
- Custom codes & Custom checkout sections collapsed by default
- Add SF Opp ID under each Draft campaign

---

## Weekly DCT Support Summary (26–30 May)
| Issue | Resolution |
|-------|-----------|
| Missing PDS options | Being added to PDS list |
| Redemption codes on additional options | Workaround: use Bulk Edit (Jira: DL-4735) |
| DCT access error from SF | Generate Merchant Permalink first |
| Opp in wrong stage | Can only link Opps in Prospecting stage |
| CC fee modification | Must be changed in SF |
| MC access issues | Grant RBAC access (Veronika) |
| Pay on view not available | Only redemption supported; POV coming |
| Photos not in SF | Only in DCT draft preview |
| Error during creation | Disable old catfood modheader |
| PDS change inside DCT | Change at Opp level in SF |
| Editing after submission | Use SF or DW |
| Error changing deal in DCT | Cannot edit submitted Opps in DCT |
| Margin splits not editable | Use "Merchant Gets" field |
