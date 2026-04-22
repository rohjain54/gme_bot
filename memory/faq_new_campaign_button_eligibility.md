---
name: New Campaign Button Eligibility - Business Rules & Debugging
description: Business rules for New Campaign button (Metro eligibility) visibility for NA and EMEA, feature flags, known exclusions, debug endpoints, and CB eligibility criteria updates.
type: reference
originSessionId: d71ba1b5-5af2-4e03-b4c9-f4b488c38d92
---
## Business Rules for New Campaign Button Visibility (Metro Eligibility)

### NA (North America)
- Merchant record must be available in **SF and M3 services**
- Merchant type: **live / local / travel**
- Merchants must **not** have any DNR reason

### EMEA
- Merchant record must be available in **SF and M3 services**
- Merchant type: **local only**
- Merchants must **not** have any DNR reason
- `Category(v3)` must **not** be **Travel**

---

## CB Eligibility Criteria (Updated / Target State)

### NA (Updated)
- Merchant record available in SF and M3 services
- Type: **local only**
- No DNR reason
- `Category(v3)` must **not** be **Travel** or **Goods**

### EMEA (Updated)
- Merchant record available in SF and M3 services
- Type: **local only**
- No DNR reason
- `Category(v3)` must **not** be **Travel** or **Goods**

### Special Cases
- **IT (Italy) and ES (Spain)**: Additional criteria on **account ownership** — this must be **kept as-is** when updating INTL logic (do not wipe it).

---

## Countries Without Self-Service Support (New Campaign Button Hidden)
- **IE** (Ireland)
- **BE** (Belgium)
- **NL** (Netherlands)

---

## Feature Flags (Debugging)

| Flag | Notes |
|------|-------|
| `__appContext__.merchant.features.features.metroFlow` | Primary flag to check first |
| `ENABLE_METRO` | Set to a fixed value — does not affect conditions currently |
| `ALLOW_MD_MS_ACCOUNT` | Set to a fixed value — does not affect conditions currently |

### How to Use the metroFlow Flag:
- Value = **self-service** + New Campaign button **not visible** → **frontend issue**
- Value = **none** → **start debugging from backend**

---

## Cache Note (Rainbow Service)
SF data is retrieved from **Rainbow service** (SF cache).
- Cache may not be updated → can affect eligibility.
- To verify: hit the Rainbow endpoint directly (see below).

---

## Debug Endpoints (Local Proxy Required)

### Dashboard Endpoint (Draft Service)
```bash
curl --location 'http://localhost:9000/draft/merchants/{merchantUUID}/dashboard' \
--header 'x-api-key: metro-stg'
```

### M3 Service Endpoint
```bash
curl --location 'http://m3-merchant-service.production.service/merchantservice/v2.1/merchants/{merchantUUID}?client_id={from secret repo}'
```

### Rainbow Service Endpoint (SF Cache)
```bash
curl --location 'http://salesforce-cache.production.service/v0/Account/{AccountId18}' \
--header 'Authorization: Basic {from secret repo}'
```

> Note: All curls require the app running locally with **local proxy enabled**.
