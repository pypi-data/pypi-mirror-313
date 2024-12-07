from collections import namedtuple
from enum import Enum



class ProvidersEnum(Enum):
    OPENAI = "openai"
    CHAT_OPENAI = "chat_openai"
    ANTHROPIC = "anthropic"
    CHAT_ANTHROPIC = "chat_anthropic"
    AZURE_CHAT_OPENAI = "azure_chat_openai"
    COHERE = "cohere"
    DALLE = "dall-e"
    TOGETHER_AI = "together_ai"
    MISTRAL_AI = "mistral_ai"
    PERPLEXITY = "perplexity"
    STABLE_DIFFUSION = "stable-diffusion"
    DALL_E = "dall-e"
    OPENROUTER = "openrouter"
    REPLICATE = "replicate"
    OPENAI_EMBEDDINGS = "openai_embeddings"
    AZURE_OPENAI_EMBEDDINGS = "azure_openai_embeddings"


class ModelsEnum(Enum):
    OPENAI_GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"
    AZURE_GPT_35_TURBO_16K = "gpt-35-turbo-16k"

    OPENAI_GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"

    OPENAI_GPT_35_TURBO_0613 = "gpt-3.5-turbo-0613"

    AZURE_GPT_35_TURBO = "gpt-35-turbo"

    OPENAI_GPT_4 = "gpt-4"
    AZURE_GPT_4 = "gpt-4"

    OPENAI_GPT_4_0613 = "gpt-4-0613"

    OPENAI_GPT_4_32K = "gpt-4-32k"
    AZURE_GPT_4_32K = "gpt-4-32k"

    OPENAI_GPT_35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"

    CLAUDE_INSTANT_12 = "claude-instant-1.2"

    DALLE_3 = "dall-e-3"
    
    STABLE_DIFFUSION_XL = "stable-diffusion-xl-1024-v1-0"
    STABLE_DIFFUSION_V6 = "stable-diffusion-v1-6"

    REPLICATE_FLUX = "black-forest-labs/flux-dev"
    REPLICATE_FLUX_PRO = "black-forest-labs/flux-pro"
    REPLICATE_FLUX_11_PRO = "black-forest-labs/flux-1.1-pro"
    REPLICATE_FLUX_SCHNELL = "black-forest-labs/flux-schnell"

    OPENAI_EMBEDDINGS_ADA_002 = "text-embedding-ada-002"
    AZURE_OPENAI_EMBEDDINGS_ADA_002 = "text-embedding-ada-002"
    OPENAI_EMBEDDINGS_TEXT_SMALL_3 = "text-embedding-3-small"

class StreamingEventType(Enum):
    UPDATE = "update"
    META = "meta"
    ERROR = "error"
    GENERATION_SOURCE = "generation_source"
    END = "end"


ModelDetails = namedtuple("ModelDetails", ["provider_name", "model_name"])


class GPTRouterEngines(Enum):
    OPENAI_GPT_35_TURBO = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-3.5-turbo"
    )
    OPENAI_GPT_35_TURBO_0613 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-3.5-turbo-0613"
    )
    OPENAI_GPT_35_TURBO_1106 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-3.5-turbo-1106"
    )
    OPENAI_GPT_35_TURBO_16K_0613 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-3.5-turbo-16k-0613"
    )
    OPENAI_GPT_35_TURBO_INSTRUCT = ModelDetails(
        ProvidersEnum.OPENAI.value, "gpt-3.5-turbo-instruct"
    )
    OPENAI_GPT_35_TURBO_0125 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-3.5-turbo-0125"
    )

    OPENAI_GPT_4_0613 = ModelDetails(ProvidersEnum.CHAT_OPENAI.value, "gpt-4-0613")
    OPENAI_GPT_4_TURBO = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-4-1106-preview"
    )
    OPENAI_GPT_4_TURBO_2024_04_09 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-4-turbo-2024-04-09"
    )

    OPENAI_GPT_4_TURBO_0125 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-4-0125-preview"
    )

    AZURE_OPENAI_GPT_4_TURBO_0125 = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt4-turbo-0125"
    )

    OPENAI_GPT_4_O = ModelDetails(ProvidersEnum.CHAT_OPENAI.value, "gpt-4o")
    
    OPENAI_GPT_4_O_MINI = ModelDetails(ProvidersEnum.CHAT_OPENAI.value, "gpt-4o-mini")
    AZURE_GPT_4O_MINI_2024_07_18 = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-4o-mini-2024-07-18"
    )
    OPENAI_GPT_4_O_24_08_06 = ModelDetails(ProvidersEnum.CHAT_OPENAI.value, "gpt-4o-2024-08-06")

    OPENAI_GPT_4_32K_0613 = ModelDetails(
        ProvidersEnum.CHAT_OPENAI.value, "gpt-4-32k-0613"
    )

    AZURE_GPT_35_TURBO = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-35-turbo"
    )
    AZURE_GPT_35_TURBO_16K = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-35-turbo-16k"
    )
    AZURE_GPT_35_TURBO_1106 = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-35-turbo-1106"
    )

    AZURE_GPT_4 = ModelDetails(ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-4")
    AZURE_GPT_4_TURBO = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-4-turbo"
    )
    AZURE_GPT_4_32K = ModelDetails(
        ProvidersEnum.AZURE_CHAT_OPENAI.value, "gpt-4-32k"
    )

    CLAUDE_INSTANT_12 = ModelDetails(
        ProvidersEnum.ANTHROPIC.value, "claude-instant-1.2"
    )
    CLAUDE_2 = ModelDetails(ProvidersEnum.ANTHROPIC.value, "claude-2")
    CLAUDE_21 = ModelDetails(ProvidersEnum.ANTHROPIC.value, "claude-2.1")
    CLAUDE_3_OPUS = ModelDetails(
        ProvidersEnum.ANTHROPIC.value, "claude-3-opus-20240229"
    )

    MISTRAL_7B = ModelDetails(
        ProvidersEnum.TOGETHER_AI.value, "mistralai/Mistral-7B-Instruct-v0.2"
    )
    MIXTRAL_8X7B = ModelDetails(
        ProvidersEnum.TOGETHER_AI.value, "mistralai/Mixtral-8x7B-Instruct-v0.1"
    )
    LLAMA_2_70B = ModelDetails(
        ProvidersEnum.TOGETHER_AI.value, "togethercomputer/llama-2-70b-chat"
    )

    MISTRAL_MEDIUM = ModelDetails(ProvidersEnum.MISTRAL_AI.value, "mistral-medium")

    PPTX_70B_ONLINE = ModelDetails(
        ProvidersEnum.PERPLEXITY.value, "pplx-70b-online"
    )
    PPTX_7B_ONLINE = ModelDetails(ProvidersEnum.PERPLEXITY.value, "pplx-7b-online")

    STABLE_DIFFUSION_XL = ModelDetails(
        ProvidersEnum.STABLE_DIFFUSION.value, "stable-diffusion-xl-1024-v1-0"
    )
    DALLE_3 = ModelDetails(ProvidersEnum.DALL_E.value, "dall-e-3")
    REPLICATE_FLUX = ModelDetails(
        ProvidersEnum.REPLICATE.value, "black-forest-labs/flux-dev"
    )
    REPLICATE_FLUX_PRO = ModelDetails(
        ProvidersEnum.REPLICATE.value, "black-forest-labs/flux-pro"
    )
    REPLICATE_FLUX_11_PRO = ModelDetails(
        ProvidersEnum.REPLICATE.value, "black-forest-labs/flux-1.1-pro"
    )
    REPLICATE_FLUX_SCHNELL = ModelDetails(
        ProvidersEnum.REPLICATE.value, "black-forest-labs/flux-schnell"
    )

    LLAMA_3_70B_NITRO = ModelDetails(
        ProvidersEnum.OPENROUTER, "meta-llama/llama-3-70b-instruct:nitro"
    )

    CLAUDE_3_SONNET = ModelDetails(
        ProvidersEnum.CHAT_ANTHROPIC.value, "claude-3-sonnet-20240229"
    )

    CLAUDE_3_HAIKU = ModelDetails(
        ProvidersEnum.CHAT_ANTHROPIC.value, "claude-3-haiku-20240307"
    )

    OPENROUTER_CLAUDE_3_HAIKU = ModelDetails(
        ProvidersEnum.OPENROUTER.value, "anthropic/claude-3-haiku"
    )
