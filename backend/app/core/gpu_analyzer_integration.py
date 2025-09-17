"""
GPU-Enhanced Integration for ConvoCanvas
Extends existing EnhancedContentAnalyzer with GPU acceleration
"""

import logging
from typing import Dict, Any, Optional
from app.core.enhanced_content_analyzer import EnhancedContentAnalyzer
from app.core.simple_gpu_analyzer import analyze_conversation_simple_gpu, get_simple_analyzer_status

logger = logging.getLogger(__name__)

class GPUEnhancedContentAnalyzer(EnhancedContentAnalyzer):
    """
    GPU-accelerated version of the existing ConvoCanvas analyzer.
    Extends EnhancedContentAnalyzer with GPU processing while maintaining compatibility.
    """

    def __init__(self):
        """Initialize both CPU and GPU analyzers"""
        super().__init__()
        self.gpu_available = self._check_gpu_availability()
        logger.info(f"🚀 GPU Enhanced Analyzer initialized. GPU available: {self.gpu_available}")

    def _check_gpu_availability(self) -> bool:
        """Check if GPU acceleration is available"""
        try:
            status = get_simple_analyzer_status()
            return status.get('gpu_available', False)
        except Exception as e:
            logger.warning(f"GPU check failed: {e}")
            return False

    def extract_user_claude_dialogue(self, content: str) -> Dict[str, Any]:
        """
        GPU-enhanced dialogue extraction with original functionality.
        """
        try:
            if self.gpu_available:
                logger.info("🔥 Using GPU-accelerated dialogue analysis")

                # Get GPU analysis first
                gpu_result = analyze_conversation_simple_gpu(content, '')

                # Get original CPU analysis
                cpu_messages = super().extract_user_claude_dialogue(content)

                # Return enhanced messages with GPU insights
                enhanced_messages = {
                    'messages': cpu_messages,
                    'gpu_enhanced': True,
                    'gpu_processing_time': gpu_result.get('processing_time_seconds', 0),
                    'gpu_features': gpu_result.get('gpu_features', {}),
                    'gpu_entities': gpu_result.get('entities', []),
                    'gpu_key_phrases': gpu_result.get('key_phrases', []),
                    'processing_method': 'hybrid_gpu_cpu'
                }

                return enhanced_messages
            else:
                logger.info("💻 Using CPU-only dialogue extraction")
                messages = super().extract_user_claude_dialogue(content)
                return {'messages': messages, 'gpu_enhanced': False, 'processing_method': 'cpu_only'}

        except Exception as e:
            logger.error(f"❌ GPU analysis failed, falling back to CPU: {e}")
            messages = super().extract_user_claude_dialogue(content)
            return {
                'messages': messages,
                'gpu_enhanced': False,
                'processing_method': 'cpu_fallback',
                'gpu_error': str(e)
            }

    def extract_decisions(self, messages) -> Dict[str, Any]:
        """
        GPU-enhanced decision extraction.
        """
        # Handle both old format (list) and new format (dict with messages)
        if isinstance(messages, dict) and 'messages' in messages:
            message_list = messages['messages']
            gpu_enhanced = messages.get('gpu_enhanced', False)
        else:
            message_list = messages
            gpu_enhanced = False

        # Get CPU decisions
        cpu_decisions = super().extract_decisions(message_list)

        if gpu_enhanced and self.gpu_available:
            # Extract text for GPU analysis
            full_text = ' '.join([msg.get('content', '') for msg in message_list])
            gpu_result = analyze_conversation_simple_gpu(full_text, '')

            # Enhance decisions with GPU insights
            enhanced_decisions = {
                'decisions': cpu_decisions,
                'gpu_decisions': gpu_result.get('decisions', []),
                'gpu_action_items': gpu_result.get('action_items', []),
                'gpu_enhanced': True
            }
            return enhanced_decisions

        return {'decisions': cpu_decisions, 'gpu_enhanced': False}

    def _merge_analysis_results(self, gpu_result: Dict[str, Any], cpu_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge GPU and CPU analysis results, taking the best from both.
        """
        # Start with CPU result as base (comprehensive)
        merged = cpu_result.copy()

        # Overlay GPU-specific enhancements
        if 'processing_time_seconds' in gpu_result:
            merged['gpu_processing_time'] = gpu_result['processing_time_seconds']

        if 'gpu_features' in gpu_result:
            merged['gpu_features'] = gpu_result['gpu_features']

        if 'gpu_memory_used_mb' in gpu_result:
            merged['gpu_memory_used_mb'] = gpu_result['gpu_memory_used_mb']

        # Enhance entity extraction if GPU provided more
        if 'entities' in gpu_result and len(gpu_result['entities']) > len(merged.get('entities', [])):
            merged['entities_gpu'] = gpu_result['entities']

        # Enhance key phrases if GPU provided more
        if 'key_phrases' in gpu_result and len(gpu_result['key_phrases']) > len(merged.get('key_phrases', [])):
            merged['key_phrases_gpu'] = gpu_result['key_phrases']

        # Add GPU decisions and action items as additional data
        if 'decisions' in gpu_result:
            merged['decisions_gpu'] = gpu_result['decisions']

        if 'action_items' in gpu_result:
            merged['action_items_gpu'] = gpu_result['action_items']

        merged['analysis_timestamp'] = gpu_result.get('analysis_timestamp', merged.get('timestamp'))

        return merged

    def get_system_status(self) -> Dict[str, Any]:
        """Get enhanced system status including GPU information"""
        base_status = {
            'analyzer_type': 'gpu_enhanced',
            'gpu_available': self.gpu_available,
            'spacy_loaded': self.nlp is not None
        }

        if self.gpu_available:
            try:
                gpu_status = get_simple_analyzer_status()
                base_status.update(gpu_status)
            except Exception as e:
                base_status['gpu_error'] = str(e)

        return base_status

def get_gpu_enhanced_analyzer() -> GPUEnhancedContentAnalyzer:
    """Get or create the global GPU-enhanced analyzer instance"""
    global _gpu_enhanced_analyzer
    if '_gpu_enhanced_analyzer' not in globals():
        globals()['_gpu_enhanced_analyzer'] = GPUEnhancedContentAnalyzer()
    return globals()['_gpu_enhanced_analyzer']

# Compatibility function - can replace existing analyzer calls
def create_enhanced_analyzer() -> GPUEnhancedContentAnalyzer:
    """Create new GPU-enhanced analyzer (compatible with existing code)"""
    return GPUEnhancedContentAnalyzer()