"""B2B Google Chat Bot — Local Demo (Streamlit).

Simulates the full @b2b_bot flow:
  1. Semantic search over 2-year B2B chat history (ChromaDB)
  2. Semantic search over known issue FAQ / playbook (memory files)
  3. Claude generates a contextual answer, referencing known issues when matched
  4. Auto-detects if a Jira GBR ticket should be created

Run:
    streamlit run demo.py
"""

import json
import os
import re
from pathlib import Path

import chromadb
import numpy as np
import streamlit as st
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "chat_messages"
MEMORY_PATH = "/Users/rohjain/.claude/projects/-Users-rohjain-Documents-workplace-gme-bot/memory"
FAQ_SIMILARITY_THRESHOLD = 0.42

SYSTEM_PROMPT = """\
You are @b2b_bot, an AI assistant embedded in the Groupon B2B team's Google Chat space.

Your responsibilities:
1. Answer merchant-side questions using the historical chat context provided.
2. If "Known Issue Context" is provided and relevant, reference it — start your answer with \
"📋 Known Issue Match:" and guide the user through the specific investigation steps or criteria \
from that context. Be precise about what to check (Salesforce fields, flags, service endpoints, etc.).
3. Detect when the user is reporting a NEW bug or issue that needs a Jira GBR ticket.
4. Extract structured ticket fields (severity, component, steps, account, deal_id, user).

Rules:
- Be concise. Match the tone of a helpful Slack/Chat bot.
- When a known issue matches, tell the user to investigate before escalating and list the exact \
check steps from the playbook.
- Only set create_ticket=true when the user explicitly reports an issue or asks to create one.
- Set known_issue_matched=true when Known Issue Context was relevant to the answer.
- Use context to surface similar past cases and whether they were resolved.
- SOX mode: read-only analysis only. Ticket creation is the only write action.

Respond ONLY with a valid JSON object matching this exact schema:
{
  "answer": "<your response to the user>",
  "create_ticket": <true or false>,
  "known_issue_matched": <true or false>,
  "ticket": {
    "summary": "<one-line issue title>",
    "severity": "<P0|P1|P2|P3>",
    "component": "<component name, e.g. Deal Activation, GBucks, Checkout>",
    "steps_to_reproduce": "<numbered steps or 'N/A'>",
    "account": "<merchant account if mentioned, else null>",
    "deal_id": "<deal ID if mentioned, else null>",
    "affected_user": "<user email if mentioned, else null>",
    "description": "<full issue description for the Jira ticket body>"
  }
}
If create_ticket is false, set ticket to null.\
"""

EXAMPLE_QUERIES = [
    "@b2b_bot merchant account 98765 getting 'deal not available' error since this morning",
    "@b2b_bot merchant from CA says the Add Option button is missing in Campaign Editor",
    "@b2b_bot new campaign button not visible — merchant type is Enterprise",
    "@b2b_bot deal is live but not showing up in Merchant Center",
    "@b2b_bot merchant can't edit campaign, getting 503 error",
    "@b2b_bot please create a P1 ticket: account groupon_test is unable to activate deals, error 500",
]


# ── Cached resources ──────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading embedding model…")
def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource(show_spinner="Connecting to ChromaDB…")
def load_collection() -> tuple[chromadb.Collection | None, int]:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        col = client.get_collection(COLLECTION_NAME)
        return col, col.count()
    except Exception:
        return None, 0


@st.cache_resource(show_spinner="Loading known issues playbook…")
def load_faq_knowledge_base(_model: SentenceTransformer) -> tuple[list[dict], "np.ndarray | None"]:
    """Load FAQ/meeting markdown files, split into sections, embed for semantic search."""
    memory_dir = Path(MEMORY_PATH)
    if not memory_dir.exists():
        return [], None

    sections: list[dict] = []
    for pattern in ("faq_*.md", "meeting_*.md"):
        for filepath in sorted(memory_dir.glob(pattern)):
            raw = filepath.read_text(encoding="utf-8")
            source = filepath.stem.replace("_", " ").title()
            chunks = re.split(r"\n(?=## )", raw)
            for chunk in chunks:
                chunk = chunk.strip()
                if len(chunk) > 80:
                    header_match = re.match(r"^## (.+)", chunk)
                    header = header_match.group(1).strip() if header_match else source
                    sections.append({"source": source, "header": header, "text": chunk})

    if not sections:
        return [], None

    texts = [s["text"][:800] for s in sections]
    emb = _model.encode(texts, show_progress_bar=False).astype(np.float32)
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    emb = emb / np.maximum(norms, 1e-9)
    return sections, emb


# ── Core functions ────────────────────────────────────────────────────────────

def semantic_search(
    query: str, model: SentenceTransformer, collection: chromadb.Collection, n: int
) -> list[dict]:
    embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=n)
    return [
        {
            "text": doc,
            "distance": results["distances"][0][i],
            "metadata": results["metadatas"][0][i],
        }
        for i, doc in enumerate(results["documents"][0])
    ]


def faq_search(
    query: str,
    model: SentenceTransformer,
    sections: list[dict],
    embeddings: "np.ndarray",
    n: int = 3,
) -> list[dict]:
    """Semantic search over FAQ sections; returns top N above similarity threshold."""
    if not sections or embeddings is None:
        return []
    q_emb = model.encode(query).astype(np.float32)
    q_emb = q_emb / max(float(np.linalg.norm(q_emb)), 1e-9)
    scores = embeddings @ q_emb
    top_idx = np.argsort(scores)[::-1][:n]
    return [
        {"section": sections[i], "score": float(scores[i])}
        for i in top_idx
        if scores[i] >= FAQ_SIMILARITY_THRESHOLD
    ]


def call_claude(
    query: str, context: list[dict], faq_hits: list[dict], api_key: str
) -> dict:
    context_parts = []
    for i, hit in enumerate(context, 1):
        similarity = max(0.0, 1.0 - hit["distance"])
        meta = hit["metadata"]
        resolved = "✅ resolved" if meta.get("has_resolution") else "🔴 unresolved"
        snippet = hit["text"][:600].replace("\n", " | ")
        context_parts.append(
            f"[Context {i} — {similarity:.0%} match, {resolved}, {meta.get('message_count', '?')} msgs]\n{snippet}"
        )

    faq_parts = [
        f"[Known Issue — {h['section']['source']} › {h['section']['header']} | {h['score']:.0%} match]\n{h['section']['text'][:700]}"
        for h in faq_hits
    ]

    parts = []
    if context_parts:
        parts.append("Historical B2B chat context:\n\n" + "\n\n".join(context_parts))
    if faq_parts:
        parts.append("Known Issue Context (FAQ / Playbook — investigate these before escalating):\n\n" + "\n\n".join(faq_parts))
    parts.append(f"Current message: {query}")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": "\n\n---\n\n".join(parts)}],
    )
    raw = response.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {"answer": raw, "create_ticket": False, "known_issue_matched": False, "ticket": None}


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="B2B Bot Demo", page_icon="🤖", layout="wide")
st.title("🤖 B2B Google Chat Bot — Local Demo")
st.caption(
    "Simulates @b2b_bot: semantic search over 2-year B2B history + Known Issue Playbook + Claude AI + Jira auto-creation"
)

model = load_embedding_model()
collection, thread_count = load_collection()
faq_sections, faq_embeddings = load_faq_knowledge_base(model)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Config")
    api_key = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Get from console.anthropic.com",
    )
    n_results = st.slider("Conversations to retrieve", min_value=3, max_value=10, value=5)

    st.divider()
    st.subheader("📊 Chat History")
    if collection:
        st.success(f"✅ {thread_count:,} threads loaded")
    else:
        st.error("ChromaDB not found.\nRun `python bulk_ingest.py` first.")

    st.divider()
    st.subheader("📋 Known Issues Playbook")
    if faq_sections:
        st.success(f"✅ {len(faq_sections)} issue sections loaded")
    else:
        st.warning("No FAQ files found.")

    st.divider()
    st.subheader("💡 Example queries")
    for ex in EXAMPLE_QUERIES:
        st.caption(ex)

# ── Main input ────────────────────────────────────────────────────────────────
query = st.text_area(
    "Simulate a @b2b_bot mention:",
    placeholder=EXAMPLE_QUERIES[0],
    height=110,
    key="query_input",
)

ready = bool(query.strip() and api_key and collection)
if not api_key:
    st.info("Enter your Anthropic API key in the sidebar to enable responses.")
if not collection:
    st.warning("Run `python bulk_ingest.py` to load the knowledge base first.")

ask_btn = st.button("🚀 Ask Bot", type="primary", disabled=not ready)

# ── Results ───────────────────────────────────────────────────────────────────
if ask_btn and ready:
    with st.spinner("🔍 Searching historical context…"):
        hits = semantic_search(query, model, collection, n_results)

    with st.spinner("📋 Checking known issues playbook…"):
        faq_hits = faq_search(query, model, faq_sections, faq_embeddings, n=3)

    with st.spinner("🧠 Calling Claude Sonnet 4.6…"):
        result = call_claude(query, hits, faq_hits, api_key)

    st.divider()

    # ── Known issues banner ───────────────────────────────────────────────────
    if faq_hits:
        st.warning(
            f"📋 **{len(faq_hits)} Known Issue(s) Matched** — please investigate the following before escalating:"
        )
        for fh in faq_hits:
            sec = fh["section"]
            with st.expander(
                f"📌 {sec['source']} › {sec['header']}  —  {fh['score']:.0%} match",
                expanded=True,
            ):
                st.markdown(sec["text"])
        st.divider()

    left, right = st.columns([3, 2])

    with left:
        st.subheader("🤖 Bot Response")
        answer = result.get("answer", "_No response_")
        st.markdown(answer)

        if result.get("create_ticket"):
            ticket = result.get("ticket") or {}
            st.subheader("🎫 Jira GBR Ticket Preview")
            severity_colors = {"P0": "🔴", "P1": "🟠", "P2": "🟡", "P3": "🟢"}
            sev = ticket.get("severity", "P2")
            st.markdown(
                f"**{severity_colors.get(sev, '⚪')} {sev} — {ticket.get('summary', 'Untitled')}**"
            )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Component:** {ticket.get('component', 'N/A')}")
                st.markdown(f"**Account:** {ticket.get('account') or 'N/A'}")
                st.markdown(f"**Deal ID:** {ticket.get('deal_id') or 'N/A'}")
            with col2:
                st.markdown(f"**Affected user:** {ticket.get('affected_user') or 'N/A'}")
                st.markdown(f"**Steps:** {ticket.get('steps_to_reproduce', 'N/A')}")

            with st.expander("Full ticket JSON"):
                st.code(json.dumps(ticket, indent=2), language="json")

            st.info("ℹ️ In production, jira-service would POST this to Jira GBR automatically.")
        else:
            st.caption("_No ticket needed for this query._")

    with right:
        st.subheader(f"📚 Top {len(hits)} Similar Past Conversations")
        for i, hit in enumerate(hits, 1):
            meta = hit["metadata"]
            similarity = max(0.0, 1.0 - hit["distance"])
            resolved = "✅ Resolved" if meta.get("has_resolution") else "🔴 Unresolved"
            label = f"#{i} — {similarity:.0%} similar · {resolved}"
            with st.expander(label):
                st.caption(
                    f"{meta.get('message_count', '?')} messages · "
                    f"Last active: {str(meta.get('last_date', ''))[:10]}"
                )
                st.text(hit["text"][:500] + ("…" if len(hit["text"]) > 500 else ""))
