# ConvoCanvas

> **🚀 Alpha Release - Core Features Working & Tested 🚀**

> **Bridge the context gap between AI conversations and long-term projects.**

ConvoCanvas transforms exported AI conversations into actionable content ideas and context summaries, solving the memory limitation problem that technical professionals face when working on complex, multi-session projects.

## ⚠️ Development Status

**Alpha Release - Core Features Working!** The MVP is functional with conversation analysis, decision tracking, and visualization capabilities tested and working. Still evolving with regular improvements. Suitable for experimentation and early adoption.

## 🧠 The Problem

As a network engineer transitioning into DevOps and automation, I've broken my Linux installs more times than I can count building local LLMs and complex infrastructure. But the real wall I hit wasn't technical—it was **context window limitations**.

AI services like Claude and Gemini forget everything between sessions. For any long-term technical project, their memory is too short. I found myself constantly re-explaining complex setups, architectural decisions, and troubleshooting context.

## 💡 The Solution

ConvoCanvas is my external memory for AI conversations. It processes exported chats and generates:

- **Context summaries** to re-prime the next AI session
- **Technical decision logs** from conversation history
- **Content ideas** (LinkedIn posts, blog topics) extracted from learning processes
- **Conversation themes** to track project evolution

**Real Impact**: Recently used ConvoCanvas to maintain context across a 3-day MPLS automation pipeline troubleshooting session—something impossible with standard AI chat limits.

## 🚀 **AI-Powered Productivity System** (v0.2.0-alpha)

ConvoCanvas is evolving into a comprehensive productivity engine combining AI conversation processing with knowledge management:

### **✅ Core Features** (Working & Tested)
- **Enhanced Analysis**: NLP-powered decision extraction with confidence scoring
- **Interactive Mindmaps**: Plotly-based decision flow visualizations
- **Sentiment Analysis**: Emotional context detection around decisions
- **Technical Domain Classification**: Auto-categorize conversations (AI/ML, DevOps, etc.)
- **Feature Flags System**: Environment-based feature toggles
- **Conversation Processing**: Parse and analyze AI chat exports

### **🚧 Experimental Features** (Alpha/Optional)
- **GPU Acceleration**: Optional GPU processing for high-end cards (RTX 4080/4090 tested)
- **Local AI Integration**: LM Studio compatibility for local models
- **Canvas Generation**: Visual output creation from conversations

### **📁 Knowledge Management** (In Progress)
- **Automated Organization**: Smart file categorization based on content
- **Metadata Generation**: Automatic tagging and frontmatter creation
- **Obsidian Integration**: Direct vault compatibility for knowledge bases

### **⚠️ Current Limitations**
- GPU features require NVIDIA cards with 12GB+ VRAM (but gracefully disabled if unavailable)
- Alpha software - expect UI/UX improvements in future releases
- Some advanced features still experimental
- Best suited for technical users familiar with API endpoints

### **🎛️ Feature Flags**
ConvoCanvas uses environment variables to control feature availability:
```bash
ENABLE_ENHANCED_ANALYSIS=true  # Enable advanced NLP analysis
ENABLE_CANVAS_GENERATION=true  # Enable visual output generation
ENABLE_NLP=true               # Enable natural language processing
DISABLE_GPU=true              # Force disable GPU acceleration
```

## 🔧 How It Works

1. **Export** conversations using the [SaveMyPhind browser extension](https://github.com/Hugo-COLLIN/SaveMyPhind-conversation-exporter) by Hugo Collin
2. **Upload** to ConvoCanvas backend (FastAPI + Python)
3. **Process** conversations to extract key decisions, technical concepts, and learning moments
4. **Generate** content ideas and context summaries for future sessions

```mermaid
---
config:
  theme: redux-dark
  look: neo
---
flowchart TB
    subgraph Input["📥 Input Layer"]
        A("🤖<br>AI Conversations")
        B("📄<br>SaveMyPhind<br>Export")
        C("📋<br>Markdown/TXT<br>Files")
    end

    subgraph API["🚀 ConvoCanvas API (FastAPI)"]
        D("🎛️<br>Feature Flags<br>System")
        E("📡<br>/api/conversations/<br>upload")
        F("🧠<br>/api/v2/conversations/<br>analyze-enhanced")
        G("⚡<br>/api/v3/conversations/<br>gpu-accelerated")
    end

    subgraph Processing["🔄 Analysis Engine"]
        H("📊<br>Enhanced Content<br>Analyzer")
        I("💭<br>Decision<br>Extraction")
        J("😊<br>Sentiment<br>Analysis")
        K("🏷️<br>Technical Domain<br>Classification")
        L("🧮<br>NLP Pipeline<br>spaCy + TextBlob")
    end

    subgraph Visualization["📈 Visualization Layer"]
        M("🗺️<br>Interactive<br>Mindmaps")
        N("📊<br>Plotly<br>Visualizations")
        O("🎨<br>Decision Flow<br>Networks")
    end

    subgraph Output["📤 Output Layer"]
        P("📋<br>Decision<br>Analysis")
        Q("💡<br>Content<br>Ideas")
        R("📊<br>JSON API<br>Response")
        S("🎯<br>Confidence<br>Scores")
    end

    subgraph Features["🎛️ Feature Management"]
        T("🔧<br>Environment<br>Variables")
        U("⚙️<br>Optional GPU<br>Acceleration")
        V("🧪<br>Experimental<br>Features")
    end

    %% Flow connections
    A --> B --> C
    C --> E
    C --> F
    C --> G

    D --> E
    D --> F
    D --> G

    E --> H
    F --> H
    G --> H

    H --> I
    H --> J
    H --> K
    H --> L

    I --> M
    J --> M
    K --> M
    L --> N

    M --> O
    N --> O

    O --> P
    O --> Q
    O --> R
    O --> S

    T --> D
    U --> D
    V --> D

    %% Styling
    style A fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#ffffff
    style H fill:#059669,stroke:#047857,stroke-width:2px,color:#ffffff
    style M fill:#dc2626,stroke:#b91c1c,stroke-width:2px,color:#ffffff
    style D fill:#7c3aed,stroke:#6d28d9,stroke-width:2px,color:#ffffff
    style P fill:#ea580c,stroke:#c2410c,stroke-width:2px,color:#ffffff
```

## 🏗️ Architecture Overview

ConvoCanvas follows a modern microservices-inspired architecture with clear separation of concerns:

### **📥 Input Layer**
- **AI Conversations**: Raw chat exports from Claude, ChatGPT, etc.
- **SaveMyPhind Integration**: Seamless browser extension workflow
- **File Support**: Markdown (.md) and text (.txt) formats

### **🚀 API Layer (FastAPI)**
- **Feature Flags System**: Environment-controlled feature toggles
- **Tiered Endpoints**: Basic → Enhanced → GPU-accelerated processing
- **RESTful Design**: Standard HTTP methods with JSON responses

### **🔄 Analysis Engine**
- **Enhanced Content Analyzer**: Core NLP processing pipeline
- **Decision Extraction**: AI-powered decision point identification
- **Sentiment Analysis**: TextBlob-based emotional context detection
- **Domain Classification**: spaCy-powered technical categorization

### **📈 Visualization Layer**
- **Interactive Mindmaps**: Plotly-based decision flow networks
- **Dynamic Layouts**: Force-directed graph positioning
- **Responsive Design**: Scales with conversation complexity

### **📤 Output Layer**
- **Structured Analysis**: JSON responses with confidence scores
- **Content Ideas**: Actionable insights for LinkedIn/blog posts
- **Decision Tracking**: Historical decision patterns and outcomes

## 🚀 Quick Start

### Development Setup

```bash
# Clone and setup
git clone https://github.com/rduffyuk/convocanvas.git
cd convocanvas

# Backend (Python/FastAPI)
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test the API
curl -X GET http://localhost:8000/
```

### Docker Setup

```bash
docker-compose up --build
```

### Try It Out

```bash
# Test the API endpoints
curl -X GET http://localhost:8000/

# Check feature flags
curl -X GET http://localhost:8000/feature-flags

# Upload a conversation file (basic parsing)
curl -X POST "http://localhost:8000/api/conversations/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-conversation.md"

# Enhanced analysis with decision tracking and mindmaps
curl -X POST "http://localhost:8000/api/v2/conversations/analyze-enhanced" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-conversation.md"
```

## 🏗️ Current Status

### **Core Platform** ✅
- ✅ **Enhanced Analysis API**: Decision extraction with confidence scoring
- ✅ **Interactive Mindmaps**: Plotly-based decision flow visualizations
- ✅ **Sentiment Analysis**: Emotional context detection around decisions
- ✅ **Technical Domain Classification**: Auto-categorize conversations by domain
- ✅ **Feature Flags System**: Environment-based feature toggles
- ✅ **API Foundation**: Multiple endpoint tiers (basic, enhanced, GPU)
- ✅ **SaveMyPhind Integration**: Parse exported conversation formats

### **Complete Automation System** 🆕 ✅
- ✅ **LibreChat Integration**: Full local AI deployment with web search
- ✅ **Universal File Organization**: Automated Obsidian vault management
- ✅ **Smart Tagging System**: YAML frontmatter automation across 56+ files
- ✅ **Local-First Architecture**: No external API dependencies for core AI
- ✅ **Perplexity-Style Search**: Real-time web search with citations
- ✅ **Auto-Documentation**: Self-generating session logs and system updates

### **Production Features** ✅
- ✅ **Error Handling**: Graceful degradation for missing dependencies
- ✅ **Testing Framework**: Comprehensive API endpoint testing completed
- ✅ **Production Config**: Docker + nginx setup with deployment guides
- 🚧 **Web Interface**: API-based (UI planned for future release)
- 📋 **Advanced Features**: Context summarization, knowledge graphs (future)
- 📋 **Monitoring**: Production logging and monitoring (future)

## 🛠️ Technology Stack

- **Backend**: FastAPI + Python 3.12+
- **NLP Processing**: spaCy + TextBlob + scikit-learn
- **Visualization**: Plotly + NetworkX for interactive mindmaps
- **Feature Management**: Environment-based feature flags
- **Production**: Docker + nginx + comprehensive testing
- **Integration**: SaveMyPhind browser extension support

## 🛣️ Roadmap

### Phase 1: Core Platform ✅
- [x] Conversation file parser
- [x] Basic content extraction
- [x] API endpoints
- [x] SaveMyPhind format support

### Phase 2: Enhanced Analysis 🚧
- [ ] Context summarization for session continuity
- [ ] Technical decision tracking
- [ ] Multi-conversation thread analysis
- [ ] Web interface for easier testing

### Phase 3: Automation 📋
- [ ] Browser extension integration
- [ ] Automated content generation
- [ ] Export to content platforms
- [ ] Knowledge graph visualization

## 🎯 Use Cases

**For Technical Professionals:**
- Maintain context across multi-day debugging sessions
- Extract learning insights from AI-assisted problem solving
- Generate technical content from real troubleshooting experiences

**For Content Creators:**
- Transform technical conversations into blog post ideas
- Generate LinkedIn posts from learning moments
- Track technical learning journey over time

**For Career Transitioners:**
- Document skill development through AI conversations
- Create portfolio content from learning processes
- Bridge knowledge gaps between domains

## 🤝 Contributing

**Note: This project is in early development.** While contributions are welcome, expect frequent changes to the codebase as I build toward the first stable release.

This started as a personal tool for my Windows→Linux→DevOps journey, but it's built to help anyone facing the AI context window problem.

**Built with conversations that ConvoCanvas now analyzes** - the entire project was planned in the very AI chats that it processes.

### Development Roadmap
- **Phase 1 (Current)**: Core parsing and basic content extraction
- **Phase 2**: Robust error handling, testing, and web interface  
- **Phase 3**: Advanced AI features and production readiness
- **v1.0.0**: First stable release

## 📋 Requirements

- Python 3.12+
- FastAPI
- SaveMyPhind browser extension for conversation exports

## 🔗 Related Projects

- [SaveMyPhind Extension](https://github.com/Hugo-COLLIN/SaveMyPhind-conversation-exporter) by Hugo Collin - Essential for exporting conversations
- [Obsidian](https://obsidian.md/) - Knowledge management app for manual workflow integration

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**From network engineering to automation, one conversation at a time.** 🌐→🤖
