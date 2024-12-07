"""
NeuroPrompt Evaluation Module
Copyright (c) 2024 Tejas Chopra. All rights reserved.

Extended functionality for prompt compression evaluation.
This module requires additional dependencies and is available
when installing with: pip install neuroprompt[eval]
"""

from .evaluator import NeuroPromptCompressWithEval

__version__ = "0.1.1"  # Keep in sync with core package
__author__ = "Tejas Chopra"
__email__ = "chopratejas@gmail.com"

__all__ = [
    "NeuroPromptCompressWithEval",
]

def is_eval_ready() -> bool:
    """Verify all evaluation dependencies are available."""
    try:
        import torch
        import numpy
        import rouge_score
        import transformers
        import sklearn
        return True
    except ImportError:
        return False