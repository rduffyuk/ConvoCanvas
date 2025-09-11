# ConvoCanvas

AI-powered creative content studio that transforms AI conversation history into multimedia content ideas.

## Vision

ConvoCanvas helps technical professionals document their learning journeys by extracting insights from AI conversations and generating content ideas for LinkedIn posts, blog articles, and educational content.

## Current Status: MVP Development

- ✅ Project planning complete
- ✅ Repository structure established  
- 🚧 Conversation parser development
- 🚧 Content suggestion engine
- 📋 Web interface (planned)

## Quick Start

### Development Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/convocanvas.git
cd convocanvas

# Run setup script
./scripts/dev-setup.sh

# Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Start frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Docker Setup

```bash
docker-compose up --build
```

## Architecture

- **Backend**: FastAPI + Python for conversation processing
- **Frontend**: Next.js + React for web interface  
- **Processing**: AI-powered content analysis and suggestion generation
- **Export**: Manual conversation exports via browser extensions

## Roadmap

### Week 1-2: Core Parser
- [x] Repository setup
- [ ] Conversation file parser
- [ ] Basic content extraction
- [ ] Unit tests

### Week 3-4: Content Engine  
- [ ] Content suggestion algorithms
- [ ] Template system
- [ ] Output formatting

### Week 5-6: Web Interface
- [ ] Upload interface
- [ ] Content review/editing
- [ ] Export capabilities

## Contributing

This is an open-source learning project. Contributions welcome!

## License

MIT License - see LICENSE file for details.
