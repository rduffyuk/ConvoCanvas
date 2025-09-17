"""
Feature flags for ConvoCanvas
Allows toggling experimental features without code changes
"""

import os
from typing import Dict, Any
from enum import Enum

class Features(Enum):
    """Available feature flags"""
    GPU_ACCELERATION = "gpu_acceleration"
    ENHANCED_ANALYSIS = "enhanced_analysis"
    CANVAS_GENERATION = "canvas_generation"
    LOCAL_AI_INTEGRATION = "local_ai_integration"
    NLP_PROCESSING = "nlp_processing"

class FeatureFlags:
    """
    Simple feature flag implementation
    Can be replaced with Unleash or LaunchDarkly later
    """

    def __init__(self):
        """Initialize feature flags from environment or config"""
        self.flags = {
            Features.GPU_ACCELERATION: self._check_gpu_available(),
            Features.ENHANCED_ANALYSIS: os.getenv("ENABLE_ENHANCED_ANALYSIS", "false").lower() == "true",
            Features.CANVAS_GENERATION: os.getenv("ENABLE_CANVAS_GENERATION", "true").lower() == "true",
            Features.LOCAL_AI_INTEGRATION: os.getenv("ENABLE_LOCAL_AI", "false").lower() == "true",
            Features.NLP_PROCESSING: os.getenv("ENABLE_NLP", "true").lower() == "true",
        }

    def _check_gpu_available(self) -> bool:
        """
        Check if GPU is available and should be enabled
        Requires NVIDIA GPU with 12GB+ VRAM
        """
        if os.getenv("DISABLE_GPU", "false").lower() == "true":
            return False

        try:
            import torch
            if torch.cuda.is_available():
                # Check VRAM (12GB minimum for high-end features)
                vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                return vram_gb >= 12.0
        except ImportError:
            pass

        return False

    def is_enabled(self, feature: Features) -> bool:
        """Check if a feature is enabled"""
        return self.flags.get(feature, False)

    def get_config(self) -> Dict[str, bool]:
        """Get all feature flag states"""
        return {
            feature.value: enabled
            for feature, enabled in self.flags.items()
        }

    def set_flag(self, feature: Features, enabled: bool):
        """Manually override a feature flag (for testing)"""
        self.flags[feature] = enabled

# Global instance
feature_flags = FeatureFlags()

def is_feature_enabled(feature: Features) -> bool:
    """Helper function to check feature status"""
    return feature_flags.is_enabled(feature)