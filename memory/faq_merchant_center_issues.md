---
name: Merchant Center FAQ - Common Issues & Resolutions
description: FAQ covering common Merchant Center issues: campaign visibility, editing, login, reviews, vouchers, 2FA, contacts, and more. Use when any MC-related support question comes up.
type: reference
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## 1. "New Campaign" Option Not Visible
**Issue:** Merchant cannot create a new campaign — button not visible.
**Reason:** Merchant type must be 'Local'. Check `categoryV3` in Salesforce.
- Exclusion applies based on: Type field AND Category field (excluding Travel and Goods).
- DNR'd accounts also will not see the "New Campaign" button.
**Confirm:** Check Salesforce Account → categoryV3 field.

---

## 2. Self-Service Deal — "Edit" Option Not Available for Campaign
**Issue:** Merchant wants to edit a campaign but "Edit" option is missing.
**Reason:** Merchant type must be 'Local'. Category (v3) in SF should not be Travel.
**Additional:** Only the account owner can edit the deal.
**Still an Issue?** Reach out to @jarvis @draft-service.

---

## 3. "Edit" Button Greyed Out on Live Deal
**Issue:** Edit button visible but greyed out on a live deal.
**Reason:** Live deals cannot be edited directly — create a new option instead.
**Note:** DCT deals — only account owners can make edits via internal tools.
**Still an Issue?** Reach out to @jarvis @draft-service.

---

## 4. Merchant Reviews Visible in Merchant Center But Not on Deal Page
**Issue:** Reviews show in Merchant Center but missing on consumer-facing deal page.
**Reason:** Consumer-side review handling differs from Merchant Center.
**Next Step:** Contact Consumer Facing team via @jarvis @core-apps.

---

## 5. Merchant Unable to Disable 2-Factor Authentication
**Solution:** Refer to internal doc: 2-Factor Authentication Wiki (Confluence).

---

## 6. Merchant Cannot Log In — No Permalink Found
**Issue:** Merchant cannot log in; no Merchant Permalink associated.
**Next Step:** Contact engineering team for support.

---

## 7. Voucher Redemption Fails When Logged In as Internal User
**Issue:** Merchant cannot redeem a voucher when logged in as internal user.
**Reason:** Voucher redemption is disabled for internal users — expected behavior.

---

## 8. MDM Edits Not Reflecting
**Issue:** Merchant edited deal through MDM but changes not reflecting.
**Resolution:** Reach out to @jarvis @draft-service.

---

## 9. Changes Under Review but Already Approved — Merchant Cannot Edit
**Issue:** "Changes under review" shown even though changes were approved. Edits possible in Deal Estate but not from merchant side.
**Resolution:** Reach out to @jarvis @draft-service.

---

## 10. Merchant Has 20+ Reviews But Only 3 Visible on Deal Page
**Issue:** Reviews exist but only a few are displayed.
**Resolution:** Reach out to @jarvis @ugc.

---

## 12. Multiple Reviews Exist But Only 2 Visible in Merchant Center
**Issue:** UGC moderator confirms 96 reviews but only 2 visible in MC.
**Resolution:** Reach out to @jarvis @ugc.

---

## 13. Can Expired Customer Reviews Be "Revived"?
**Issue:** Reviews expired in MC — can they be made visible again on deal page?
**Resolution:** Reach out to @jarvis @ugc.
**Review Display Policy (by deal type/region):**
- EMEA_GOODS: 12 months
- NA_GOODS: 18 months
- EMEA_LOCAL: 18 months
- NA_LOCAL: All time
Reviews outside these windows will not be displayed per UGC guidelines.

---

## 14. Old Draft Appears When Merchant Tries to Create New Campaign
**Issue:** Merchant cannot create new campaign — old draft appears instead.
**Resolution:** Reach out to @jarvis @draft-service.

---

## 15. Approved Edits Not Reflecting in Deal
**Issue:** Edits approved but not reflecting even after 3+ attempts.
**Resolution:** Reach out to @jarvis @draft-service.

---

## 16. Merchant Cannot Log In Due to 2FA
**Issue:** Merchant blocked by 2-factor authentication.
**Resolution Steps (Internal User):**
1. Log in as Internal User: `https://www.groupon.com/merchant/center/internal=true`
2. Use merchant permalink to log in as internal user (Okta access required).
3. Navigate to Admin screen → Click "Send Recovery Key".
4. Email with recovery key is sent to merchant.
**Merchant Recovery Steps:**
1. Click "Start Recovery Process" from email.
2. Enter email ID + password → Login.
3. Click "Groupon Recovery Key".
4. Enter the Recovery Key from the email.
5. Click Submit → Merchant can now log in (2FA disabled after recovery key login).
**Reference:** https://groupondev.atlassian.net/wiki/spaces/MX/pages/81652154481/2+factor+authentication+in+Merchant+center

---

## 17. Cannot Delete Primary Contact / Change Primary Contact
**Issue:** Internal user cannot delete primary contact to promote secondary contact.
**Reason:** Internal users do not have permission to delete contacts.
**Solution:** Must be logged in with merchant credentials to perform this action.

---

## 18. Merchant Center Internal Login Access Request
**Solution:** Raise request via Helpdesk:
https://groupondev.atlassian.net/servicedesk/customer/portal/111/group/188/create/2153

---

## 19. DNR Account — New Campaign Button Not Visible
**Issue:** Merchant cannot create new campaign even after completing all checklists; campaign page not loading.
**Reason:** Account is DNR'd — "New Campaign" button is not visible on DNR accounts.

---

## 20. Difference Between Admin and Staff in Merchant Center
**Reference:** https://groupondev.atlassian.net/wiki/spaces/MX/pages/82323505386/Merchant+Center+-+Admin+vs+Staff

---

## 21. How to Update User Names in Merchant Center (Admin and Staff)
**Reference:** https://groupondev.atlassian.net/wiki/spaces/MX/pages/82550980692/How+to+update+First+and+last+name+for+Admin+and+staff+user+in+Merchant+Center

---

## 22. Merchant Cannot See Voucher Scanning Screen in App
**Issue:** Voucher scanning screen not visible in Groupon Merchant App.
**Reason:** Camera permission not enabled on device.
**For Android:**
1. Settings → Privacy → Permission Manager → Camera → Groupon Merchant App → Allow only while using the app.
2. Force close and reopen app.
**For iPhone (iOS):**
1. Settings → Privacy & Security → Camera → Groupon Merchant App → Toggle ON.
2. Force close and reopen app.
**Reference:** https://groupondev.atlassian.net/wiki/spaces/MX/pages/82571952167/Redeem+Voucher+-+Allow+Camera+for+Merchant+Mobile+App
