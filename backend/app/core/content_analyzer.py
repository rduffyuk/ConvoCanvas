"""Enhanced content extraction with improved deduplication and content generation"""

import re
from typing import List, Dict


def extract_user_claude_dialogue(content: str) -> List[Dict]:
    """Extract structured user/Claude dialogue from Save My Chatbot format"""
    messages = []
    sections = re.split(r"(?=## (?:User|Claude))", content)

    for section in sections:
        if section.strip():
            if section.startswith("## User"):
                role = "user"
                text = re.sub(r"^## User\s*", "", section, flags=re.MULTILINE).strip()
            elif section.startswith("## Claude"):
                role = "claude"
                text = re.sub(r"^## Claude\s*", "", section, flags=re.MULTILINE).strip()
            else:
                continue

            if text:
                messages.append({"role": role, "content": text})

    return messages


def analyze_technical_concepts(messages: List[Dict]) -> List[str]:
    """Extract and deduplicate technical concepts"""
    technical_terms = set()
    tech_patterns = [
        r"\b(?:API|REST|GraphQL|webhook|Docker|Kubernetes|CI/CD|FastAPI|React|"
        r"Python|JavaScript|GitHub|Git)\b",
        r"\b(?:network|routing|MPLS|BGP|OSPF|monitoring|infrastructure)\b",
        r"\b(?:database|SQL|NoSQL|Redis|PostgreSQL|MongoDB)\b",
    ]

    for message in messages:
        for pattern in tech_patterns:
            matches = re.findall(pattern, message["content"], re.IGNORECASE)
            # Convert to lowercase for deduplication, then title case for display
            technical_terms.update([match.title() for match in matches])

    return sorted(list(technical_terms))


def extract_content_ideas(content: str) -> Dict:
    """Extract content opportunities from conversation"""
    messages = extract_user_claude_dialogue(content)
    technical_concepts = analyze_technical_concepts(messages)

    ideas = {
        "linkedin_posts": [],
        "blog_topics": [],
        "technical_concepts": technical_concepts,
        "message_count": len(messages),
        "user_messages": len([m for m in messages if m["role"] == "user"]),
        "claude_messages": len([m for m in messages if m["role"] == "claude"]),
        "conversation_themes": [],
    }

    full_text = " ".join([m["content"] for m in messages]).lower()

    # Identify conversation themes
    themes = []
    if "convocanvas" in full_text:
        themes.append("product_development")
        ideas["linkedin_posts"].append(
            "Building ConvoCanvas: From conversation exports to content automation"
        )
        ideas["blog_topics"].append(
            "ConvoCanvas Technical Deep Dive: Architecture and Implementation"
        )

    if "network engineer" in full_text and any(
        term in full_text for term in ["automation", "ci/cd", "docker"]
    ):
        themes.append("career_transition")
        ideas["linkedin_posts"].append(
            "Network Engineer → DevOps: My automation learning journey"
        )
        ideas["blog_topics"].append(
            "Bridging Infrastructure and Development: A Network Engineer's Perspective"
        )

    if "open source" in full_text:
        themes.append("open_source_strategy")
        ideas["blog_topics"].append(
            "Open Source First: Strategic Decision Framework for Technical Projects"
        )

    if "obsidian" in full_text and "ai" in full_text:
        themes.append("knowledge_management")
        ideas["blog_topics"].append(
            "AI-Enhanced Knowledge Management: Obsidian + Conversation Analysis"
        )

    ideas["conversation_themes"] = themes
    return ideas
