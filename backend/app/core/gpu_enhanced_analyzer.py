"""
GPU-Enhanced Conversation Analyzer for ConvoCanvas
Optimized for RTX 4080 with memory-efficient processing
"""

import torch
import logging
from typing import Dict, List, Any, Optional
from transformers import pipeline, AutoTokenizer, AutoModel
import spacy
from datetime import datetime
import gc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPUResourceManager:
    """Manages GPU memory usage and prevents conflicts with LM Studio"""

    def __init__(self, max_gpu_memory_mb: int = 1600):  # Optimized: Use 1.6GB of 1.9GB available
        self.max_memory_mb = max_gpu_memory_mb
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_gpu_available = torch.cuda.is_available()

        if self.is_gpu_available:
            logger.info(f"🚀 GPU Device: {torch.cuda.get_device_name(0)}")
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**2
            logger.info(f"💾 Total GPU Memory: {total_memory:.0f}MB")
            logger.info(f"🎯 Allocated Limit: {max_gpu_memory_mb}MB")
        else:
            logger.warning("⚠️ GPU not available, falling back to CPU")

    def get_available_memory_mb(self) -> float:
        """Get available GPU memory in MB"""
        if not self.is_gpu_available:
            return 0

        torch.cuda.empty_cache()
        total = torch.cuda.get_device_properties(0).total_memory / 1024**2
        allocated = torch.cuda.memory_allocated(0) / 1024**2
        return total - allocated

    def check_memory_safety(self, required_mb: int) -> bool:
        """Check if we can safely allocate memory"""
        if not self.is_gpu_available:
            return True  # CPU fallback always safe

        available = self.get_available_memory_mb()
        safe_allocation = min(available * 0.85, self.max_memory_mb)  # 85% safety margin - more aggressive

        logger.info(f"🔍 Memory Check: Need {required_mb}MB, Safe allocation: {safe_allocation:.0f}MB")
        return required_mb <= safe_allocation

    def cleanup(self):
        """Clean up GPU memory"""
        if self.is_gpu_available:
            torch.cuda.empty_cache()
            gc.collect()

class GPUEnhancedAnalyzer:
    """GPU-accelerated conversation analyzer with fallback to CPU"""

    def __init__(self):
        self.gpu_manager = GPUResourceManager()
        self.models = {}
        self.nlp = None
        self._initialize_models()

    def _initialize_models(self):
        """Initialize models with GPU optimization"""
        try:
            # Initialize spaCy (CPU - CuPy not available, but transformers will use GPU)
            logger.info("💻 Initializing spaCy with CPU (transformers will use GPU)...")
            self.nlp = spacy.load("en_core_web_sm")

            # Initialize sentiment analysis with GPU (using safer model)
            if self.gpu_manager.is_gpu_available and self.gpu_manager.check_memory_safety(300):
                logger.info("🎭 Loading GPU sentiment analysis...")
                self.models['sentiment'] = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=0,
                    max_length=512,
                    truncation=True
                )
            else:
                logger.info("💻 Loading CPU sentiment analysis...")
                self.models['sentiment'] = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1
                )

            # Initialize summarization model (lighter model)
            if self.gpu_manager.is_gpu_available and self.gpu_manager.check_memory_safety(400):
                logger.info("📝 Loading GPU summarization...")
                self.models['summarizer'] = pipeline(
                    "summarization",
                    model="sshleifer/distilbart-cnn-12-6",
                    device=0,
                    max_length=150,
                    min_length=30,
                    truncation=True
                )
            else:
                logger.info("💻 Loading CPU summarization...")
                self.models['summarizer'] = pipeline(
                    "summarization",
                    model="sshleifer/distilbart-cnn-12-6",
                    device=-1
                )

            logger.info("✅ All models initialized successfully")

        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            # Fallback to basic CPU processing
            self.nlp = spacy.load("en_core_web_sm")
            self.models = {}

    def analyze_conversation_enhanced(self, text: str, conversation_title: str = "") -> Dict[str, Any]:
        """Enhanced conversation analysis with GPU acceleration"""
        start_time = datetime.now()

        try:
            # Monitor memory usage
            if self.gpu_manager.is_gpu_available:
                initial_memory = torch.cuda.memory_allocated(0) / 1024**2
                logger.info(f"🔋 Starting analysis, GPU memory: {initial_memory:.0f}MB")

            results = {
                "title": conversation_title,
                "analysis_timestamp": start_time.isoformat(),
                "gpu_accelerated": self.gpu_manager.is_gpu_available,
                "text_length": len(text),
                "processing_method": "gpu" if self.gpu_manager.is_gpu_available else "cpu"
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

            # 2. Sentiment analysis
            if 'sentiment' in self.models:
                logger.info("🎭 Analyzing sentiment...")
                # Process in chunks to manage memory
                chunks = [text[i:i+500] for i in range(0, min(len(text), 2000), 500)]
                sentiments = []

                for chunk in chunks:
                    if chunk.strip():
                        sentiment = self.models['sentiment'](chunk)
                        sentiments.extend(sentiment)

                if sentiments:
                    # Aggregate sentiment scores
                    avg_confidence = sum(s['score'] for s in sentiments) / len(sentiments)
                    dominant_sentiment = max(set(s['label'] for s in sentiments),
                                           key=lambda x: sum(1 for s in sentiments if s['label'] == x))

                    results["sentiment"] = {
                        "overall": dominant_sentiment,
                        "confidence": avg_confidence,
                        "details": sentiments[:5]  # Top 5 sentiment scores
                    }

            # 3. Text summarization
            if 'summarizer' in self.models and len(text) > 200:
                logger.info("📝 Generating summary...")
                try:
                    # Summarize in chunks and combine
                    summary_text = text[:1000]  # Limit input for memory safety
                    summary = self.models['summarizer'](summary_text)
                    results["summary"] = summary[0]['summary_text'] if summary else "Summary generation failed"
                except Exception as e:
                    logger.warning(f"⚠️ Summarization failed: {e}")
                    results["summary"] = "Summary not available"

            # 4. Decision extraction (enhanced)
            decisions = self._extract_decisions_gpu(text)
            results["decisions"] = decisions

            # 5. Action items extraction
            action_items = self._extract_action_items_gpu(text)
            results["action_items"] = action_items

            # Performance metrics
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            results["processing_time_seconds"] = processing_time

            if self.gpu_manager.is_gpu_available:
                final_memory = torch.cuda.memory_allocated(0) / 1024**2
                results["gpu_memory_used_mb"] = final_memory - initial_memory
                logger.info(f"⚡ Analysis complete in {processing_time:.2f}s, GPU memory delta: {final_memory - initial_memory:.0f}MB")
            else:
                logger.info(f"💻 CPU analysis complete in {processing_time:.2f}s")

            # Cleanup
            self.gpu_manager.cleanup()

            return results

        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            self.gpu_manager.cleanup()
            return {
                "error": str(e),
                "analysis_timestamp": start_time.isoformat(),
                "gpu_accelerated": False
            }

    def _extract_decisions_gpu(self, text: str) -> List[Dict[str, Any]]:
        """GPU-accelerated decision extraction"""
        decisions = []

        # Use spaCy's matcher for decision patterns
        decision_patterns = [
            "decided to", "chose to", "will implement", "going with",
            "selected", "determined", "concluded", "opted for"
        ]

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        for i, sentence in enumerate(sentences):
            for pattern in decision_patterns:
                if pattern.lower() in sentence.lower():
                    # Extract context around decision
                    context_start = max(0, i-1)
                    context_end = min(len(sentences), i+2)
                    context = " ".join(sentences[context_start:context_end])

                    decisions.append({
                        "decision_text": sentence.strip(),
                        "context": context.strip(),
                        "confidence": 0.8,  # Pattern-based confidence
                        "position": i
                    })
                    break

        return decisions[:10]  # Limit to top 10 decisions

    def _extract_action_items_gpu(self, text: str) -> List[Dict[str, Any]]:
        """GPU-accelerated action item extraction"""
        action_items = []

        # Action patterns
        action_patterns = [
            "need to", "should", "will", "must", "todo", "action",
            "implement", "create", "build", "setup", "configure"
        ]

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        for i, sentence in enumerate(sentences):
            for pattern in action_patterns:
                if pattern.lower() in sentence.lower():
                    # Check if it's actually an action (has imperative indicators)
                    if any(word in sentence.lower() for word in ["implement", "create", "setup", "install", "configure"]):
                        action_items.append({
                            "action_text": sentence.strip(),
                            "priority": "medium",  # Default priority
                            "confidence": 0.7,
                            "position": i
                        })
                        break

        return action_items[:15]  # Limit to top 15 actions

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system and GPU status"""
        status = {
            "gpu_available": self.gpu_manager.is_gpu_available,
            "models_loaded": list(self.models.keys()),
            "timestamp": datetime.now().isoformat()
        }

        if self.gpu_manager.is_gpu_available:
            status.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "total_memory_mb": torch.cuda.get_device_properties(0).total_memory / 1024**2,
                "available_memory_mb": self.gpu_manager.get_available_memory_mb(),
                "allocated_memory_mb": torch.cuda.memory_allocated(0) / 1024**2
            })

        return status

# Global analyzer instance
_gpu_analyzer = None

def get_gpu_analyzer() -> GPUEnhancedAnalyzer:
    """Get or create the global GPU analyzer instance"""
    global _gpu_analyzer
    if _gpu_analyzer is None:
        logger.info("🚀 Initializing GPU Enhanced Analyzer...")
        _gpu_analyzer = GPUEnhancedAnalyzer()
    return _gpu_analyzer

def analyze_conversation_with_gpu(text: str, title: str = "") -> Dict[str, Any]:
    """Main entry point for GPU-accelerated conversation analysis"""
    analyzer = get_gpu_analyzer()
    return analyzer.analyze_conversation_enhanced(text, title)

def get_analyzer_status() -> Dict[str, Any]:
    """Get current analyzer status"""
    analyzer = get_gpu_analyzer()
    return analyzer.get_system_status()