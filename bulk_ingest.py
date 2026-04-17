"""One-time ingestion of chat_export.json into local ChromaDB.

Run once before starting the demo:
    python bulk_ingest.py

Set CHAT_EXPORT_PATH env var if chat_export.json is not auto-detected.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "chat_messages"
BATCH_SIZE = 100
MAX_TEXT_LENGTH = 2000  # truncate long threads before embedding

RESOLUTION_KEYWORDS = [
    "fixed", "resolved", "solution", "workaround", "deployed",
    "rolled back", "works now", "thank you", "closing", "closed",
    "verified", "confirmed working",
]


def find_chat_export() -> str:
    candidates = [
        os.getenv("CHAT_EXPORT_PATH", ""),
        "./chat_export.json",
        "../../chat_export.json",
        "../../../chat_export.json",
        "/Users/rohjain/Documents/workplace/claude-hub/chat_export.json",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    return ""


def has_resolution(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in RESOLUTION_KEYWORDS)


def safe_id(raw_id: str) -> str:
    """Return a ChromaDB-safe ID (non-empty, ≤64 chars)."""
    if not raw_id:
        return hashlib.md5(raw_id.encode()).hexdigest()
    return hashlib.md5(raw_id.encode()).hexdigest()


def group_by_thread(messages: list[dict]) -> dict[str, list[dict]]:
    threads: dict[str, list[dict]] = {}
    for msg in messages:
        # Use thread name if present, else fall back to message name
        thread_key = msg.get("thread") or msg.get("message_id") or "unknown"
        threads.setdefault(thread_key, []).append(msg)
    for thread_id in threads:
        threads[thread_id].sort(key=lambda m: m.get("created_at", ""))
    return threads


def build_document(thread_id: str, messages: list[dict]) -> dict | None:
    lines = []
    for msg in messages:
        text = (msg.get("text") or "").strip()
        if text:
            sender = msg.get("sender", "Unknown")
            lines.append(f"{sender}: {text}")

    if not lines:
        return None

    combined = "\n".join(lines)
    first, last = messages[0], messages[-1]

    return {
        "id": safe_id(thread_id),
        "text": combined[:MAX_TEXT_LENGTH],
        "metadata": {
            "thread_id": thread_id[:200],
            "message_count": len(messages),
            "first_date": first.get("created_at", ""),
            "last_date": last.get("created_at", ""),
            "has_resolution": has_resolution(combined),
            "unique_senders": len({m.get("sender_email", "") for m in messages}),
        },
    }


def main() -> None:
    export_path = find_chat_export()
    if not export_path:
        print("❌  chat_export.json not found.")
        print("    Set CHAT_EXPORT_PATH env var or copy the file here.")
        sys.exit(1)

    print(f"📂  Loading messages from {export_path}...")
    with open(export_path) as f:
        raw_messages = json.load(f)
    print(f"    {len(raw_messages):,} messages loaded")

    threads = group_by_thread(raw_messages)
    print(f"    {len(threads):,} threads found")

    docs = [d for tid, msgs in threads.items() if (d := build_document(tid, msgs))]
    print(f"    {len(docs):,} non-empty threads to ingest")

    print("\n🤖  Loading embedding model (may take ~30s on first run)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("    Cleared existing collection")
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)

    print(f"\n⏳  Ingesting in batches of {BATCH_SIZE}...")
    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i : i + BATCH_SIZE]
        ids = [d["id"] for d in batch]
        texts = [d["text"] for d in batch]
        metadatas = [d["metadata"] for d in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        done = min(i + BATCH_SIZE, len(docs))
        print(f"    {done}/{len(docs)} threads ingested...", end="\r")

    print(f"\n\n✅  Done! {len(docs):,} threads stored in ChromaDB at {CHROMA_PATH}/")
    print("    Now run: streamlit run demo.py")


if __name__ == "__main__":
    main()
