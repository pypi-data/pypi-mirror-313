# AILiteLLM

[![PyPI version](https://badge.fury.io/py/ailitellm.svg)](https://badge.fury.io/py/ailitellm)
[![Downloads](https://static.pepy.tech/badge/ailitellm)](https://pepy.tech/project/ailitellm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Documentation Status](https://readthedocs.org/projects/ailitellm/badge/?version=latest)](https://ailitellm.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/ailitellm)](https://github.com/yourusername/ailitellm/issues)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/ailitellm)](https://github.com/yourusername/ailitellm/stargazers)

AILiteLLM is a lightweight Python wrapper around the Hugging Face Inference API that provides OpenAI-like interface for various open-source language models. It makes it easy to use powerful open-source models with an interface familiar to OpenAI developers.

## 📊 Package Stats
- PyPI: [https://pypi.org/project/ailitellm/](https://pypi.org/project/ailitellm/)
- Documentation: [https://ailitellm.readthedocs.io/](https://ailitellm.readthedocs.io/)
- Source Code: [https://github.com/yourusername/ailitellm](https://github.com/yourusername/ailitellm)
- Issue Tracker: [https://github.com/yourusername/ailitellm/issues](https://github.com/yourusername/ailitellm/issues)

## Features

- OpenAI-compatible interface
- Support for multiple Hugging Face models
- Stream responses support
- Function calling capabilities
- Full typing support
- Easy model switching

## Installation

From PyPI:
```bash
pip install ailitellm
```

From source:
```bash
git clone https://github.com/yourusername/ailitellm.git
cd ailitellm
pip install -e .
```

Development installation:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from ailitellm import ai, ailite_model

# Simple completion
response = ai("What is the capital of France?")
print(response.choices[0].message.content)

# Using a specific model
response = ai(
    "Explain quantum computing",
    model=ailite_model("Qwen/Qwen2.5-72B-Instruct")
)
```

## Available Models

AILiteLLM supports the following models:

- `Qwen/Qwen2.5-72B-Instruct` - Large general purpose model
- `Qwen/QwQ-32B-Preview` - Preview version of QwQ model
- `Qwen/Qwen2.5-Coder-32B-Instruct` - Specialized for coding tasks
- `NousResearch/Hermes-3-Llama-3.1-8B` - Efficient general purpose model
- `microsoft/Phi-3.5-mini-instruct` - Lightweight instruction-following model

## Advanced Usage

### Chat Completions

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke about programming."}
]

response = ai(messages)
```

### Streaming Responses

```python
for chunk in ai("Write a poem about AI", stream=True):
    print(chunk.choices[0].delta.content, end="")
```

### Function Calling

```python
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the weather for a location"""
    pass

response = ai(
    "What's the weather in London?",
    tools=[get_weather],
    tool_choice="auto"
)
```

### Advanced Parameters

```python
response = ai(
    "Generate a creative story",
    temperature=0.8,
    max_tokens=500,
    top_p=0.9,
    presence_penalty=0.6
)
```

### Custom Client

```python
from ailitellm import AILite

custom_client = AILite(
    base_url="your_custom_endpoint",
    api_key="your_api_key"
)
```

## Error Handling

```python
try:
    response = ai("Your prompt here")
except Exception as e:
    print(f"An error occurred: {e}")
```

## API Reference

### Main Functions

#### `ai(messages_or_prompt, **kwargs)`

Main interface for generating completions.

Key parameters:
- `messages_or_prompt`: List of messages or string prompt
- `model`: Model to use (default: "Qwen/Qwen2.5-72B-Instruct")
- `temperature`: Sampling temperature (default: 0)
- `max_tokens`: Maximum tokens to generate
- `stream`: Enable streaming responses
- `tools`: List of functions for tool calling
- See source code for full list of parameters

#### `ailite_model(model: HFModelType)`

Helper function to specify model type with proper type checking.

### Classes

#### `AILite`

Custom client class extending OpenAI's base client.

## 🧑‍💻 Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/ailitellm.git
cd ailitellm

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## 📦 Dependencies

- Python >= 3.8
- openai >= 1.0.0
- httpx
- typing-extensions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 Citation

If you use AILiteLLM in your research, please cite:

```bibtex
@software{ailitellm2024,
  author = {Your Name},
  title = {AILiteLLM: OpenAI-compatible Interface for Hugging Face Models},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/yourusername/ailitellm}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the API interface design
- Hugging Face for model hosting and inference API
- All model creators and contributors

## 📫 Contact

- GitHub Issues: [https://github.com/yourusername/ailitellm/issues](https://github.com/yourusername/ailitellm/issues)
- Email: your.email@example.com
- Twitter: [@yourusername](https://twitter.com/yourusername)