"""Enhanced AI-powered content analyzer with decision tracking and visualization"""
import re
import json
from typing import List, Dict, Tuple, Any
from collections import Counter, defaultdict
import spacy
import nltk
from textblob import TextBlob
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EnhancedContentAnalyzer:
    """AI-powered content analyzer with decision tracking and visual insights"""

    def __init__(self):
        """Initialize NLP models and components"""
        # Load spaCy model (install with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None

        # Decision patterns for extraction
        self.decision_patterns = [
            r'(?:decided|decision|choose|chose|selected|pick|go with|opt for|settle on)\s+(?:to\s+)?([^.!?]+)',
            r'(?:let\'s|we should|i think we should|recommend|suggest)\s+([^.!?]+)',
            r'(?:final|conclusion|outcome|result):\s*([^.!?]+)',
            r'(?:approach|strategy|plan|solution):\s*([^.!?]+)'
        ]

        # Technical domain keywords for context
        self.tech_domains = {
            'networking': ['network', 'router', 'switch', 'bgp', 'ospf', 'mpls', 'vpn', 'firewall'],
            'automation': ['ci/cd', 'pipeline', 'docker', 'kubernetes', 'ansible', 'terraform'],
            'development': ['api', 'fastapi', 'react', 'nextjs', 'python', 'javascript', 'github'],
            'ai_ml': ['llm', 'ai', 'machine learning', 'neural', 'model', 'training'],
            'monitoring': ['grafana', 'prometheus', 'elk', 'logging', 'metrics', 'alerting']
        }

    def extract_user_claude_dialogue(self, content: str) -> List[Dict]:
        """Extract structured user/Claude dialogue with enhanced metadata"""
        messages = []
        sections = re.split(r'(?=## (?:User|Claude))', content)

        for i, section in enumerate(sections):
            if section.strip():
                if section.startswith('## User'):
                    role = 'user'
                    text = re.sub(r'^## User\s*', '', section, flags=re.MULTILINE).strip()
                elif section.startswith('## Claude'):
                    role = 'claude'
                    text = re.sub(r'^## Claude\s*', '', section, flags=re.MULTILINE).strip()
                else:
                    continue

                if text:
                    # Enhanced message metadata
                    message = {
                        "role": role,
                        "content": text,
                        "sequence": i,
                        "word_count": len(text.split()),
                        "sentiment": self._analyze_sentiment(text),
                        "entities": self._extract_entities(text),
                        "technical_domain": self._classify_technical_domain(text)
                    }
                    messages.append(message)

        return messages

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using TextBlob"""
        blob = TextBlob(text)
        return {
            "polarity": blob.sentiment.polarity,  # -1 (negative) to 1 (positive)
            "subjectivity": blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        }

    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return []

        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "description": spacy.explain(ent.label_)
            })
        return entities

    def _classify_technical_domain(self, text: str) -> List[str]:
        """Classify text into technical domains"""
        text_lower = text.lower()
        domains = []

        for domain, keywords in self.tech_domains.items():
            if any(keyword in text_lower for keyword in keywords):
                domains.append(domain)

        return domains

    def extract_decisions(self, messages: List[Dict]) -> List[Dict]:
        """Extract technical decisions from conversation using NLP"""
        decisions = []

        for msg_idx, message in enumerate(messages):
            content = message['content']

            # Extract decisions using patterns
            for pattern in self.decision_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    decision_text = match.group(1).strip()

                    # Skip very short decisions
                    if len(decision_text.split()) < 3:
                        continue

                    decision = {
                        "id": f"decision_{len(decisions)}",
                        "text": decision_text,
                        "context": content,
                        "message_index": msg_idx,
                        "role": message['role'],
                        "technical_domains": message['technical_domain'],
                        "sentiment": self._analyze_sentiment(decision_text),
                        "entities": self._extract_entities(decision_text),
                        "confidence": self._calculate_decision_confidence(decision_text, content)
                    }
                    decisions.append(decision)

        return decisions

    def _calculate_decision_confidence(self, decision_text: str, context: str) -> float:
        """Calculate confidence score for decision extraction"""
        # Simple heuristic based on decision keywords and context
        decision_keywords = ['final', 'conclude', 'definitive', 'certain', 'confirmed']
        uncertainty_keywords = ['maybe', 'perhaps', 'might', 'could', 'possibly']

        decision_score = sum(1 for word in decision_keywords if word in decision_text.lower())
        uncertainty_score = sum(1 for word in uncertainty_keywords if word in decision_text.lower())

        # Base confidence + decision keywords - uncertainty keywords
        confidence = 0.5 + (decision_score * 0.2) - (uncertainty_score * 0.1)
        return max(0.0, min(1.0, confidence))

    def create_decision_mindmap(self, decisions: List[Dict]) -> Dict[str, Any]:
        """Create interactive mindmap data for decisions"""
        if not decisions:
            return {"nodes": [], "edges": [], "html": ""}

        # Create NetworkX graph
        G = nx.Graph()

        # Add decision nodes
        for decision in decisions:
            G.add_node(
                decision['id'],
                label=decision['text'][:50] + '...' if len(decision['text']) > 50 else decision['text'],
                full_text=decision['text'],
                domains=decision['technical_domains'],
                confidence=decision['confidence'],
                role=decision['role']
            )

        # Connect related decisions (same technical domain)
        for i, dec1 in enumerate(decisions):
            for j, dec2 in enumerate(decisions[i+1:], i+1):
                # Connect if they share technical domains
                shared_domains = set(dec1['technical_domains']) & set(dec2['technical_domains'])
                if shared_domains:
                    G.add_edge(dec1['id'], dec2['id'], weight=len(shared_domains))

        # Convert to visualization format
        pos = nx.spring_layout(G, k=1, iterations=50)

        # Create nodes for visualization
        nodes = []
        for node_id, data in G.nodes(data=True):
            x, y = pos[node_id]
            nodes.append({
                "id": node_id,
                "label": data['label'],
                "full_text": data['full_text'],
                "x": float(x),
                "y": float(y),
                "domains": data['domains'],
                "confidence": data['confidence'],
                "role": data['role'],
                "color": self._get_node_color(data['domains'])
            })

        # Create edges
        edges = []
        for edge in G.edges(data=True):
            edges.append({
                "source": edge[0],
                "target": edge[1],
                "weight": edge[2].get('weight', 1)
            })

        # Generate Plotly visualization
        html_viz = self._create_plotly_mindmap(nodes, edges)

        return {
            "nodes": nodes,
            "edges": edges,
            "html": html_viz,
            "summary": {
                "total_decisions": len(decisions),
                "high_confidence": len([d for d in decisions if d['confidence'] > 0.7]),
                "technical_domains": list(set().union(*[d['technical_domains'] for d in decisions])),
                "user_decisions": len([d for d in decisions if d['role'] == 'user']),
                "claude_decisions": len([d for d in decisions if d['role'] == 'claude'])
            }
        }

    def _get_node_color(self, domains: List[str]) -> str:
        """Get color for node based on technical domains"""
        color_map = {
            'networking': '#FF6B6B',
            'automation': '#4ECDC4',
            'development': '#45B7D1',
            'ai_ml': '#96CEB4',
            'monitoring': '#FFEAA7'
        }

        # Return color of first domain, or default
        if domains:
            return color_map.get(domains[0], '#DDA0DD')
        return '#DDA0DD'

    def _create_plotly_mindmap(self, nodes: List[Dict], edges: List[Dict]) -> str:
        """Create interactive Plotly mindmap visualization"""
        # Create edge traces
        edge_x = []
        edge_y = []

        node_map = {node['id']: node for node in nodes}

        for edge in edges:
            source = node_map[edge['source']]
            target = node_map[edge['target']]
            edge_x.extend([source['x'], target['x'], None])
            edge_y.extend([source['y'], target['y'], None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        # Create node trace
        node_x = [node['x'] for node in nodes]
        node_y = [node['y'] for node in nodes]
        node_colors = [node['color'] for node in nodes]
        node_text = [f"{node['label']}<br>Confidence: {node['confidence']:.1%}<br>Domains: {', '.join(node['domains'])}"
                     for node in nodes]

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=node_text,
            text=[node['label'] for node in nodes],
            textposition="middle center",
            marker=dict(
                size=30,
                color=node_colors,
                line=dict(width=2, color='white')
            )
        )

        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Technical Decision Mindmap',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Hover over nodes for details",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="#888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))

        return fig.to_html()

    def generate_enhanced_content_ideas(self, messages: List[Dict], decisions: List[Dict]) -> Dict:
        """Generate enhanced content ideas using AI analysis"""
        if not messages:
            return {}

        # Extract topics using TF-IDF
        texts = [msg['content'] for msg in messages]

        try:
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()

            # Get top terms
            tfidf_scores = tfidf_matrix.sum(axis=0).A1
            top_terms = [(feature_names[i], tfidf_scores[i]) for i in tfidf_scores.argsort()[-20:][::-1]]
        except:
            top_terms = []

        # Analyze conversation flow
        sentiment_flow = [msg['sentiment']['polarity'] for msg in messages]
        avg_sentiment = np.mean(sentiment_flow) if sentiment_flow else 0

        # Count technical domains
        all_domains = []
        for msg in messages:
            all_domains.extend(msg['technical_domain'])
        domain_counts = Counter(all_domains)

        # Generate personalized content
        ideas = {
            'linkedin_posts': self._generate_linkedin_posts(messages, decisions, top_terms, domain_counts),
            'blog_topics': self._generate_blog_topics(messages, decisions, top_terms, domain_counts),
            'technical_concepts': [term for term, score in top_terms[:10]],
            'conversation_themes': list(domain_counts.keys()),
            'decisions_summary': {
                'total_decisions': len(decisions),
                'high_confidence_decisions': len([d for d in decisions if d['confidence'] > 0.7]),
                'decision_domains': list(set().union(*[d['technical_domains'] for d in decisions if d['technical_domains']]))
            },
            'sentiment_analysis': {
                'overall_sentiment': 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral',
                'sentiment_score': avg_sentiment,
                'sentiment_flow': sentiment_flow
            },
            'conversation_stats': {
                'total_messages': len(messages),
                'user_messages': len([m for m in messages if m['role'] == 'user']),
                'claude_messages': len([m for m in messages if m['role'] == 'claude']),
                'avg_message_length': np.mean([msg['word_count'] for msg in messages]) if messages else 0
            }
        }

        return ideas

    def _generate_linkedin_posts(self, messages, decisions, top_terms, domain_counts):
        """Generate personalized LinkedIn posts based on conversation analysis"""
        posts = []

        # Network engineering focus
        if 'networking' in domain_counts:
            posts.append(
                "🌐 Network Engineer → DevOps Journey: Today I tackled [specific challenge from conversation]. "
                f"Key insight: {top_terms[0][0] if top_terms else 'automation is everything'}. "
                "The transition continues! #NetworkEngineering #DevOps #Automation"
            )

        # Decision-focused posts
        if decisions:
            high_conf_decisions = [d for d in decisions if d['confidence'] > 0.7]
            if high_conf_decisions:
                posts.append(
                    f"💡 Technical Decision Log: Made {len(high_conf_decisions)} key decisions today. "
                    f"Biggest impact: {high_conf_decisions[0]['text'][:100]}... "
                    "Decision tracking is a game-changer for complex projects! #TechLeadership #DecisionMaking"
                )

        # ConvoCanvas development
        if any('convocanvas' in msg['content'].lower() for msg in messages):
            posts.append(
                "🚀 Building ConvoCanvas: Transforming AI conversations into actionable insights. "
                f"Today's focus: {', '.join(list(domain_counts.keys())[:2])}. "
                "The future of conversation analysis is here! #AI #ConversationAI #ProductDevelopment"
            )

        return posts

    def _generate_blog_topics(self, messages, decisions, top_terms, domain_counts):
        """Generate blog topics based on conversation analysis"""
        topics = []

        # Technical deep-dives
        if top_terms:
            topics.append({
                "title": f"Deep Dive: {top_terms[0][0].title()} in Practice",
                "subtitle": "Real-world implementation and lessons learned",
                "estimated_length": "1500-2000 words"
            })

        # Decision tracking methodology
        if decisions:
            topics.append({
                "title": "Technical Decision Tracking: A Visual Approach",
                "subtitle": "How mindmaps revolutionized my engineering workflow",
                "estimated_length": "1200-1500 words"
            })

        # Multi-domain posts
        if len(domain_counts) > 2:
            domains_str = " + ".join(list(domain_counts.keys())[:3])
            topics.append({
                "title": f"Bridging {domains_str}: An Integration Story",
                "subtitle": "When multiple technical domains collide",
                "estimated_length": "2000-2500 words"
            })

        return topics

# Backward compatibility function
def extract_content_ideas(content: str) -> Dict:
    """Backward compatible function using enhanced analyzer"""
    analyzer = EnhancedContentAnalyzer()
    messages = analyzer.extract_user_claude_dialogue(content)
    decisions = analyzer.extract_decisions(messages)
    return analyzer.generate_enhanced_content_ideas(messages, decisions)