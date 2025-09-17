# Obsidian Integration Guide

This guide shows how to integrate ConvoCanvas with Obsidian while keeping the core API independent.

## 🎯 Design Philosophy

- **Core Independence**: ConvoCanvas API works without Obsidian
- **Frontend Flexibility**: Obsidian is just one possible frontend
- **Performance**: Processing happens via API, not Obsidian plugins
- **Portability**: Easy to switch to other knowledge management systems

## 🔄 Integration Approaches

### Option 1: File-Based Workflow (Recommended)
Use this example vault structure as your Obsidian vault or integrate it into your existing vault.

```bash
# Process conversation and save to Obsidian vault
./Scripts/process-conversation.sh Input/Conversations/example-chat.md

# Results appear in Output/ folders, ready for Obsidian linking
```

### Option 2: Automated Processing
Set up automated processing when new conversations are added:

```bash
# Watch for new conversations (requires inotify-tools)
#!/bin/bash
inotifywait -m Input/Conversations/ -e create -e moved_to |
while read path action file; do
    if [[ "$file" =~ .*\.md$ ]]; then
        echo "Processing new conversation: $file"
        ./Scripts/process-conversation.sh "$path$file"
    fi
done
```

### Option 3: Custom Obsidian Commands
Create custom Obsidian commands that call the ConvoCanvas API:

1. Install the "Shell Commands" community plugin
2. Add custom commands that run the processing script
3. Bind to hotkeys for quick processing

## 📁 Obsidian Vault Structure

```
your-obsidian-vault/
├── 00-Inbox/                    # New conversations go here
├── 01-AI-Conversations/         # Processed conversations
│   ├── Raw/                     # Original conversation files
│   └── Analyzed/                # ConvoCanvas analysis results
├── 02-Decision-Maps/            # Interactive mindmaps
├── 03-Content-Ideas/            # Generated content suggestions
├── Scripts/                     # Processing automation
└── Templates/                   # Obsidian templates for consistency
```

## 🔗 Linking and Navigation

### Automatic Backlinking
ConvoCanvas outputs include metadata perfect for Obsidian linking:

```markdown
# DevOps Pipeline Discussion - Analysis

**Source**: [[example-chat]]
**Decisions**: 6 extracted
**Domains**: DevOps, CI/CD, Kubernetes
**Sentiment**: Positive (0.72)

## Key Decisions
- [[GitHub Actions vs Jenkins]]
- [[Secret Management Strategy]]
- [[Database Migration Approach]]

## Generated Content
- [[LinkedIn Post - CI/CD Best Practices]]
- [[Blog Idea - Microservices Database Evolution]]
```

### Template Integration
Create Obsidian templates that include ConvoCanvas metadata fields:

```yaml
---
conversation_source: "{{conversation_file}}"
analysis_date: "{{date}}"
decision_count: "{{decision_count}}"
primary_domain: "{{primary_domain}}"
sentiment_score: "{{sentiment}}"
tags: ["ai-conversation", "{{domain}}", "decision-tracking"]
---
```

## 🚀 Workflow Examples

### Daily Processing Routine
1. Export conversations using SaveMyPhind
2. Drop files in `00-Inbox/`
3. Run processing script or use Obsidian command
4. Review results and create manual links
5. File processed conversations in appropriate folders

### Project-Based Organization
- Process project-related conversations together
- Create project overview notes linking to related decisions
- Use Obsidian's graph view to visualize decision relationships

### Content Creation Pipeline
1. ConvoCanvas extracts content ideas from conversations
2. Review generated suggestions in Obsidian
3. Develop ideas into full posts/articles
4. Track which conversations led to published content

## 🛠️ Advanced Integrations

### Dataview Queries
Use Obsidian's Dataview plugin to query ConvoCanvas metadata:

````markdown
```dataview
TABLE decision_count, sentiment_score, primary_domain
FROM "01-AI-Conversations"
WHERE decision_count > 3
SORT analysis_date DESC
```
````

### Graph Analysis
- Obsidian's graph view shows relationships between decisions
- Tag conversations by domain for filtered graph views
- Track evolution of thinking on specific topics

### Templater Automation
Use Templater plugin to automate note creation from ConvoCanvas outputs:

```javascript
// Auto-create decision tracking notes
const analysis = await tp.system.prompt("Paste ConvoCanvas analysis JSON");
const decisions = JSON.parse(analysis).decisions.extracted_decisions;

decisions.forEach(decision => {
    tp.file.create_new(`${decision.id} - ${decision.text}`,
                       `02-Decision-Maps/${decision.id}`);
});
```

## 💡 Benefits of This Approach

- **Flexibility**: Not locked into Obsidian-specific solutions
- **Performance**: Heavy processing happens outside Obsidian
- **Reliability**: Core functionality works even if Obsidian issues occur
- **Portability**: Easy migration to other knowledge management systems
- **Integration**: Works with existing Obsidian workflows and plugins

---

This approach gives you the best of both worlds: powerful ConvoCanvas analysis with Obsidian's excellent knowledge management and linking capabilities.