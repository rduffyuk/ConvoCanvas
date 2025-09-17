# 🎬 ConvoCanvas Demo

Quick demonstration of ConvoCanvas capabilities using the example vault.

## 🚀 30-Second Demo

```bash
# 1. Start ConvoCanvas (in another terminal)
cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --port 8000

# 2. Process the example conversation
cd example-vault
./Scripts/process-conversation.sh Input/Conversations/example-chat.md

# 3. View results
ls -la Output/*/
```

## 📊 What You'll See

### Input
- **Raw conversation**: DevOps pipeline discussion between human and AI

### Output
- **Basic analysis**: Title, word count, source detection
- **Enhanced analysis**: 6 decisions extracted with confidence scores
- **Interactive mindmap**: HTML visualization showing decision relationships
- **Content ideas**: Generated LinkedIn posts and blog topics
- **Technical domains**: Classified as DevOps, CI/CD, Kubernetes

### Sample Decision Extraction
```json
{
  "id": "decision_1",
  "text": "Use GitHub Actions for CI/CD pipeline",
  "confidence": 0.85,
  "sentiment": {"polarity": 0.7, "subjectivity": 0.4},
  "technical_domains": ["devops", "automation"],
  "context": "For microservices with Docker and Kubernetes..."
}
```

### Sample Content Ideas
- "🚀 Choosing the Right CI/CD Tool: GitHub Actions vs Jenkins vs GitLab"
- "Blog: Database Migration Strategies in Microservices Architecture"
- "LinkedIn: 3 Critical Decisions Every DevOps Team Must Make"

## 🎯 Key Benefits Demonstrated

1. **Decision Tracking**: Automatically extracts and categorizes decisions
2. **Visual Analysis**: Interactive mindmaps show decision relationships
3. **Content Generation**: Creates social media and blog content ideas
4. **Domain Classification**: Categorizes conversations by technical domain
5. **Sentiment Analysis**: Understands emotional context around decisions

## 🔄 Integration Options

- **Obsidian**: Use as vault or integrate with existing workflow
- **Standalone**: Process conversations and export to any system
- **API-first**: Build custom integrations with the core API
- **Automated**: Set up processing pipelines for exported conversations

## 📈 Real-World Applications

- **Technical Teams**: Track architectural decisions and reasoning
- **Content Creators**: Generate ideas from learning conversations
- **Project Managers**: Visualize decision flows and dependencies
- **Individual Learning**: Build searchable knowledge base from AI interactions

---

*This demo shows ConvoCanvas processing a single conversation. In practice, you'd process multiple conversations over time to build a comprehensive decision and knowledge tracking system.*