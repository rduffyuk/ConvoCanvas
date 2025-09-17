"""
Obsidian Canvas Generator for Decision Visualization
Creates native .canvas files for decision flow diagrams
"""
import json
import uuid
import base64
import zlib
from typing import List, Dict, Any, Tuple
import math

class CanvasDecisionVisualizer:
    """Generates Obsidian Canvas files for decision visualization"""

    def __init__(self):
        self.canvas_width = 2000
        self.canvas_height = 1500
        self.node_width = 300
        self.node_height = 150
        self.padding = 50

        # Color scheme for different decision types
        self.colors = {
            "user_decision": "1",      # Red - user decisions
            "assistant_decision": "2", # Blue - assistant decisions
            "technical": "3",          # Green - technical decisions
            "process": "4",            # Yellow - process decisions
            "recommendation": "5",     # Purple - recommendations
            "summary": "6"             # Gray - summary nodes
        }

    def create_decision_canvas(self, decisions: List[Dict], conversation_title: str = "Decision Flow") -> str:
        """
        Create a Canvas file showing decision flow and relationships

        Args:
            decisions: List of decision objects with text, confidence, role, etc.
            conversation_title: Title for the canvas

        Returns:
            JSON string for .canvas file
        """
        if not decisions:
            return self._create_empty_canvas(conversation_title)

        nodes = []
        edges = []

        # Create title node
        title_node = self._create_title_node(conversation_title, len(decisions))
        nodes.append(title_node)

        # Create decision nodes in a flow layout
        positions = self._calculate_flow_positions(len(decisions))

        for i, decision in enumerate(decisions):
            node = self._create_decision_node(decision, positions[i], i)
            nodes.append(node)

            # Connect to previous decision (create flow)
            if i > 0:
                edge = self._create_edge(f"decision-{i-1}", f"decision-{i}")
                edges.append(edge)

            # Connect first decision to title
            if i == 0:
                edge = self._create_edge("title", f"decision-{i}")
                edges.append(edge)

        # Add summary/insights node if multiple decisions
        if len(decisions) > 2:
            summary_node = self._create_summary_node(decisions)
            nodes.append(summary_node)

            # Connect last decision to summary
            if decisions:
                edge = self._create_edge(f"decision-{len(decisions)-1}", "summary")
                edges.append(edge)

        canvas = {
            "nodes": nodes,
            "edges": edges
        }

        return json.dumps(canvas, indent=2)

    def _create_title_node(self, title: str, decision_count: int) -> Dict:
        """Create the main title node for the canvas"""
        return {
            "id": "title",
            "x": self.canvas_width // 2 - self.node_width // 2,
            "y": 50,
            "width": self.node_width + 100,
            "height": 120,
            "color": self.colors["summary"],
            "type": "text",
            "text": f"# {title}\n\n**Decisions Identified:** {decision_count}\n**Analysis Date:** $(date)\n\n*AI-Generated Decision Flow Visualization*"
        }

    def _create_decision_node(self, decision: Dict, position: Tuple[int, int], index: int) -> Dict:
        """Create a node for a specific decision"""
        x, y = position

        # Determine node color based on decision properties
        color = self._get_decision_color(decision)

        # Format decision text for canvas display
        decision_text = self._format_decision_text(decision, index + 1)

        return {
            "id": f"decision-{index}",
            "x": x,
            "y": y,
            "width": self.node_width,
            "height": self.node_height,
            "color": color,
            "type": "text",
            "text": decision_text
        }

    def _create_summary_node(self, decisions: List[Dict]) -> Dict:
        """Create a summary node with decision insights"""
        # Calculate summary statistics
        total_decisions = len(decisions)
        user_decisions = len([d for d in decisions if d.get('role') == 'user'])
        assistant_decisions = len([d for d in decisions if d.get('role') == 'assistant'])
        avg_confidence = sum(d.get('confidence', 0) for d in decisions) / total_decisions if decisions else 0

        # Count technical domains
        domains = {}
        for decision in decisions:
            for domain in decision.get('technical_domains', []):
                domains[domain] = domains.get(domain, 0) + 1

        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:3]

        summary_text = f"""## 📊 Decision Summary

**Total Decisions:** {total_decisions}
**User Decisions:** {user_decisions}
**Assistant Decisions:** {assistant_decisions}
**Average Confidence:** {avg_confidence:.1%}

**Top Technical Domains:**
{chr(10).join([f"- {domain}: {count}" for domain, count in top_domains])}

**Decision Flow Pattern:**
Sequential decision-making process with {total_decisions} key decision points identified through AI analysis.
"""

        return {
            "id": "summary",
            "x": self.canvas_width // 2 - (self.node_width + 50) // 2,
            "y": self.canvas_height - 200,
            "width": self.node_width + 50,
            "height": 180,
            "color": self.colors["summary"],
            "type": "text",
            "text": summary_text
        }

    def _calculate_flow_positions(self, count: int) -> List[Tuple[int, int]]:
        """Calculate positions for decision nodes in a flowing layout"""
        positions = []

        if count <= 3:
            # Simple horizontal layout for few decisions
            start_x = (self.canvas_width - (count * (self.node_width + self.padding))) // 2
            y = 300

            for i in range(count):
                x = start_x + i * (self.node_width + self.padding)
                positions.append((x, y))
        else:
            # Multi-row zigzag layout for many decisions
            nodes_per_row = 3
            rows = math.ceil(count / nodes_per_row)

            for i in range(count):
                row = i // nodes_per_row
                col = i % nodes_per_row

                # Zigzag: reverse every other row
                if row % 2 == 1:
                    col = nodes_per_row - 1 - col

                x = 200 + col * (self.node_width + self.padding)
                y = 300 + row * (self.node_height + self.padding)

                positions.append((x, y))

        return positions

    def _get_decision_color(self, decision: Dict) -> str:
        """Determine canvas color based on decision properties"""
        role = decision.get('role', 'unknown')
        decision_type = decision.get('type', 'general')

        if role == 'user':
            return self.colors["user_decision"]
        elif role == 'assistant':
            return self.colors["assistant_decision"]
        elif 'technical' in decision_type.lower():
            return self.colors["technical"]
        elif 'process' in decision_type.lower():
            return self.colors["process"]
        else:
            return self.colors["recommendation"]

    def _format_decision_text(self, decision: Dict, number: int) -> str:
        """Format decision for display in canvas node"""
        text = decision.get('text', 'No decision text available')
        confidence = decision.get('confidence', 0)
        role = decision.get('role', 'unknown')

        # Truncate long text
        if len(text) > 150:
            text = text[:147] + "..."

        # Format with metadata
        role_emoji = "👤" if role == 'user' else "🤖"
        confidence_bar = "█" * int(confidence * 5) + "░" * (5 - int(confidence * 5))

        return f"""## {role_emoji} Decision #{number}

**{text}**

**Confidence:** {confidence:.1%}
`{confidence_bar}`

**Role:** {role.title()}
**Type:** {decision.get('type', 'General').title()}
"""

    def _create_edge(self, from_node: str, to_node: str) -> Dict:
        """Create an edge connecting two nodes"""
        return {
            "id": f"{from_node}-to-{to_node}",
            "fromNode": from_node,
            "fromSide": "bottom",
            "toNode": to_node,
            "toSide": "top"
        }

    def _create_empty_canvas(self, title: str) -> str:
        """Create a canvas when no decisions are found"""
        node = {
            "id": "no-decisions",
            "x": self.canvas_width // 2 - self.node_width // 2,
            "y": self.canvas_height // 2 - self.node_height // 2,
            "width": self.node_width,
            "height": self.node_height,
            "color": self.colors["summary"],
            "type": "text",
            "text": f"# {title}\n\n**No Decisions Found**\n\nThis conversation may not contain clear decision points, or they may need to be identified manually.\n\n*Try analyzing a conversation with more explicit decision-making content.*"
        }

        canvas = {
            "nodes": [node],
            "edges": []
        }

        return json.dumps(canvas, indent=2)

class ExcalidrawDecisionVisualizer:
    """Generates Excalidraw files for decision visualization"""

    def __init__(self):
        self.width = 1200
        self.height = 800

    def create_decision_excalidraw(self, decisions: List[Dict], conversation_title: str = "Decision Flow") -> str:
        """
        Create an Excalidraw file for decision visualization

        Returns:
        Complete .excalidraw.md file content with frontmatter
        """
        if not decisions:
            return self._create_empty_excalidraw(conversation_title)

        # Generate Excalidraw elements
        elements = []

        # Add title
        title_element = self._create_text_element(
            text=f"{conversation_title}\n{len(decisions)} Decisions Found",
            x=50, y=50, font_size=24, width=400
        )
        elements.append(title_element)

        # Add decision boxes
        y_offset = 150
        for i, decision in enumerate(decisions):
            decision_element = self._create_decision_box(decision, 50, y_offset + i * 120, i + 1)
            elements.extend(decision_element)

        # Create Excalidraw JSON
        excalidraw_data = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
            "elements": elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff"
            },
            "files": {}
        }

        # Create uncompressed JSON format (easier for plugin to parse)
        json_string = json.dumps(excalidraw_data, indent=2)

        # Create full .excalidraw.md content with frontmatter (uncompressed format)
        content = f"""---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


# Text Elements
{conversation_title} - Decision Flow Visualization

# Drawing
```json
{json_string}
```
%%
"""

        return content

    def _create_text_element(self, text: str, x: int, y: int, font_size: int = 16, width: int = 200) -> Dict:
        """Create a text element for Excalidraw"""
        return {
            "type": "text",
            "version": 1,
            "versionNonce": self._generate_nonce(),
            "isDeleted": False,
            "id": str(uuid.uuid4()),
            "fillStyle": "hachure",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "angle": 0,
            "x": x,
            "y": y,
            "strokeColor": "#000000",
            "backgroundColor": "transparent",
            "width": width,
            "height": font_size * 1.2,
            "seed": 1234567890,
            "groupIds": [],
            "roundness": None,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
            "fontSize": font_size,
            "fontFamily": 1,
            "text": text,
            "rawText": text,
            "baseline": font_size,
            "textAlign": "left",
            "verticalAlign": "top",
            "containerId": None,
            "originalText": text
        }

    def _create_decision_box(self, decision: Dict, x: int, y: int, number: int) -> List[Dict]:
        """Create a decision box with rectangle and text"""
        elements = []

        # Rectangle background
        rect = {
            "type": "rectangle",
            "version": 1,
            "versionNonce": self._generate_nonce(),
            "isDeleted": False,
            "id": str(uuid.uuid4()),
            "fillStyle": "hachure",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "angle": 0,
            "x": x,
            "y": y,
            "strokeColor": self._get_decision_stroke_color(decision),
            "backgroundColor": self._get_decision_bg_color(decision),
            "width": 600,
            "height": 100,
            "seed": 1234567890,
            "groupIds": [],
            "roundness": {"type": 3},
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False
        }
        elements.append(rect)

        # Decision text
        decision_text = self._format_decision_for_excalidraw(decision, number)
        text = self._create_text_element(decision_text, x + 10, y + 10, 14, 580)
        elements.append(text)

        return elements

    def _get_decision_stroke_color(self, decision: Dict) -> str:
        """Get stroke color based on decision role"""
        role = decision.get('role', 'unknown')
        if role == 'user':
            return "#ff6b6b"  # Red for user decisions
        elif role == 'assistant':
            return "#4ecdc4"  # Teal for assistant decisions
        else:
            return "#45b7d1"  # Blue for other decisions

    def _get_decision_bg_color(self, decision: Dict) -> str:
        """Get background color based on decision confidence"""
        confidence = decision.get('confidence', 0)
        if confidence > 0.7:
            return "#e8f5e8"  # Light green for high confidence
        elif confidence > 0.4:
            return "#fff3cd"  # Light yellow for medium confidence
        else:
            return "#f8d7da"  # Light red for low confidence

    def _format_decision_for_excalidraw(self, decision: Dict, number: int) -> str:
        """Format decision text for Excalidraw display"""
        text = decision.get('text', 'No decision text')
        confidence = decision.get('confidence', 0)
        role = decision.get('role', 'unknown')

        # Truncate if too long
        if len(text) > 80:
            text = text[:77] + "..."

        role_symbol = "👤" if role == 'user' else "🤖"

        return f"{role_symbol} Decision #{number}: {text}\nConfidence: {confidence:.1%} | Role: {role.title()}"

    def _generate_nonce(self) -> int:
        """Generate a version nonce for Excalidraw elements"""
        return hash(str(uuid.uuid4())) % (10 ** 8)

    def _create_empty_excalidraw(self, title: str) -> str:
        """Create empty Excalidraw when no decisions found"""
        elements = [
            self._create_text_element(
                text=f"{title}\n\nNo decisions found in this conversation.\nTry analyzing content with explicit decision points.",
                x=100, y=200, font_size=18, width=600
            )
        ]

        excalidraw_data = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
            "elements": elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": "#ffffff"
            },
            "files": {}
        }

        # Create uncompressed JSON format (easier for plugin to parse)
        json_string = json.dumps(excalidraw_data, indent=2)

        content = f"""---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


# Text Elements
{title} - No Decisions Found

# Drawing
```json
{json_string}
```
%%
"""

        return content