from openai import OpenAI
import numpy as np
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize
import nltk
from collections import defaultdict
import json
from typing import Dict, Any, List
from ..neuroprompt.compressor import NeuroPromptCompress

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
