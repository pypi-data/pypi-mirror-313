# GPTRouter Python Client

This is a Python client for the GPTRouter APIs.

## Installation

Use the package manager [pip](https://pypi.org/en/stable) to install gpt-router.

```bash
pip install gpt-router
```

## Usage

```python
from gpt_router.client import GPTRouterClient
from gpt_router.models import ModelGenerationRequest, GenerationParams
from gpt_router.enums import ModelsEnum, ProvidersEnum


client = GPTRouter(base_url='your_base_url', api_key='your_api_key')

messages = [
    {"role": "user", "content": "Write me a short poem"},
]
prompt_params = GenerationParams(messages=messages)
claude2_request = ModelGenerationRequest(
    model_name=ModelsEnum.CLAUDE_INSTANT_12,
    provider_name=ProvidersEnum.ANTHROPIC.value,
    order=1,
    prompt_params=prompt_params,
)

response = client.generate(ordered_generation_requests=[claude2_request])
print(response.choices[0].text)
```

Remember to replace `'your_base_url'` and `'your_api_key'` with your actual base URL and API key when using the client.