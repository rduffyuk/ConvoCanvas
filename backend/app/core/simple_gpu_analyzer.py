"""
Simple GPU-Enhanced Conversation Analyzer for ConvoCanvas
Uses PyTorch GPU acceleration without complex model dependencies
"""

import torch
import logging
import spacy
from typing import Dict, List, Any, Optional
from datetime import datetime
import gc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleGPUAnalyzer:
    """Simplified GPU-accelerated conversation analyzer"""

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_gpu_available = torch.cuda.is_available()
        self.nlp = None
        self._initialize_models()

    def _initialize_models(self):
        """Initialize basic models"""
        try:
            if self.is_gpu_available:
                logger.info(f"🚀 GPU Device: {torch.cuda.get_device_name(0)}")
                total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**2
                logger.info(f"💾 Total GPU Memory: {total_memory:.0f}MB")

            # Initialize spaCy with CPU (works reliably)
            logger.info("💻 Initializing spaCy with CPU...")
            self.nlp = spacy.load("en_core_web_sm")

            logger.info("✅ Basic models initialized successfully")

        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            # Fallback to basic CPU processing
            self.nlp = spacy.load("en_core_web_sm") if self.nlp is None else self.nlp

    def analyze_conversation_simple(self, text: str, conversation_title: str = "") -> Dict[str, Any]:
        """Simplified conversation analysis with basic GPU utilization"""
        start_time = datetime.now()

        try:
            # Monitor GPU memory if available
            initial_memory = 0
            if self.is_gpu_available:
                initial_memory = torch.cuda.memory_allocated(0) / 1024**2
                logger.info(f"🔋 Starting analysis, GPU memory: {initial_memory:.0f}MB")

            results = {
                "title": conversation_title,
                "analysis_timestamp": start_time.isoformat(),
                "gpu_accelerated": self.is_gpu_available,
                "text_length": len(text),
                "processing_method": "gpu" if self.is_gpu_available else "cpu"
            }

            # 1. Basic NLP processing with spaCy
            logger.info("🔍 Processing with spaCy...")
            doc = self.nlp(text[:10000])  # Limit to 10k chars for memory safety

            # Extract entities
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            results["entities"] = entities[:20]  # Top 20 entities

            # Extract key phrases (noun phrases)
            noun_phrases = [chunk.text for chunk in doc.noun_chunks]
            results["key_phrases"] = noun_phrases[:15]  # Top 15 phrases

            # 2. Simple GPU-accelerated text processing
            if self.is_gpu_available:
                # Use GPU for simple tensor operations
                text_tensor = self._text_to_tensor(text[:1000])
                gpu_features = self._extract_gpu_features(text_tensor)
                results["gpu_features"] = gpu_features

            # 3. Decision extraction (pattern-based)
            decisions = self._extract_decisions_simple(text)
            results["decisions"] = decisions

            # 4. Action items extraction
            action_items = self._extract_action_items_simple(text)
            results["action_items"] = action_items

            # Performance metrics
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            results["processing_time_seconds"] = processing_time

            if self.is_gpu_available:
                final_memory = torch.cuda.memory_allocated(0) / 1024**2
                results["gpu_memory_used_mb"] = final_memory - initial_memory
                logger.info(f"⚡ Analysis complete in {processing_time:.2f}s, GPU memory delta: {final_memory - initial_memory:.0f}MB")
            else:
                logger.info(f"💻 CPU analysis complete in {processing_time:.2f}s")

            # Cleanup GPU memory
            if self.is_gpu_available:
                torch.cuda.empty_cache()
                gc.collect()

            return results

        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            if self.is_gpu_available:
                torch.cuda.empty_cache()
            return {
                "error": str(e),
                "analysis_timestamp": start_time.isoformat(),
                "gpu_accelerated": False
            }

    def _text_to_tensor(self, text: str) -> torch.Tensor:
        """Convert text to simple tensor for GPU processing"""
        # Simple character-level encoding
        char_indices = [ord(c) % 128 for c in text[:512]]  # Limit to 512 chars
        tensor = torch.tensor(char_indices, dtype=torch.float32)
        if self.is_gpu_available:
            tensor = tensor.to(self.device)
        return tensor

    def _extract_gpu_features(self, text_tensor: torch.Tensor) -> Dict[str, float]:
        """Extract simple features using GPU tensor operations"""
        try:
            # Simple statistical features using GPU
            features = {
                "mean_char_value": float(torch.mean(text_tensor)),
                "std_char_value": float(torch.std(text_tensor)),
                "max_char_value": float(torch.max(text_tensor)),
                "text_complexity": float(torch.std(text_tensor) / (torch.mean(text_tensor) + 1e-8))
            }
            return features
        except Exception as e:
            logger.warning(f"GPU feature extraction failed: {e}")
            return {}

    def _extract_decisions_simple(self, text: str) -> List[Dict[str, Any]]:
        """Simple decision extraction using spaCy"""
        decisions = []

        decision_patterns = [
            "decided to", "chose to", "will implement", "going with",
            "selected", "determined", "concluded", "opted for"
        ]

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        for i, sentence in enumerate(sentences):
            for pattern in decision_patterns:
                if pattern.lower() in sentence.lower():
                    decisions.append({
                        "decision_text": sentence.strip(),
                        "confidence": 0.8,
                        "position": i
                    })
                    break

        return decisions[:10]

    def _extract_action_items_simple(self, text: str) -> List[Dict[str, Any]]:
        """Simple action item extraction"""
        action_items = []

        action_patterns = [
            "need to", "should", "will", "must", "todo", "action",
            "implement", "create", "build", "setup", "configure"
        ]

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        for i, sentence in enumerate(sentences):
            for pattern in action_patterns:
                if pattern.lower() in sentence.lower():
                    if any(word in sentence.lower() for word in ["implement", "create", "setup", "install", "configure"]):
                        action_items.append({
                            "action_text": sentence.strip(),
                            "priority": "medium",
                            "confidence": 0.7,
                            "position": i
                        })
                        break

        return action_items[:15]

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        status = {
            "gpu_available": self.is_gpu_available,
            "timestamp": datetime.now().isoformat(),
            "analyzer_type": "simple_gpu"
        }

        if self.is_gpu_available:
            status.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "total_memory_mb": torch.cuda.get_device_properties(0).total_memory / 1024**2,
                "allocated_memory_mb": torch.cuda.memory_allocated(0) / 1024**2
            })

        return status

# Global analyzer instance
_simple_gpu_analyzer = None

def get_simple_gpu_analyzer() -> SimpleGPUAnalyzer:
    """Get or create the global simple GPU analyzer instance"""
    global _simple_gpu_analyzer
    if _simple_gpu_analyzer is None:
        logger.info("🚀 Initializing Simple GPU Enhanced Analyzer...")
        _simple_gpu_analyzer = SimpleGPUAnalyzer()
    return _simple_gpu_analyzer

def analyze_conversation_simple_gpu(text: str, title: str = "") -> Dict[str, Any]:
    """Main entry point for simple GPU-accelerated conversation analysis"""
    analyzer = get_simple_gpu_analyzer()
    return analyzer.analyze_conversation_simple(text, title)

def get_simple_analyzer_status() -> Dict[str, Any]:
    """Get current simple analyzer status"""
    analyzer = get_simple_gpu_analyzer()
    return analyzer.get_system_status()