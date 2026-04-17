"""B2B Google Chat Bot — Local Demo (Streamlit).

Simulates the full @b2b_bot flow:
  1. Semantic search over 2-year B2B chat history (ChromaDB)
  2. Claude generates a contextual answer
  3. Auto-detects if a Jira GBR ticket should be created

Run:
    streamlit run demo.py
"""

import json
import os
import re

import chromadb
import streamlit as st
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "chat_messages"

SYSTEM_PROMPT = """\
You are @b2b_bot, an AI assistant embedded in the Groupon B2B team's Google Chat space.

Your responsibilities:
1. Answer merchant-side questions using the historical chat context provided.
2. Detect when the user is reporting a NEW bug or issue that needs a Jira GBR ticket.
3. Extract structured ticket fields (severity, component, steps, account, deal_id, user).

Rules:
- Be concise. Match the tone of a helpful Slack/Chat bot.
- Only set create_ticket=true when the user explicitly reports an issue or asks to create one.
- Use context to surface similar past cases and whether they were resolved.
- SOX mode: read-only analysis only. Ticket creation is the only write action.

Respond ONLY with a valid JSON object matching this exact schema:
{
  "answer": "<your response to the user>",
  "create_ticket": <true or false>,
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
    "@b2b_bot how do we handle GBucks not applying at checkout for a merchant?",
    "@b2b_bot deal ID 123456 is not showing as cartable — what are the usual causes?",
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


# ── Core functions ────────────────────────────────────────────────────────────

def semantic_search(query: str, model: SentenceTransformer, collection: chromadb.Collection, n: int) -> list[dict]:
    embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=n)
    hits = []
    for i, doc in enumerate(results["documents"][0]):
        hits.append({
            "text": doc,
            "distance": results["distances"][0][i],
            "metadata": results["metadatas"][0][i],
        })
    return hits


def call_claude(query: str, context: list[dict], api_key: str) -> dict:
    context_parts = []
    for i, hit in enumerate(context, 1):
        similarity = max(0.0, 1.0 - hit["distance"])
        meta = hit["metadata"]
        resolved = "✅ resolved" if meta.get("has_resolution") else "🔴 unresolved"
        snippet = hit["text"][:600].replace("\n", " | ")
        context_parts.append(
            f"[Context {i} — {similarity:.0%} match, {resolved}, {meta.get('message_count', '?')} msgs]\n{snippet}"
        )

    user_message = (
        "Historical B2B chat context:\n\n"
        + "\n\n".join(context_parts)
        + f"\n\n---\n\nCurrent message: {query}"
    )

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    raw = response.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {"answer": raw, "create_ticket": False, "ticket": None}


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="B2B Bot Demo", page_icon="🤖", layout="wide")

st.title("🤖 B2B Google Chat Bot — Local Demo")
st.caption("Simulates @b2b_bot: semantic search over 2-year B2B history + Claude AI + Jira ticket auto-creation")

model = load_embedding_model()
collection, thread_count = load_collection()

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
    st.subheader("📊 Knowledge Base")
    if collection:
        st.success(f"✅ {thread_count:,} threads loaded")
    else:
        st.error("ChromaDB not found.\nRun `python bulk_ingest.py` first.")

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

    with st.spinner("🧠 Calling Claude Sonnet 4.6…"):
        result = call_claude(query, hits, api_key)

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
