
# GoLean API Client

[![PyPI version](https://badge.fury.io/py/golean.svg?cache=0)](https://badge.fury.io/py/golean)
[![Python Versions](https://img.shields.io/pypi/pyversions/golean.svg)](https://pypi.org/project/golean/)

GoLean is a powerful Python client for the GoLean API, offering efficient and prompt compression services tailored for Large Language Models (LLMs). Optimize your LLM workflows with our state-of-the-art compression algorithms.

## Features

- **Efficient Prompt Compression:** Optimize LLM performance with prompt compression.
- **Flexible Model Support:** Compatible with a wide range of LLMs from OpenAI, Anthropic, and Cohere.
- **Cost Optimization:** Reduce token usage for various LLM APIs.
- **Secure Authentication:** Robust API key-based authentication system.
- **Easy Configuration:** Seamless setup with support for environment variables.
- **Comprehensive Documentation:** Detailed guides and API references to get you started quickly.

## Installation

Install the GoLean client using pip:

```bash
pip install golean
```

## Quick Start

Here’s how to get started with GoLean:

### Example 1: Compress Context

Context could be any text you want to compress. Examples of this could be user and bot messages in a conversation history, an article, a piece of text, etc. 

```python
from golean import GoLean

# Initialize the GoLean client
golean = GoLean(api_key="your_api_key")

# Compress a prompt
result = golean.compress_with_context(
    context="A large language model (LLM) is a type of computational model designed for natural language processing tasks such as language generation. As language models, LLMs acquire these abilities by learning statistical relationships from vast amounts of text during a self-supervised and semi-supervised training process."
)

print("Compressed Result:", result)
```

### Example 2: Compress Using Prompt Template and Data

Prompt template is a python string with placeholder strings that will be populated by data. Here, we will compress the data and then populate the compressed data back to the template.

```python
from golean import GoLean

# Initialize with API key
golean = GoLean(api_key="your_api_key")

# Compress template and data
result = golean.compress_with_template(
    template="""Read the passage, then answer the question. Only output the exact answer without any extra word or punctuation. 
Passage: {context}
Question: {question}""",
    data={
        "context": "A large language model (LLM) is a type of computational model designed for natural language processing tasks such as language generation. As language models, LLMs acquire these abilities by learning statistical relationships from vast amounts of text during a self-supervised and semi-supervised training process." ,
        "question": "name an example task the LLM is designed for"
    }
)

print("Compressed Result:", result)
```

## Configuration

### API Key

Set your API key using one of these methods:

1. Environment variable:

   ```bash
   export GOLEAN_API_KEY=your_api_key_here
   ```

2. `.env` file in your project root:

   ```
   GOLEAN_API_KEY=your_api_key_here
   ```

3. Directly in your code (not recommended for production):
   ```python
   golean = GoLean(api_key="your_api_key_here")
   ```

## API Reference

### `GoLean` Class

```python
class GoLean:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoLean client.

        Args:
            api_key (str, optional): Your GoLean API key. If not provided, reads from GOLEAN_API_KEY env variable.
        """

    def compress_with_context(context: str) -> Dict[str, Any]:
        """
        Compress a context string using the GoLean API.

        Args:
            context (str): The context string to be compressed.

        Returns:
            Dict[str, Any]: Contains compressed result, token counts, and compression rate.
        """

    def compress_with_template(template: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compress a template string by replacing placeholders with compressed values.

        Args:
            template (str): A string containing placeholders (e.g., "{key}").
            data (dict): Key-value pairs where keys match placeholders in the template.

        Returns:
            Dict[str, Any]: Contains compressed result, token counts, and compression rate.
        """
```

For complete API documentation, please refer to our [official documentation](https://docs.golean.ai).

## Response Format

The `compress_with_context` and `compress_with_template` methods returns a dictionary with the following keys:

- `compressed_result` (str): The compressed version of the input.
- `origin_tokens` (int): The number of tokens in the original input.
- `compressed_tokens` (int): The number of tokens in the compressed output.
- `compression_rate` (str): Ratio of compressed_tokens / origin_tokens.


## Supported Models

GoLean supports compression optimization for various LLM models:

## OpenAI Models

### GPT-3.5 Series

- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`

### GPT-4 Series

- `gpt-4`
- `gpt-4-turbo`

### GPT-4o Series

- `gpt-4o`
- `gpt-4o-mini`

### o1 Series

- `o1-preview`
- `o1-mini`

## Anthropic Models

### Claude 3 Series

- `claude-3-haiku`
- `claude-3-sonnet`
- `claude-3-opus`

### Claude 3.5 Series

- `claude-3.5-haiku`
- `claude-3.5-sonnet`

## Cohere Models

### Command Series

- `command-r`
- `command-r+`

### Aya Series

- `aya`

## Support

For technical assistance, please contact our support team:

- Email: support@golean.ai
- Documentation: [https://golean.ai](https://golean.ai)

For enterprise support options and custom LLM optimization solutions, please contact our sales team at support@golean.ai.

## Legal

Copyright © 2024 GoLean, Inc. All rights reserved.

GoLean is a registered trademark of GoLean, Inc. All other trademarks are the property of their respective owners.

---

Empower your LLMs with GoLean - Compress, Optimize, Succeed.
