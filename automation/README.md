# ConvoCanvas Automation Suite

**Universal file organization and metadata management for knowledge systems**

## 🎯 What's Included

### **Universal Obsidian Organizer**
- `obsidian-universal-organizer.sh` - Organizes files by date across entire vault
- `obsidian-daily-organizer.sh` - Daily file management automation
- Works with any vault structure, any date pattern

### **Smart Tagging System**
- `obsidian-universal-tagger.py` - Adds YAML frontmatter to all markdown files
- `obsidian-auto-tagger.py` - Legacy tagger for specific patterns
- `obsidian-auto-tagger-organized.py` - Post-organization tagging

### **Metadata Management**
- Content-based categorization (AI-Conversations, Content-Ideas, etc.)
- Date and time stamping
- Smart tag generation based on file paths and content
- Navigation index creation

## 🚀 Quick Start

### **Setup**
```bash
# Copy scripts to your preferred location
cp automation/obsidian-organizer/* ~/scripts/

# Make executable
chmod +x ~/scripts/*.sh

# Install Python dependencies
pip install pyyaml
```

### **Basic Usage**

**Organize all files by date:**
```bash
cd /path/to/your/obsidian-vault
~/scripts/obsidian-universal-organizer.sh
```

**Add metadata to all files:**
```bash
cd /path/to/your/obsidian-vault
python ~/scripts/obsidian-universal-tagger.py
```

**Daily automation (add to crontab):**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/obsidian-daily-organizer.sh
```

## 📁 What Gets Organized

### **Date-Based Structure Created**
```
your-vault/
├── 01-AI-Conversations/
│   ├── 2025-09-September/
│   │   ├── 2025-09-11_Claude-Network-Setup.md
│   │   └── 2025-09-14_AI-Automation-Discussion.md
├── 02-Content-Ideas/
│   ├── 2025-09-September/
│   │   └── 2025-09-14_LinkedIn-Post-Ideas.md
└── [other categories]/
    └── [date-organized files]
```

### **YAML Frontmatter Added**
```yaml
---
date: 2025-09-14
source: Claude Code
category: AI-Conversations
tags: [automation, obsidian, file-organization]
status: completed
priority: high
created: 2025-09-14 21:30:00
---
```

## ⚙️ Configuration

### **Customize Categories**
Edit the Python scripts to modify:
- Category detection patterns
- Tag generation rules
- Date parsing formats
- File naming conventions

### **Folder Structure**
The organizer automatically detects and creates:
- AI conversation files → `01-AI-Conversations/`
- Content ideas → `02-Content-Ideas/`
- Technical docs → `03-Technical-Documentation/`
- And more based on content analysis

## 🛠️ Script Details

### **obsidian-universal-organizer.sh**
- Processes all `.md` files in vault
- Extracts dates from filenames and content
- Creates organized folder structure
- Preserves original files as backup
- Generates navigation indices

### **obsidian-universal-tagger.py**
- Scans all markdown files
- Analyzes content and location
- Adds comprehensive YAML frontmatter
- Smart categorization based on content
- Handles existing frontmatter gracefully

### **obsidian-daily-organizer.sh**
- Lightweight daily maintenance
- Organizes recent files only
- Perfect for cron automation
- Minimal resource usage

## 📊 Performance

**Tested With:**
- ✅ 56 files processed successfully
- ✅ Multiple vault structures supported
- ✅ Preserves file integrity and links
- ✅ Handles special characters and spaces

**Processing Speed:**
- ~100 files/minute on standard hardware
- Intelligent skip of already-organized files
- Progress indicators for large vaults

## 🔧 Customization Examples

### **Add New Category**
```python
# In obsidian-universal-tagger.py
category_patterns = {
    'AI-Conversations': ['claude', 'chatgpt', 'ai-', 'conversation'],
    'Your-Category': ['your-pattern', 'another-pattern'],  # Add this
    # ... existing patterns
}
```

### **Custom Date Formats**
```bash
# In organizer scripts, modify date extraction patterns
DATE_PATTERNS=(
    '\d{4}-\d{2}-\d{2}'          # YYYY-MM-DD
    '\d{2}-\d{2}-\d{4}'          # MM-DD-YYYY (add custom)
    # ... add your patterns
)
```

## 🎯 Use Cases

### **Knowledge Workers**
- Organize years of accumulated notes
- Maintain clean, navigable knowledge base
- Auto-categorize different types of content

### **AI Practitioners**
- Organize AI conversation exports
- Track learning progression over time
- Maintain context across projects

### **Content Creators**
- Organize ideas and drafts by date
- Smart categorization of content types
- Easy access to inspiration archives

## 📋 Best Practices

1. **Backup First**: Always backup your vault before running
2. **Test Small**: Try on a subset of files first
3. **Review Results**: Check organization matches expectations
4. **Customize**: Adapt scripts to your specific needs
5. **Automate**: Set up daily runs for continuous organization

---

**These scripts transformed a chaotic collection of 56 files into a perfectly organized, searchable knowledge base in minutes.**