# GME Bot — B2B Google Chat AI Bot (Local Demo)

A local demo of the `@b2b_bot` AI assistant for the Groupon B2B/Merchant team.

The bot responds to `@b2b_bot` mentions in Google Chat, searches 2 years of B2B chat history for similar past issues, generates AI-powered answers using Claude, and auto-creates Jira GBR tickets when an issue is detected.

---

## Demo Flow

```
User types @b2b_bot message
        ↓
Semantic search over 2,826 threads (ChromaDB + sentence-transformers)
        ↓
Claude Sonnet 4.6 generates answer using historical context
        ↓
If issue detected → Jira GBR ticket preview shown
```

---

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) — `pip install uv`
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com/settings/keys)
- `chat_export.json` — exported from the B2B Google Chat space

---

## Setup & Run

### One-command setup (first time only)

```bash
# 1. Clone the repo
git clone https://github.com/rohjain54/gme_bot.git
cd gme_bot

# 2. Place chat_export.json in this directory (or two levels up)

# 3. Run setup (installs deps + ingests chat history into ChromaDB)
bash setup.sh
```

### After first-time setup

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
uv run streamlit run demo.py
```

Open **http://localhost:8501** in your browser.

---

## Scripts

| Script | Purpose |
|---|---|
| `bulk_ingest.py` | One-time ingestion of `chat_export.json` → ChromaDB |
| `demo.py` | Streamlit web UI |
| `setup.sh` | Installs deps + runs ingestion + launches demo |

---

## Example Queries

```
@b2b_bot merchant account 98765 getting 'deal not available' error since this morning

@b2b_bot how do we handle GBucks not applying at checkout?

@b2b_bot deal ID 123456 is not showing as cartable — what are the usual causes?

@b2b_bot please create a P1 ticket: account groupon_test unable to activate deals, error 500
```

---

## Architecture (Production)

```
Google Chat ──→ webhook-service (FastAPI :8080)
                      ↓
              rag-engine (ChromaDB + Claude :8081)
                      ↓
              jira-service (Jira REST API :8082)
```

> This demo collapses all three services into a single Streamlit app for local development.

---

## Security Notes

- Never commit `chat_export.json`, `.env`, or API keys
- In production, all secrets go into GCP Secret Manager
- Bot operates in read-only mode (SOX compliance) — ticket creation is the only write action
