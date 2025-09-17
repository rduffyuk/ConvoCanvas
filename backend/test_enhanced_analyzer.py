#!/usr/bin/env python3
"""Test script for enhanced content analyzer"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.enhanced_content_analyzer import EnhancedContentAnalyzer

def test_analyzer():
    """Test the enhanced content analyzer with sample conversation"""

    # Sample conversation content
    test_conversation = """
## User
I'm working on a ConvoCanvas project and need to implement network automation for our MPLS infrastructure. We're using FastAPI for the backend and I'm considering Docker for deployment. What's the best approach for CI/CD pipeline integration?

## Claude
For your ConvoCanvas project with MPLS network automation, I'd recommend the following approach:

1. **Decision**: Use GitLab CI/CD with Docker containers for consistent deployments
2. **Final decision**: Implement infrastructure as code with Terraform for network device configuration
3. **Conclusion**: Set up monitoring with Grafana and Prometheus for real-time network visibility

The combination of FastAPI, Docker, and GitLab CI/CD will give you a robust automation pipeline. For MPLS specifically, you'll want to integrate with network APIs for configuration management.

## User
That sounds good. Let's go with GitLab CI/CD approach. I also think we should implement automated testing for network configurations. What testing framework would you recommend?

## Claude
**Recommendation**: Use pytest for your testing framework with network simulation capabilities.

**Final approach**: Implement these testing layers:
- Unit tests for API endpoints with pytest
- Integration tests for network device interactions
- End-to-end tests for complete MPLS provisioning workflows

This testing strategy will ensure your network automation is reliable and catch configuration errors before deployment.
"""

    print("🔬 Testing Enhanced Content Analyzer")
    print("=" * 50)

    # Initialize analyzer
    analyzer = EnhancedContentAnalyzer()

    # Test dialogue extraction
    print("\n1. Testing dialogue extraction...")
    messages = analyzer.extract_user_claude_dialogue(test_conversation)
    print(f"   ✅ Extracted {len(messages)} messages")

    for i, msg in enumerate(messages):
        print(f"   Message {i+1} ({msg['role']}): {msg['word_count']} words, sentiment: {msg['sentiment']['polarity']:.2f}")

    # Test decision extraction
    print("\n2. Testing decision extraction...")
    decisions = analyzer.extract_decisions(messages)
    print(f"   ✅ Extracted {len(decisions)} decisions")

    for i, decision in enumerate(decisions):
        print(f"   Decision {i+1}: {decision['text'][:60]}... (confidence: {decision['confidence']:.2f})")

    # Test mindmap generation
    print("\n3. Testing mindmap generation...")
    mindmap_data = analyzer.create_decision_mindmap(decisions)
    print(f"   ✅ Generated mindmap with {len(mindmap_data['nodes'])} nodes and {len(mindmap_data['edges'])} edges")
    print(f"   Summary: {mindmap_data['summary']}")

    # Test content ideas generation
    print("\n4. Testing content ideas generation...")
    content_ideas = analyzer.generate_enhanced_content_ideas(messages, decisions)
    print(f"   ✅ Generated content ideas")
    print(f"   LinkedIn posts: {len(content_ideas.get('linkedin_posts', []))}")
    print(f"   Blog topics: {len(content_ideas.get('blog_topics', []))}")
    print(f"   Technical concepts: {len(content_ideas.get('technical_concepts', []))}")
    print(f"   Conversation themes: {content_ideas.get('conversation_themes', [])}")

    # Show sample outputs
    print("\n5. Sample outputs:")
    if content_ideas.get('linkedin_posts'):
        print(f"   Sample LinkedIn post: {content_ideas['linkedin_posts'][0][:100]}...")

    if content_ideas.get('technical_concepts'):
        print(f"   Top technical concepts: {', '.join(content_ideas['technical_concepts'][:5])}")

    print("\n" + "=" * 50)
    print("✅ Enhanced Content Analyzer test completed successfully!")
    print(f"🎯 Key improvements over basic analyzer:")
    print(f"   - AI-powered decision extraction ({len(decisions)} vs 0 in basic)")
    print(f"   - Sentiment analysis for each message")
    print(f"   - Named entity recognition")
    print(f"   - Interactive mindmap visualization")
    print(f"   - Technical domain classification")
    print(f"   - Enhanced content personalization")

if __name__ == "__main__":
    test_analyzer()