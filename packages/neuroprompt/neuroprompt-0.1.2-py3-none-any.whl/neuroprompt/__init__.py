"""
NeuroPrompt - Intelligent Prompt Compression for LLMs
Copyright (c) 2024 Tejas Chopra. All rights reserved.

Core package providing basic prompt compression functionality.
For evaluation features, install with: pip install neuroprompt[eval]
"""

from .compressor import NeuroPromptCompress

__version__ = "0.1.2"
__author__ = "Tejas Chopra"
__email__ = "chopratejas@gmail.com"

# Core exports
__all__ = ["NeuroPromptCompress"]

# Check for eval support
try:
    from neuroprompt_eval import NeuroPromptCompressWithEval
    __all__.append("NeuroPromptCompressWithEval")
    HAS_EVAL = True
except ImportError:
    HAS_EVAL = False

def has_eval_support() -> bool:
    """Check if evaluation features are available."""
    return HAS_EVAL

def get_version() -> str:
    """Get the current version of NeuroPrompt."""
    return __version__