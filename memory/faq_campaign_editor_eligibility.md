---
name: Campaign Editor (CE) Eligibility - Merchant Facing
description: Campaign Editor eligibility criteria, ineligibility conditions, G1/G2 differences, approval requirements, and margin logic. Use when CE access or editing questions arise.
type: reference
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## Who Has Campaign Editor Access?
**Local Merchants — Both US and INTL**

## When Can Merchants Edit?
- When campaign is **scheduled**
- When campaign is **live**

---

## Ineligibility Conditions (CE Unavailable)

| # | Situation | Description | How to Check |
|---|-----------|-------------|--------------|
| 1 | PDS not eligible for Self Service | Some PDSs are not suited for Self Service | Check NAM PDS list / CB Database; refer INTL doc |
| 2 | Tiered Offering | Campaign is Offer, Deal, or Mixed → limited access | Salesforce → Opportunity level |
| 3 | Account marked DNR | Risk flag preventing merchant from editing | SF Account → non-empty `DNR_Reason__c` field |
| 4 | Account is Enterprise or National | CE supports local merchants only | SF → Account level → "Type" field |
| 5 | MAMD (MultiAccount Multi Deal) | Blocked in CE (edit not available on Campaign List page) | CE Campaign Editor / Campaign List page |
| 6 | Changes Pending Review | All systems incl. CE blocked until approved/rejected | CE Campaign List → shows 'Pending Changes' (CE Database) |
| 7 | Payment Terms are Continuous | Only Pay on Redemption is eligible | SF → `Payment_Terms__c` (Reading Rainbow) |
| 8 | GLive | Not filtered on Opportunity record type | PDS level check |
| 9 | Unsupported country | CE supports: US, CA, AU, GB, PL, DE, FR, IT, ES, NL, BE, UAE (Add option NOT available in UAE) | — |
| 10 | Product inventory service ID is VIS | `inventoryServiceId: "vis"` | Product level → check in dmapiv2 |

## Add Option — Additional Ineligibility (CE Flow)
- GLive deal in any country → **false**
- Deal with "Both" offer type → **false**
- ILS deal in France → **false** (ILS only allowed in US/CA)
- Deal with no inventory products → **false**
- Deal with redemption codes (regular merchants) → **false**
- Bookable deal → **false**

---

## G1 vs G2 Campaign Differences

| Feature | G2 Campaigns (margins PDS-specific) | G1 Campaigns (current state) |
|---------|--------------------------------------|-------------------------------|
| Pause/Unpause Deal | Editable | Editable |
| Photos (add, exchange, crop) | Editable | Editable |
| Add Option | Editable | **Not editable** |
| Update Highlights | Editable | Editable |
| Update Description | Editable | Editable |
| Edit Price/Discount | Editable (NAM only) | **Not editable** |
| Monthly Cap | Editable (replenishes each month) | Editable |
| Total Cap | **Not editable** | **Not editable** |
| Change Option Title | Not editable (auto-adjusted on option changes) | Not editable (auto-adjusted) |
| Fine Print (check/uncheck clauses) | Editable (NAM only) | Editable (NAM only) |
| Enable Redemption Location | Editable | Editable |
| Modify Start Date | Editable when scheduled | Editable if scheduled; **not editable if live** |
| Modify End Date | Editable | **Fixed — cannot be edited in CE** |

---

## Approvals Required

| Deal Attribute | Region | Non-MD/MC Account | MD/MC Account |
|----------------|--------|-------------------|---------------|
| Pause Deal | Global | Auto-approved | Account Owner Only |
| Unpause Deal | Global | Auto-approved | Account Owner Only |
| Update Deal Description | Global | MO Agent | MO Agent |
| Update Deal Highlights | Global | MO Agent | MO Agent |
| Image (add, exchange, crop) | Global | MO Agent | MO Agent |
| Add Deal Option | Global (excl. UAE) | MO Agent | Account Owner Only |
| Inactivate Deal Option* | Global | Auto-approved | Account Owner Only (as of Jul 2023) |
| Activate Deal Option | Global | Auto-approved | Account Owner Only |
| Option Reordering | Global | Auto-approved | Auto-approved |
| Change Price/Discount | NAM | MO Agent | Account Owner Only |
| Fine Print (check/uncheck) | NAM | MO Agent | Account Owner Only |
| Enable Redemption Location | Global | Auto-approved | Auto-approved |
| Increase Monthly Cap | Global | Auto-approved | Auto-approved |
| Decrease Monthly Cap | Global | Auto-approved | Auto-approved |
| Adjust Campaign Start Date (Deal Strength = "A sure thing" only) | Global | Auto-approved | Auto-approved |
| Adjust Campaign End Date | Global | MO Agent | Account Owner Only |

*At least 1 active option must remain.

### How to Reassign (MD Required case):
1. Add in submitter comments: *"all edits except MD required are good for approval"*
2. Change case Owner to the Account Owner → hit Save.

---

## Margin Logic

**New option added by merchant:**
CE fetches the **maximum** of the maximum among all options of the given deal (global logic, updated Oct 2023).

**Merchant edits regular price or discount:**
No change in Groupon Margin %. The margin % before the edit continues to apply to that option.
