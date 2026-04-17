#!/usr/bin/env bash
# B2B Bot Demo — one-time setup + ingestion
# Usage: bash setup.sh

set -e

echo "=== B2B Bot Demo Setup ==="
echo ""

# Step 1: Install dependencies
echo "Step 1/3: Installing Python dependencies..."
uv venv .venv --quiet 2>/dev/null || true
uv pip install -r requirements.txt --quiet
echo "  ✅ Dependencies installed"
echo ""

# Step 2: Find chat_export.json
EXPORT_PATH=""
for candidate in \
    "./chat_export.json" \
    "../../chat_export.json" \
    "/Users/rohjain/Documents/workplace/claude-hub/chat_export.json"; do
    if [ -f "$candidate" ]; then
        EXPORT_PATH="$candidate"
        break
    fi
done

if [ -z "$EXPORT_PATH" ]; then
    echo "❌  chat_export.json not found."
    echo "    Copy it to this directory or set CHAT_EXPORT_PATH and re-run."
    exit 1
fi

echo "Step 2/3: Ingesting chat history from $EXPORT_PATH..."
CHAT_EXPORT_PATH="$EXPORT_PATH" uv run python bulk_ingest.py
echo ""

# Step 3: Launch demo
echo "Step 3/3: Launching Streamlit demo..."
echo ""
echo "  Open http://localhost:8501 in your browser."
echo "  Add your Anthropic API key in the sidebar."
echo ""
uv run streamlit run demo.py
