# NeuroPrompt

A smart prompt compression and optimization tool for Large Language Models that automatically adapts to different types of content and provides comprehensive quality evaluation.

## Installation

```bash
export OPENAI_API_KEY=<your_openai_key>
pip install neuroprompt
```

## Features

- Smart prompt compression with content-aware parameter optimization
- Support for various content types (code, lists, technical content)
- Comprehensive response quality evaluation
- Cost optimization for OpenAI API calls
- Automatic token counting and cost estimation

## Quick Start

```python
from neuroprompt import NeuroPromptCompress
from openai import OpenAI


@NeuroPromptCompress()
def chat_completion(messages, model="gpt-4o", temperature=0.7):
    client = OpenAI()
    return client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature
    )


# Example usage
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Your prompt here..."}
]

response = chat_completion(messages=messages)
```

## Documentation

### Basic Usage

The package provides two main decorators:

1. `NeuroPromptCompress`: Basic compression without evaluation
2. `NeuroPromptCompressWithEval`: Compression with comprehensive quality evaluation

### Quality Metrics

The evaluation includes:
- ROUGE scores
- BLEU score
- Semantic similarity
- Information coverage
- Expert evaluation using GPT-4o

## License

```
Copyright © 2024 Tejas Chopra.

All rights reserved.

This is proprietary software. Unauthorized copying, modification, distribution, or use of this software, in whole or in part, is strictly prohibited.
```

### Third Party Components

This software uses LLMLingua under MIT license. See the `LICENSE` file for full terms.
