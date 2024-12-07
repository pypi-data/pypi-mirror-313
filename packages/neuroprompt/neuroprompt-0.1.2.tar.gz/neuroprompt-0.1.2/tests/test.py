from neuroprompt.compressor import NeuroPromptCompressWithEval, NeuroPromptCompress
from typing import Dict, Any
from openai import OpenAI


# Example usage
@NeuroPromptCompressWithEval()
def chat_completion_eval(
        messages: list,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        **kwargs
) -> Dict[str, Any]:
    """Send a chat completion request to OpenAI with compressed prompts."""
    client = OpenAI()
    return client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        **kwargs
    )


# Example usage
@NeuroPromptCompress()
def chat_completion(
        messages: list,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        **kwargs
) -> Dict[str, Any]:
    """Send a chat completion request to OpenAI with compressed prompts."""
    client = OpenAI()
    return client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        **kwargs
    )


def main():
    # Example 1: Long Text Content
    messages_long_text = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": """
        Please analyze this lengthy text about climate change:

        Climate change is one of the most pressing challenges facing our world today. 
        The Intergovernmental Panel on Climate Change (IPCC) has repeatedly warned that 
        we need to take immediate action to reduce greenhouse gas emissions. The primary 
        drivers of climate change include burning fossil fuels, deforestation, and 
        industrial processes. These activities release carbon dioxide, methane, and other 
        greenhouse gases into the atmosphere, trapping heat and causing global temperatures 
        to rise. This has led to various consequences including rising sea levels, more 
        frequent extreme weather events, and disruption of ecosystems. Scientists have 
        observed that the rate of warming has accelerated in recent decades, with the 
        last seven years being the warmest on record. This trend has serious implications 
        for agriculture, water resources, human health, and biodiversity. Many species 
        are at risk of extinction as their habitats change faster than they can adapt.

        Can you summarize the key points and suggest some solutions?
        """}
    ]

    # Example 2: Code Content
    messages_code = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": """
        Can you help me understand and optimize this Python code?

        ```python
        def calculate_fibonacci(n):
            if n <= 0:
                return []
            elif n == 1:
                return [0]

            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            return fib

        # Example usage
        result = calculate_fibonacci(10)
        print(f"First 10 Fibonacci numbers: {result}")
        ```

        What improvements would you suggest?
        """}
    ]

    # Example 3: List Content
    messages_list = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": """
        Here are the top priorities for our project:

        1. Complete user authentication system
           * Implement OAuth 2.0
           * Add password reset functionality
           * Set up email verification

        2. Database optimization
           * Index frequently accessed columns
           * Implement query caching
           * Set up database replication

        3. Frontend improvements
           - Update UI components
           - Implement responsive design
           - Add dark mode support

        Can you help me create a timeline for these tasks?
        """}
    ]

    # Example 4: Content with URLs and Technical Information
    messages_technical = [
        {"role": "system", "content": "You are a helpful technical assistant."},
        {"role": "user", "content": """
        I'm researching machine learning frameworks. Here are some resources I found:

        TensorFlow (https://www.tensorflow.org) offers comprehensive tools and has a 
        market share of 35.8%. PyTorch (https://pytorch.org) is growing rapidly, with 
        version 2.0 introducing significant improvements. The framework achieved a 
        48.3% performance boost for CNN inference.

        In our benchmarks:
        - Model A: 89.7% accuracy, 250ms inference time
        - Model B: 92.3% accuracy, 180ms inference time
        - Model C: 87.5% accuracy, 150ms inference time

        Which framework would you recommend for our computer vision project?
        """}
    ]

    print("\n=== Example 1: Long Text Content ===")
    response = chat_completion_eval(messages=messages_long_text, model="gpt-4o")

    print("\n=== Example 2: Code Content ===")
    response = chat_completion_eval(messages=messages_code, model="gpt-4o")

    print("\n=== Example 3: List Content ===")
    response = chat_completion_eval(messages=messages_list, model="gpt-4o")

    print("\n=== Example 4: Technical Content ===")
    response = chat_completion_eval(messages=messages_technical, model="gpt-4o")


def test_complex_prompts():
    # Example 1: Complex Multi-task Prompt with JSON Response Format
    messages_complex = [
        {"role": "system", "content": "You are an AI expert in data analysis and business strategy."},
        {"role": "user", "content": """
        Analyze the following business metrics and provide recommendations in JSON format.

        Q4 2023 Performance Metrics:
        - Revenue: $12.4M (↑8% YoY)
        - Customer Acquisition Cost: $342 (↓5% QoQ)
        - Churn Rate: 2.8% (↑0.3% QoQ)
        - NPS Score: 48 (↓2 points)
        - Feature Adoption: 73% (↑5% QoQ)

        Response Format Requirements:
        {
            "key_insights": ["array of 3-4 critical insights"],
            "risk_factors": {
                "high_priority": ["list"],
                "medium_priority": ["list"]
            },
            "recommendations": {
                "immediate_actions": ["list"],
                "long_term_strategy": ["list"]
            },
            "projected_impact": {
                "revenue": "string",
                "customer_retention": "string",
                "market_position": "string"
            }
        }
        """}
    ]

    # Example 2: Highly Condensed Technical Prompt
    messages_condensed = [
        {"role": "system", "content": "You are a systems architecture expert."},
        {"role": "user", "content": """
        Arch:k8s+istio;30svcs;5DC;mult-cloud;DR-active/active;RPO=0;RTO<1m. 
        Issue:p99lat>2s;CPU=85%;MEM=90%;net-split-2x/w;
        Req:opt+scale+resilience;cost-eff;24/7.

        Format response as:
        {
            "root_causes": [],
            "solutions": [],
            "architecture_changes": [],
            "cost_impact": {"capex": "", "opex": ""}
        }
        """}
    ]

    # Example 3: Nested JSON Analysis
    messages_json = [
        {"role": "system", "content": "You are a data structure optimization expert."},
        {"role": "user", "content": """
        Analyze this JSON structure and suggest optimizations:

        {
            "userProfile": {
                "basicInfo": {
                    "id": "u123",
                    "name": {"first": "John", "last": "Doe"},
                    "email": "john@example.com",
                    "preferences": {
                        "notifications": {
                            "email": {"marketing": true, "updates": false},
                            "push": {"marketing": false, "updates": true}
                        }
                    }
                },
                "subscriptions": [
                    {
                        "planId": "pro",
                        "status": "active",
                        "billingCycle": {"interval": "month", "count": 1},
                        "features": ["feature1", "feature2"],
                        "usage": {
                            "apiCalls": {"current": 1500, "limit": 2000},
                            "storage": {"current": 15, "limit": 20, "unit": "GB"}
                        }
                    }
                ]
            }
        }

        Response Format:
        {
            "structure_analysis": {
                "depth": "int",
                "redundancy_points": ["list"],
                "performance_impacts": ["list"]
            },
            "optimization_suggestions": {
                "schema_changes": ["list"],
                "denormalization_opportunities": ["list"],
                "indexing_recommendations": ["list"]
            },
            "migration_strategy": {
                "steps": ["list"],
                "risks": ["list"],
                "estimated_effort": "string"
            }
        }
        """}
    ]

    # Example 4: Multi-modal Context with Complex Requirements
    messages_multimodal = [
        {"role": "system", "content": "You are a multi-domain expert in ML, UX, and business strategy."},
        {"role": "user", "content": """
        Context: E-commerce platform migration + ML integration

        Technical Stack:
        - BE: Node.js/Express → Python/FastAPI
        - FE: React/Redux → Next.js/React Query
        - ML: TensorFlow.js → PyTorch
        - DB: MongoDB → PostgreSQL+Redis

        Critical Requirements:
        1. Zero-downtime migration
        2. Real-time product recommendations
        3. A/B testing infrastructure
        4. GDPR/CCPA compliance
        5. <200ms p95 latency

        Budget: $400K
        Timeline: 4 months
        Team: 8 devs, 2 ML, 1 DevOps

        Respond in JSON:
        {
            "architecture_decisions": {
                "infrastructure": ["list"],
                "data_layer": ["list"],
                "ml_pipeline": ["list"]
            },
            "migration_phases": [{
                "phase": "string",
                "duration": "string",
                "team_allocation": {},
                "risks": ["list"]
            }],
            "success_metrics": {
                "technical": ["list"],
                "business": ["list"]
            },
            "contingency_plans": ["list"]
        }
        """}
    ]

    # Run tests with different models to compare performance
    models = ["gpt-4"]

    for model in models:
        print(f"\n=== Testing with {model} ===")

        print("\n=== Complex Multi-task Analysis ===")
        response = chat_completion_eval(messages=messages_complex, model=model)

        print("\n=== Condensed Technical Analysis ===")
        response = chat_completion_eval(messages=messages_condensed, model=model)

        print("\n=== JSON Structure Analysis ===")
        response = chat_completion_eval(messages=messages_json, model=model)

        print("\n=== Multi-modal Context Analysis ===")
        response = chat_completion_eval(messages=messages_multimodal, model=model)


if __name__ == "__main__":
    main()
    test_complex_prompts()