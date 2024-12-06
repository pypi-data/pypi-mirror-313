from llmlingua import PromptCompressor
import tiktoken
import re
from functools import wraps
import torch
from typing import Dict, Any, List
from openai import OpenAI
import numpy as np
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize
import nltk
from collections import defaultdict
import json


def analyze_text_structure(text: str) -> Dict[str, Any]:
    """
    Comprehensive text structure analysis for optimal compression.
    Returns a dictionary of metrics about the text structure.
    """
    sentences = nltk.sent_tokenize(text)
    words = text.split()

    # Basic structure metrics
    basic_metrics = {
        "num_sentences": len(sentences),
        "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
        "num_words": len(words),
        "paragraph_count": len(text.split('\n\n')),
        "has_long_sentences": any(len(s.split()) > 30 for s in sentences),
    }

    # Code detection patterns
    code_patterns = {
        # General code patterns
        "has_code_blocks": bool(re.search(r'```[\s\S]*?```', text)),
        "has_inline_code": bool(re.search(r'`[^`]+`', text)),

        # Language-specific patterns
        "has_python": bool(re.search(r'\b(?:def|class|import|from|return|if\s+__name__)\b', text)),
        "has_javascript": bool(re.search(r'\b(?:function|const|let|var|=>|async|await)\b', text)),
        "has_java": bool(re.search(r'\b(?:public|private|class|void|static)\b', text)),
        "has_cpp": bool(re.search(r'\b(?:include|namespace|template|cout|cin)\b', text)),
        "has_rust": bool(re.search(r'\b(?:fn|impl|struct|enum|mut|let)\b', text)),
        "has_go": bool(re.search(r'\b(?:func|package|import|defer|go|chan)\b', text)),

        # SQL patterns
        "has_sql": bool(re.search(r'\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|JOIN)\b', text, re.IGNORECASE)),
        "has_sql_functions": bool(
            re.search(r'\b(?:COUNT|SUM|AVG|MAX|MIN|GROUP BY|ORDER BY)\b', text, re.IGNORECASE)),

        # Shell/CLI patterns
        "has_shell_commands": bool(re.search(r'\b(?:sudo|apt|yum|brew|pip|npm|yarn)\b', text)),
        "has_git_commands": bool(re.search(r'\b(?:git|commit|push|pull|merge|branch)\b', text)),
    }

    # Technical content patterns
    technical_patterns = {
        # Data formats
        "has_json": bool(re.search(r'{\s*".+"\s*:', text) or re.search(r'Response Format.*{', text, re.DOTALL)),
        "has_yaml": bool(re.search(r'^\s*[\w-]+:\s*\w+', text, re.MULTILINE)),
        "has_xml": bool(re.search(r'<[\w-]+[^>]*>[^<]*</[\w-]+>', text)),

        # Configuration patterns
        "has_env_vars": bool(re.search(r'\b[A-Z_]+=[^\s]+', text)),
        "has_config_settings": bool(
            re.search(r'(?:config|configuration|settings)\.(?:json|yaml|yml|xml|ini)\b', text, re.IGNORECASE)),

        # API/Protocol patterns
        "has_api_endpoints": bool(re.search(r'/api/v\d+/|/v\d+/[\w-]+/', text)),
        "has_http_methods": bool(re.search(r'\b(?:GET|POST|PUT|DELETE|PATCH)\b', text)),
        "has_status_codes": bool(re.search(r'\b[1-5][0-9]{2}\b', text)),

        # Infrastructure/DevOps
        "has_docker": bool(re.search(r'\b(?:docker|container|image|volume|dockerfile)\b', text, re.IGNORECASE)),
        "has_kubernetes": bool(re.search(r'\b(?:kubectl|pod|deployment|service|namespace)\b', text, re.IGNORECASE)),
        "has_cloud": bool(re.search(r'\b(?:aws|azure|gcp|s3|ec2|lambda)\b', text, re.IGNORECASE))
    }

    # Documentation patterns
    doc_patterns = {
        # Format markers
        "has_json_schema": bool(re.search(r'Format.*response.*{', text, re.IGNORECASE | re.DOTALL)),
        "has_markdown": bool(re.search(r'(?:\*\*|__|##|>\s|\[.*\]\(.*\))', text)),
        "has_jsdoc": bool(re.search(r'/\*\*[\s\S]*?\*/', text)),

        # Documentation elements
        "has_examples": bool(re.search(r'\b(?:example|e\.g\.|i\.e\.|sample)\b', text, re.IGNORECASE)),
        "has_parameters": bool(re.search(r'\b(?:parameter|param|argument|arg)\b', text, re.IGNORECASE)),
        "has_returns": bool(re.search(r'\b(?:returns?|output)\b:', text, re.IGNORECASE))
    }

    # Data content patterns
    data_patterns = {
        # Numbers and units
        "has_numbers": bool(re.search(r'\d', text)),
        "has_decimals": bool(re.search(r'\d+\.\d+', text)),
        "has_percentages": bool(re.search(r'\d+%', text)),
        "has_scientific": bool(re.search(r'\d+e[+-]\d+', text)),

        # Units and measurements
        "has_time_units": bool(re.search(r'\b\d+\s*(?:ms|s|min|h|day|month|year)s?\b', text, re.IGNORECASE)),
        "has_size_units": bool(re.search(r'\b\d+\s*(?:b|kb|mb|gb|tb)\b', text, re.IGNORECASE)),
        "has_currency": bool(re.search(r'(?:\$|€|£)\d+', text)),

        # Data structures
        "has_lists": bool(re.search(r'^\s*[-*•]\s|^\s*\d+\.\s', text, re.MULTILINE)),
        "has_tables": bool(re.search(r'\|.*\|.*\|', text)),
        "json_depth": len(re.findall(r'{', text))
    }

    # URL and web patterns
    url_patterns = {
        # URLs and domains
        "has_urls": bool(
            re.search(r'(?:https?:\/\/)?(?:[\w-]+\.)+[\w-]+(?:\/[\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?', text)),
        "has_domains": bool(re.search(r'\b(?:www\.)?(?:[\w-]+\.)+(?:com|org|net|io|ai|edu|gov)\b', text)),
        "has_emails": bool(re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)),
        "has_ip_addresses": bool(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text)),

        # Web technologies
        "has_html": bool(re.search(r'<[^>]+>', text)),
        "has_css": bool(re.search(r'[.#][a-zA-Z-]+\s*{[^}]*}', text)),
        "has_js_code": bool(re.search(r'\b(?:function|const|let|var|=>)\b', text))
    }

    # Combine all metrics
    metrics = {
        **basic_metrics,
        **code_patterns,
        **technical_patterns,
        **doc_patterns,
        **data_patterns,
        **url_patterns,
    }

    # Extract specific items for preservation
    if metrics["has_urls"]:
        metrics["url_list"] = re.findall(
            r'(?:https?:\/\/)?(?:[\w-]+\.)+[\w-]+(?:\/[\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?', text)

    if metrics["has_api_endpoints"]:
        metrics["api_endpoints"] = re.findall(r'/api/v\d+/[\w-]+/?(?:[\w-]+/?)*', text)

    return metrics


class NeuroPromptCompress:
    def __init__(self):

        # Calculate maximum possible force tokens based on your patterns
        max_force_tokens = 500  # Increased to handle our comprehensive token preservation

        # Configure LLMLingua2
        llmlingua2_config = {
            "max_batch_size": 50,  # Default batch size for processing
            "max_force_token": max_force_tokens,  # Maximum number of tokens that can be forcefully preserved
        }

        """Initialize the PromptixCompress with smart defaults"""
        self.compressor = PromptCompressor(
            model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
            device_map="cuda" if torch.cuda.is_available() else "cpu",
            use_llmlingua2=True,
            llmlingua2_config=llmlingua2_config
        )

        # Initialize tokenizers for different models
        self.tokenizers = {
            "gpt-4o": tiktoken.encoding_for_model("gpt-4o"),
            "gpt-4": tiktoken.encoding_for_model("gpt-4"),
            "gpt-3.5": tiktoken.encoding_for_model("gpt-3.5"),
            "gpt-3.5-turbo": tiktoken.encoding_for_model("gpt-3.5-turbo"),
        }

        # Cost per 1K tokens for different models (input prices)
        self.token_costs = {
            "gpt-4o": 0.0025,
            "gpt-4": 0.03,
            "gpt-3.5": 0.003,
            "gpt-3.5-turbo": 0.003,
        }

        # Initialize NLTK
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def get_optimal_parameters(self, messages: List[dict], model: str) -> Dict[str, Any]:
        """
        Get optimal compression parameters based on comprehensive content analysis.
        Returns a dictionary of compression parameters.
        """
        combined_text = " ".join([m.get("content", "") for m in messages if m.get("content")])
        metrics = analyze_text_structure(combined_text)
        token_count = len(self.tokenizers[model].encode(combined_text))

        # Base parameters
        params = {
            "use_sentence_level_filter": True,
            "use_context_level_filter": True,
            "use_token_level_filter": True,
            "keep_split": False,
            "force_reserve_digit": True,
            "drop_consecutive": False,
            "token_to_word": "mean",
            "force_tokens": set()  # Using set to avoid duplicates
        }

        # Base compression rate based on token count
        if token_count < 500:
            params["compression_rate"] = 0.7  # Very light compression
        elif token_count < 1000:
            params["compression_rate"] = 0.6  # Moderate compression
        else:
            params["compression_rate"] = 0.5  # Heavy compression

        # Code-specific optimizations
        if any([metrics[key] for key in metrics if key.startswith("has_") and "code" in key]):
            params["compression_rate"] = min(0.95, params["compression_rate"] * 1.2)
            params["keep_split"] = True

            # Language-specific tokens
            if metrics["has_python"]:
                params["force_tokens"].update([
                    "def", "class", "import", "from", "return", "if", "__name__", "__main__",
                    "self", "None", "True", "False", "try", "except", "finally", "raise",
                    "async", "await", "with", "as", "lambda"
                ])

            if metrics["has_javascript"]:
                params["force_tokens"].update([
                    "function", "const", "let", "var", "=>", "async", "await", "import",
                    "export", "default", "class", "extends", "null", "undefined"
                ])

            if metrics["has_java"]:
                params["force_tokens"].update([
                    "public", "private", "protected", "class", "interface", "extends",
                    "implements", "static", "final", "void", "new", "this", "super"
                ])

        # SQL preservation
        if metrics["has_sql"] or metrics["has_sql_functions"]:
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.3)
            params["force_tokens"].update([
                "SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "OUTER",
                "GROUP BY", "ORDER BY", "HAVING", "COUNT", "SUM", "AVG", "MIN", "MAX",
                "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TABLE", "INDEX"
            ])

        # Data format preservation
        if any([metrics["has_json"], metrics["has_yaml"], metrics["has_xml"]]):
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.3)
            params["keep_split"] = True
            params["force_tokens"].update([
                "{", "}", "[", "]", ":", ",", '"', "'", "<", ">", "/",
                "type", "properties", "required", "items", "ref", "definitions"
            ])

        # API and protocol preservation
        if metrics["has_api_endpoints"] or metrics["has_http_methods"]:
            params["force_tokens"].update([
                "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS",
                "api", "v1", "v2", "v3", "endpoint", "request", "response",
                "200", "201", "204", "400", "401", "403", "404", "500"
            ])
            if "api_endpoints" in metrics:
                params["force_tokens"].update(metrics["api_endpoints"])

        # Infrastructure and DevOps terms
        if any([metrics["has_docker"], metrics["has_kubernetes"], metrics["has_cloud"]]):
            params["force_tokens"].update([
                "docker", "container", "image", "volume", "kubernetes", "pod", "deployment",
                "service", "namespace", "aws", "azure", "gcp", "lambda", "function"
            ])

        # URL and web content preservation
        if any([metrics["has_urls"], metrics["has_domains"], metrics["has_emails"]]):
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.2)
            params["force_tokens"].update([
                "http", "https", "www", "://", ".com", ".org", ".net", ".io",
                "@", "/", "_", "-", "#", "?", "&", "=", "api", "endpoint"
            ])
            if "url_list" in metrics:
                for url in metrics["url_list"]:
                    params["force_tokens"].update(re.split(r'[/:#?]', url))

        # Numbers and units preservation
        if any([metrics["has_numbers"], metrics["has_decimals"], metrics["has_percentages"]]):
            params["force_reserve_digit"] = True
            params["force_tokens"].update([
                "ms", "s", "min", "hr", "day", "week", "month", "year",
                "b", "kb", "mb", "gb", "tb", "%", "$", "€", "£"
            ])

        # Documentation elements
        if any([metrics["has_markdown"], metrics["has_jsdoc"], metrics["has_examples"]]):
            params["force_tokens"].update([
                "#", "##", "###", "**", "__", ">", "-", "*", "[", "]", "(",
                ")", "```", "example", "param", "return", "throws"
            ])

        # Shell and CLI commands
        if metrics["has_shell_commands"] or metrics["has_git_commands"]:
            params["force_tokens"].update([
                "sudo", "apt", "yum", "brew", "pip", "npm", "yarn",
                "install", "update", "remove", "git", "commit", "push",
                "pull", "merge", "branch", "checkout", "clone", "fetch"
            ])
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.2)

        # List and structured content preservation
        if metrics["has_lists"] or metrics["has_tables"]:
            params["keep_split"] = True
            params["force_tokens"].update([
                "-", "*", "•", "1.", "2.", "3.", "a.", "b.", "c.",
                "|", "+-", "-+", "+", "table", "header", "row"
            ])

        # Configuration and environment variables
        if metrics["has_env_vars"] or metrics["has_config_settings"]:
            params["force_tokens"].update([
                "config", "settings", "env", "environment", "production",
                "development", "staging", "test", "debug", "=", "export"
            ])
            params["compression_rate"] = min(0.95, params["compression_rate"] * 1.15)

        # Special handling for very technical content
        technical_indicator_count = sum(1 for k, v in metrics.items()
                                        if k.startswith('has_') and v is True)
        if technical_indicator_count > 5:
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.25)
            params["use_sentence_level_filter"] = False  # Disable sentence filtering for highly technical content

        # Special handling for documentation-heavy content
        doc_indicators = ['has_examples', 'has_parameters', 'has_returns', 'has_markdown']
        if sum(1 for ind in doc_indicators if metrics.get(ind, False)) >= 2:
            params["keep_split"] = True
            params["compression_rate"] = min(0.95, params["compression_rate"] * 1.15)

        # Preserve indentation and formatting for code blocks
        if any([metrics["has_code_blocks"], metrics["has_python"], metrics["has_javascript"]]):
            params["keep_split"] = True
            params["force_tokens"].update([
                "    ",  # 4-space indentation
                "\t",  # tab indentation
                "=>",  # arrow functions
                "->",  # Python return type hints
                ";",  # statement terminator
            ])

        # Handle long sentences differently
        if metrics["has_long_sentences"]:
            params["use_sentence_level_filter"] = True
            params["compression_rate"] *= 0.9  # More aggressive compression for long sentences

        # Special consideration for high JSON nesting
        if metrics["json_depth"] > 3:
            params["keep_split"] = True
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.2)

        # Final adjustments based on content complexity
        total_metrics = sum(1 for v in metrics.values() if isinstance(v, bool) and v)
        if total_metrics > 10:  # Highly complex content
            params["compression_rate"] = min(0.98, params["compression_rate"] * 1.3)
            params["use_context_level_filter"] = True
            params["keep_split"] = True

        # Convert force_tokens from set to list and clean up
        params["force_tokens"] = list(params["force_tokens"])
        # Remove empty strings and None values
        params["force_tokens"] = [t for t in params["force_tokens"] if t and t.strip()]
        # Remove duplicates while preserving order
        params["force_tokens"] = list(dict.fromkeys(params["force_tokens"]))

        # Final validation of compression rate
        params["compression_rate"] = max(min(params["compression_rate"], 1.0), 0.4)

        return params

    def compress_messages(self, messages: List[dict], model: str, params: Dict[str, Any]) -> List[dict]:
        """Enhanced message compression with structure preservation."""
        compressed_messages = []

        for message in messages:
            if "content" in message and message["content"]:
                # Split content into instruction/context/question
                content = message["content"]

                # Preserve JSON response format blocks
                json_formats = re.findall(r'Response Format.*?{.*?}', content, re.DOTALL | re.IGNORECASE)
                placeholders = {f"__JSON_FORMAT_{i}__": fmt for i, fmt in enumerate(json_formats)}

                for placeholder, fmt in placeholders.items():
                    content = content.replace(fmt, placeholder)

                # Compress the modified content
                compressed_result = self.compressor.compress_prompt(
                    context=[content],
                    rate=params["compression_rate"],
                    use_sentence_level_filter=params["use_sentence_level_filter"],
                    use_context_level_filter=params["use_context_level_filter"],
                    use_token_level_filter=params["use_token_level_filter"],
                    keep_split=params["keep_split"],
                    force_reserve_digit=params["force_reserve_digit"],
                    drop_consecutive=params["drop_consecutive"],
                    token_to_word=params["token_to_word"],
                    force_tokens=params.get("force_tokens", [])
                )

                # Restore JSON formats
                compressed_content = compressed_result["compressed_prompt"]
                for placeholder, fmt in placeholders.items():
                    compressed_content = compressed_content.replace(placeholder, fmt)

                compressed_message = message.copy()
                compressed_message["content"] = compressed_content
                compressed_messages.append(compressed_message)
            else:
                compressed_messages.append(message)

        return compressed_messages

    def calculate_token_metrics(self, messages: List[dict], model: str) -> Dict[str, Any]:
        """Calculate token metrics for messages."""
        tokenizer = self.tokenizers.get(model, self.tokenizers["gpt-4"])
        total_tokens = 0

        for message in messages:
            if "content" in message and message["content"]:
                total_tokens += len(tokenizer.encode(message["content"]))
                total_tokens += 4  # Format tokens per message

        total_tokens += 2  # Conversation format tokens
        cost = (total_tokens / 1000) * self.token_costs.get(model, self.token_costs["gpt-4"])

        return {
            "total_tokens": total_tokens,
            "cost": cost
        }

    def compress_prompt(self, func_args: tuple, func_kwargs: dict) -> tuple:
        """Main compression function."""
        messages = None
        args_list = list(func_args)
        model = func_kwargs.get("model", "gpt-4")

        # Extract messages from args or kwargs
        if "messages" in func_kwargs:
            messages = func_kwargs["messages"]
        elif len(func_args) > 0 and isinstance(func_args[0], list):
            messages = func_args[0]

        if not messages:
            return func_args, func_kwargs

        # Calculate original metrics
        original_metrics = self.calculate_token_metrics(messages, model)

        # Get optimal parameters based on content analysis
        optimal_params = self.get_optimal_parameters(messages, model)

        # Compress messages
        compressed_messages = self.compress_messages(messages, model, optimal_params)

        # Calculate compressed metrics
        compressed_metrics = self.calculate_token_metrics(compressed_messages, model)

        # Print metrics
        print("\nNeuroPrompt Compression Metrics:")
        print(f"Original Tokens: {original_metrics['total_tokens']:,}")
        print(f"Compressed Tokens: {compressed_metrics['total_tokens']:,}")
        print(f"Compression Ratio: {compressed_metrics['total_tokens'] / original_metrics['total_tokens']:.2%}")
        print(f"Cost Savings: ${(original_metrics['cost'] - compressed_metrics['cost']):.4f}")

        # Update args or kwargs
        if "messages" in func_kwargs:
            func_kwargs["messages"] = compressed_messages
        else:
            args_list[0] = compressed_messages

        return tuple(args_list), func_kwargs

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            modified_args, modified_kwargs = self.compress_prompt(args, kwargs)
            return func(*modified_args, **modified_kwargs)

        return wrapper


class ResponseEvaluator:
    def __init__(self):
        """Initialize the evaluator with necessary NLTK downloads"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')

        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.client = OpenAI()  # Assumes OPENAI_API_KEY is set in environment

    def calculate_semantic_similarity(self, original_response: str, compressed_response: str) -> float:
        """Calculate semantic similarity using OpenAI embeddings."""
        try:
            original_embedding = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=original_response
            ).data[0].embedding

            compressed_embedding = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=compressed_response
            ).data[0].embedding

            # Calculate cosine similarity
            similarity = np.dot(original_embedding, compressed_embedding) / (
                    np.linalg.norm(original_embedding) * np.linalg.norm(compressed_embedding)
            )
            return float(similarity)
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.0

    def evaluate_responses(
            self,
            original_response: str,
            compressed_response: str,
            prompt_context: str
    ) -> Dict[str, Any]:
        """Evaluate the quality of compressed response compared to original response."""

        # 1. Calculate ROUGE scores
        rouge_scores = self.rouge_scorer.score(original_response, compressed_response)

        # 2. Calculate BLEU score
        original_tokens = word_tokenize(original_response)
        compressed_tokens = word_tokenize(compressed_response)
        bleu_score = sentence_bleu([original_tokens], compressed_tokens)

        # 3. Calculate semantic similarity
        semantic_similarity = self.calculate_semantic_similarity(
            original_response, compressed_response
        )

        # 4. Information coverage analysis
        original_info = self.extract_key_information(original_response)
        compressed_info = self.extract_key_information(compressed_response)
        coverage_score = self.calculate_coverage(original_info, compressed_info)

        # 5. Use GPT-4 for qualitative evaluation
        expert_evaluation = self.get_expert_evaluation(
            original_response, compressed_response, prompt_context
        )

        return {
            "rouge_scores": {
                "rouge1": rouge_scores['rouge1'].fmeasure,
                "rouge2": rouge_scores['rouge2'].fmeasure,
                "rougeL": rouge_scores['rougeL'].fmeasure
            },
            "bleu_score": bleu_score,
            "semantic_similarity": semantic_similarity,
            "information_coverage": coverage_score,
            "expert_evaluation": expert_evaluation
        }

    def extract_key_information(self, text: str) -> Dict[str, List[str]]:
        """Extract key information elements from text."""
        # Tokenize and tag parts of speech
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)

        info = defaultdict(list)

        # Extract named entities, numbers, and key terms
        for word, tag in tagged:
            if tag.startswith('NN'):  # Nouns
                info['nouns'].append(word)
            elif tag.startswith('VB'):  # Verbs
                info['verbs'].append(word)
            elif tag.startswith('CD'):  # Numbers
                info['numbers'].append(word)
            elif tag in ['JJ', 'JJR', 'JJS']:  # Adjectives
                info['adjectives'].append(word)

        return dict(info)

    def calculate_coverage(
            self,
            original_info: Dict[str, List[str]],
            compressed_info: Dict[str, List[str]]
    ) -> float:
        """Calculate information coverage score."""
        total_matches = 0
        total_items = 0

        for key in original_info:
            if key in compressed_info:
                matches = len(set(original_info[key]) & set(compressed_info[key]))
                total_matches += matches
                total_items += len(original_info[key])

        return total_matches / total_items if total_items > 0 else 0.0

    def get_expert_evaluation(
            self,
            original_response: str,
            compressed_response: str,
            prompt_context: str
    ) -> Dict[str, Any]:
        """Use GPT-4 to evaluate response quality."""
        evaluation_prompt = f"""
        Please evaluate the following two responses to a prompt. Score each aspect from 1-10 and provide brief reasoning.

        Original Prompt Context: {prompt_context}

        Original Response: {original_response}

        Compressed Response: {compressed_response}

        Please evaluate and score the following aspects of the compressed response compared to the original:
        1. Accuracy (How accurate is the information?)
        2. Completeness (How complete is the response?)
        3. Relevance (How relevant is the response to the prompt?)
        4. Coherence (How well-structured and coherent is the response?)

        Provide your evaluation ONLY IN JSON format with scores and brief explanations. Remove all markdown.
        JUST RETURN JSON such that it can work with json.loads()
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "You are an expert evaluator. Provide concise, objective evaluations."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.3
            )
            # Parse the JSON response
            evaluation = json.loads(response.choices[0].message.content)
            return evaluation

        except Exception as e:
            print(f"Error in expert evaluation: {e}")
            return {
                "error": "Failed to get expert evaluation",
                "details": str(e)
            }


class NeuroPromptCompressWithEval(NeuroPromptCompress):
    def __init__(self):
        super().__init__()
        self.evaluator = ResponseEvaluator()
        self.evaluation_results = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get original response
            original_response = func(*args, **kwargs)

            # Get compressed response
            modified_args, modified_kwargs = self.compress_prompt(args, kwargs)
            compressed_response = func(*modified_args, **modified_kwargs)

            # Get prompt context
            messages = kwargs.get('messages', args[0] if args else None)
            prompt_context = messages[-1]['content'] if messages else ""

            # Evaluate responses
            evaluation = self.evaluator.evaluate_responses(
                original_response.choices[0].message.content,
                compressed_response.choices[0].message.content,
                prompt_context
            )

            # Store evaluation results
            self.evaluation_results.append({
                'prompt_context': prompt_context,
                'original_response': original_response.choices[0].message.content,
                'compressed_response': compressed_response.choices[0].message.content,
                'evaluation': evaluation
            })

            # Print evaluation summary
            print("\nResponse Quality Metrics:")
            print(f"ROUGE-1 Score: {evaluation['rouge_scores']['rouge1']:.3f}")
            print(f"ROUGE-2 Score: {evaluation['rouge_scores']['rouge2']:.3f}")
            print(f"ROUGE-L Score: {evaluation['rouge_scores']['rougeL']:.3f}")
            print(f"BLEU Score: {evaluation['bleu_score']:.3f}")
            print(f"Semantic Similarity: {evaluation['semantic_similarity']:.3f}")
            print(f"Information Coverage: {evaluation['information_coverage']:.3f}")
            print("\nExpert Evaluation:")
            for key, value in evaluation['expert_evaluation'].items():
                print(f"{key}: {value}")

            return compressed_response

        return wrapper
