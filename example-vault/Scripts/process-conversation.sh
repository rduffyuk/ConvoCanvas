#!/bin/bash

# ConvoCanvas Conversation Processor
# Usage: ./process-conversation.sh <conversation-file>

set -e

# Configuration
API_BASE="http://localhost:8000"
SCRIPT_DIR="$(dirname "$0")"
VAULT_DIR="$(dirname "$SCRIPT_DIR")"
INPUT_FILE="$1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Validate input
if [ -z "$INPUT_FILE" ] || [ ! -f "$INPUT_FILE" ]; then
    log_error "Usage: $0 <conversation-file>"
    log_error "Example: $0 Input/Conversations/example-chat.md"
    exit 1
fi

# Check if API is running
log_info "Checking ConvoCanvas API..."
if ! curl -s "$API_BASE/" > /dev/null; then
    log_error "ConvoCanvas API not running. Start it with:"
    echo "  cd ../backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000"
    exit 1
fi
log_success "API is running"

# Get filename without path and extension
FILENAME=$(basename "$INPUT_FILE" .md)
OUTPUT_DIR="$VAULT_DIR/Output"

# Create output directories
mkdir -p "$OUTPUT_DIR"/{Conversations,Mindmaps,Content-Ideas}

log_info "Processing conversation: $FILENAME"

# 1. Basic conversation upload
log_info "📤 Uploading for basic analysis..."
BASIC_RESULT=$(curl -s -X POST "$API_BASE/api/conversations/upload" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$INPUT_FILE")

if [ $? -eq 0 ]; then
    echo "$BASIC_RESULT" | jq '.' > "$OUTPUT_DIR/Conversations/${FILENAME}_basic.json"
    log_success "Basic analysis saved to Output/Conversations/${FILENAME}_basic.json"
else
    log_error "Basic analysis failed"
    exit 1
fi

# 2. Enhanced analysis with decision tracking
log_info "🧠 Running enhanced analysis..."
ENHANCED_RESULT=$(curl -s -X POST "$API_BASE/api/v2/conversations/analyze-enhanced" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$INPUT_FILE")

if [ $? -eq 0 ]; then
    # Save full analysis
    echo "$ENHANCED_RESULT" | jq '.' > "$OUTPUT_DIR/Conversations/${FILENAME}_enhanced.json"
    log_success "Enhanced analysis saved to Output/Conversations/${FILENAME}_enhanced.json"

    # Extract mindmap HTML
    if echo "$ENHANCED_RESULT" | jq -e '.decisions.decision_mindmap.html' > /dev/null; then
        echo "$ENHANCED_RESULT" | jq -r '.decisions.decision_mindmap.html' > "$OUTPUT_DIR/Mindmaps/${FILENAME}_mindmap.html"
        log_success "Interactive mindmap saved to Output/Mindmaps/${FILENAME}_mindmap.html"
    fi

    # Extract content ideas
    if echo "$ENHANCED_RESULT" | jq -e '.content_ideas' > /dev/null; then
        echo "$ENHANCED_RESULT" | jq -r '.content_ideas' > "$OUTPUT_DIR/Content-Ideas/${FILENAME}_ideas.json"
        log_success "Content ideas saved to Output/Content-Ideas/${FILENAME}_ideas.json"
    fi

else
    log_error "Enhanced analysis failed"
    exit 1
fi

# 3. Check feature flags
log_info "🎛️  Checking available features..."
FEATURES=$(curl -s "$API_BASE/feature-flags")
echo "$FEATURES" | jq '.' > "$OUTPUT_DIR/feature-flags.json"

# Summary
log_success "Processing complete! 🎉"
echo ""
log_info "Results saved to:"
echo "  📊 Basic analysis: Output/Conversations/${FILENAME}_basic.json"
echo "  🧠 Enhanced analysis: Output/Conversations/${FILENAME}_enhanced.json"
echo "  🗺️  Interactive mindmap: Output/Mindmaps/${FILENAME}_mindmap.html"
echo "  💡 Content ideas: Output/Content-Ideas/${FILENAME}_ideas.json"
echo ""
log_info "To view the mindmap, open the HTML file in your browser:"
echo "  open Output/Mindmaps/${FILENAME}_mindmap.html"
echo ""

# Check for insights
DECISIONS_COUNT=$(echo "$ENHANCED_RESULT" | jq '.decisions.extracted_decisions | length')
log_info "📈 Analysis insights:"
echo "  🎯 Decisions extracted: $DECISIONS_COUNT"

if [ "$DECISIONS_COUNT" -gt 0 ]; then
    echo "  🔍 Decision topics:"
    echo "$ENHANCED_RESULT" | jq -r '.decisions.extracted_decisions[].text' | head -3 | sed 's/^/    - /'
fi

log_warning "Remember to review and integrate these insights into your knowledge base!"