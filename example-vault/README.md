# ConvoCanvas Example Vault

This example demonstrates how to integrate ConvoCanvas with Obsidian (or any knowledge management system) for automated conversation processing.

## 🏗️ Structure

```
example-vault/
├── Input/                    # Raw conversation files
│   └── Conversations/        # Place exported AI conversations here
├── Output/                   # Processed results
│   ├── Conversations/        # Analyzed conversations with metadata
│   ├── Mindmaps/            # Interactive decision flow visualizations
│   └── Content-Ideas/       # Generated content suggestions
├── Scripts/                 # Automation scripts
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Start ConvoCanvas API
```bash
cd ../backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Process a Conversation
```bash
# Run the example processing script
./Scripts/process-conversation.sh Input/Conversations/example-chat.md
```

### 3. View Results
- **Analyzed conversation**: `Output/Conversations/`
- **Interactive mindmap**: `Output/Mindmaps/` (open .html files in browser)
- **Content ideas**: `Output/Content-Ideas/`

## 🔄 Workflow

1. **Export** conversations using SaveMyPhind browser extension
2. **Place** files in `Input/Conversations/`
3. **Process** using ConvoCanvas API (manual or automated)
4. **Review** generated insights in `Output/` folders
5. **Integrate** insights into your knowledge management workflow

## 🛠️ Customization

This example uses a simple file-based workflow. You can adapt it for:
- **Obsidian**: Use as vault root or integrate with existing vault
- **Notion**: Modify scripts to upload to Notion via API
- **Logseq**: Adapt for Logseq's file structure
- **Custom systems**: Use the core API with your preferred tools

## 🎯 Benefits

- **Automated decision tracking** from AI conversations
- **Visual mindmaps** showing decision relationships
- **Content generation** for social media and blogs
- **Technical domain classification** for better organization
- **Sentiment analysis** to understand decision-making patterns

---

*This example demonstrates ConvoCanvas capabilities without requiring Obsidian installation. The core API remains independent and can integrate with any system.*