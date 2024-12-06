# @Author: Bi Ying
# @Date:   2024-07-27 00:02:34
from typing import Final, Dict, Any

from .enums import ContextLengthControlType

CONTEXT_LENGTH_CONTROL: Final[ContextLengthControlType] = ContextLengthControlType.Latest

ENDPOINT_CONCURRENT_REQUESTS: Final[int] = 20
ENDPOINT_RPM: Final[int] = 60
ENDPOINT_TPM: Final[int] = 300000

MODEL_CONTEXT_LENGTH: Final[int] = 32768

# Moonshot models
MOONSHOT_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "moonshot-v1-8k": {
        "id": "moonshot-v1-8k",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "moonshot-v1-32k": {
        "id": "moonshot-v1-32k",
        "context_length": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "moonshot-v1-128k": {
        "id": "moonshot-v1-128k",
        "context_length": 131072,
        "function_call_available": True,
        "response_format_available": True,
    },
}
MOONSHOT_DEFAULT_MODEL: Final[str] = "moonshot-v1-8k"

# Deepseek models
DEEPSEEK_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "deepseek-chat": {
        "id": "deepseek-chat",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "deepseek-coder": {
        "id": "deepseek-chat",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
}
DEEPSEEK_DEFAULT_MODEL: Final[str] = "deepseek-chat"

# Baichuan models
BAICHUAN_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "Baichuan4": {
        "id": "Baichuan4",
        "context_length": 32768,
        "max_output_tokens": 2048,
        "function_call_available": True,
        "response_format_available": True,
    },
    "Baichuan3-Turbo": {
        "id": "Baichuan3-Turbo",
        "context_length": 32768,
        "max_output_tokens": 2048,
        "function_call_available": True,
        "response_format_available": True,
    },
    "Baichuan3-Turbo-128k": {
        "id": "Baichuan3-Turbo-128k",
        "context_length": 128000,
        "max_output_tokens": 2048,
        "function_call_available": True,
        "response_format_available": True,
    },
    "Baichuan2-Turbo": {
        "id": "Baichuan2-Turbo",
        "context_length": 32768,
        "max_output_tokens": 2048,
        "function_call_available": True,
        "response_format_available": False,
    },
    "Baichuan2-53B": {
        "id": "Baichuan2-53B",
        "context_length": 32768,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": False,
    },
}
BAICHUAN_DEFAULT_MODEL: Final[str] = "Baichuan3-Turbo"

# Groq models
GROQ_DEFAULT_MODEL: Final[str] = "llama3-70b-8192"
GROQ_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "mixtral-8x7b-32768": {
        "id": "mixtral-8x7b-32768",
        "context_length": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "llama3-70b-8192": {
        "id": "llama3-70b-8192",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "llama3-8b-8192": {
        "id": "llama3-8b-8192",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gemma-7b-it": {
        "id": "gemma-7b-it",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gemma2-9b-it": {
        "id": "gemma2-9b-it",
        "context_length": 8192,
    },
    "llama3-groq-70b-8192-tool-use-preview": {
        "id": "llama3-groq-70b-8192-tool-use-preview",
        "context_length": 8192,
        "function_call_available": True,
        "max_output_tokens": 8000,
    },
    "llama3-groq-8b-8192-tool-use-preview": {
        "id": "llama3-groq-8b-8192-tool-use-preview",
        "context_length": 8192,
        "function_call_available": True,
        "max_output_tokens": 8000,
    },
    "llama-3.1-70b-versatile": {
        "id": "llama-3.1-70b-versatile",
        "context_length": 131072,
        "function_call_available": True,
        "max_output_tokens": 8000,
    },
    "llama-3.1-8b-instant": {
        "id": "llama-3.1-8b-instant",
        "context_length": 131072,
        "function_call_available": True,
        "max_output_tokens": 8000,
    },
}

# Qwen models
QWEN_DEFAULT_MODEL: Final[str] = "qwen2.5-72b-instruct"
QWEN_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "qwen1.5-1.8b-chat": {
        "id": "qwen1.5-1.8b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-4b-chat": {
        "id": "qwen1.5-4b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-7b-chat": {
        "id": "qwen1.5-7b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-14b-chat": {
        "id": "qwen1.5-14b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-32b-chat": {
        "id": "qwen1.5-32b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-72b-chat": {
        "id": "qwen1.5-72b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen1.5-110b-chat": {
        "id": "qwen1.5-110b-chat",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2-72b-instruct": {
        "id": "qwen2-72b-instruct",
        "context_length": 30000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2.5-7b-instruct": {
        "id": "qwen2.5-7b-instruct",
        "context_length": 131072,
        "max_output_tokens": 8192,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2.5-14b-instruct": {
        "id": "qwen2.5-14b-instruct",
        "context_length": 131072,
        "max_output_tokens": 8192,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2.5-32b-instruct": {
        "id": "qwen2.5-32b-instruct",
        "context_length": 131072,
        "max_output_tokens": 8192,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen2.5-72b-instruct": {
        "id": "qwen2.5-72b-instruct",
        "context_length": 131072,
        "max_output_tokens": 8192,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen-max": {
        "id": "qwen-max",
        "context_length": 8096,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen-max-longcontext": {
        "id": "qwen-max-longcontext",
        "context_length": 30000,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen-plus": {
        "id": "qwen-plus",
        "context_length": 131072,
        "max_output_tokens": 8096,
        "function_call_available": False,
        "response_format_available": True,
    },
    "qwen-turbo": {
        "id": "qwen-turbo",
        "context_length": 8096,
        "max_output_tokens": 1500,
        "function_call_available": False,
        "response_format_available": True,
    },
}

# Yi models
YI_DEFAULT_MODEL: Final[str] = "yi-lightning"
YI_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "yi-large": {
        "id": "yi-large",
        "context_length": 32000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-lightning": {
        "id": "yi-lightning",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-large-turbo": {
        "id": "yi-large-turbo",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-large-fc": {
        "id": "yi-large-fc",
        "context_length": 32000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": False,
    },
    "yi-medium": {
        "id": "yi-medium",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-medium-200k": {
        "id": "yi-medium-200k",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-spark": {
        "id": "yi-spark",
        "context_length": 16000,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "yi-vision": {
        "id": "yi-vision",
        "context_length": 4000,
        "max_output_tokens": 2000,
        "function_call_available": False,
        "response_format_available": False,
        "native_multimodal": True,
    },
}

# ZhiPuAI models
ZHIPUAI_DEFAULT_MODEL: Final[str] = "glm-4-air"
ZHIPUAI_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "glm-3-turbo": {
        "id": "glm-3-turbo",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4": {
        "id": "glm-4",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-plus": {
        "id": "glm-4-plus",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-0520": {
        "id": "glm-4-0520",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-air": {
        "id": "glm-4-air",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-airx": {
        "id": "glm-4-airx",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-flash": {
        "id": "glm-4-flash",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4-long": {
        "id": "glm-4-long",
        "context_length": 1000000,
        "function_call_available": True,
        "response_format_available": False,
        "max_output_tokens": 4095,
    },
    "glm-4v": {
        "id": "glm-4v",
        "context_length": 2000,
        "function_call_available": False,
        "response_format_available": False,
        "max_output_tokens": 1024,
        "native_multimodal": True,
    },
    "glm-4v-plus": {
        "id": "glm-4v-plus",
        "context_length": 2000,
        "function_call_available": False,
        "response_format_available": False,
        "max_output_tokens": 1024,
        "native_multimodal": True,
    },
}

# Mistral models
MISTRAL_DEFAULT_MODEL: Final[str] = "mistral-small"
MISTRAL_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "open-mistral-7b": {
        "id": "open-mistral-7b",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "open-mixtral-8x7b": {
        "id": "open-mixtral-8x7b",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "open-mixtral-8x22b": {
        "id": "open-mixtral-8x22b",
        "context_length": 64000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "open-mistral-nemo": {
        "id": "open-mistral-nemo",
        "context_length": 128000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "codestral-latest": {
        "id": "codestral-latest",
        "context_length": 32000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "mistral-small-latest": {
        "id": "mistral-small-latest",
        "context_length": 30000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "mistral-medium-latest": {
        "id": "mistral-medium-latest",
        "context_length": 30000,
        "function_call_available": False,
        "response_format_available": True,
    },
    "mistral-large-latest": {
        "id": "mistral-large-latest",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# OpenAI models
OPENAI_DEFAULT_MODEL: Final[str] = "gpt-4o"
OPENAI_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "gpt-35-turbo": {
        "id": "gpt-35-turbo",
        "context_length": 16385,
        "function_call_available": True,
        "response_format_available": True,
        "max_output_tokens": 4096,
    },
    "gpt-4-turbo": {
        "id": "gpt-4-turbo",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4": {
        "id": "gpt-4",
        "context_length": 8192,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "gpt-4o": {
        "id": "gpt-4o",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
    "gpt-4o-mini": {
        "id": "gpt-4o-mini",
        "context_length": 128000,
        "max_output_tokens": 16384,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
    "gpt-4v": {
        "id": "gpt-4v",
        "context_length": 128000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": True,
    },
    "o1-mini": {
        "id": "o1-mini",
        "context_length": 128000,
        "max_output_tokens": 65536,
        "function_call_available": False,
        "response_format_available": False,
        "native_multimodal": False,
    },
    "o1-preview": {
        "id": "o1-preview",
        "context_length": 128000,
        "max_output_tokens": 32768,
        "function_call_available": False,
        "response_format_available": False,
        "native_multimodal": False,
    },
}

# Anthropic models
ANTHROPIC_DEFAULT_MODEL: Final[str] = "claude-3-5-sonnet-20241022"
ANTHROPIC_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "claude-3-opus-20240229": {
        "id": "claude-3-opus-20240229",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": False,
        "native_multimodal": True,
    },
    "claude-3-sonnet-20240229": {
        "id": "claude-3-sonnet-20240229",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "native_multimodal": True,
        "response_format_available": False,
    },
    "claude-3-haiku-20240307": {
        "id": "claude-3-haiku-20240307",
        "context_length": 200000,
        "max_output_tokens": 4096,
        "function_call_available": True,
        "response_format_available": False,
        "native_multimodal": True,
    },
    "claude-3-5-haiku-20241022": {
        "id": "claude-3-5-haiku-20241022",
        "context_length": 200000,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": False,
        "native_multimodal": False,
    },
    "claude-3-5-sonnet-20240620": {
        "id": "claude-3-5-sonnet-20240620",
        "context_length": 200000,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": False,
        "native_multimodal": True,
    },
    "claude-3-5-sonnet-20241022": {
        "id": "claude-3-5-sonnet-20241022",
        "context_length": 200000,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": False,
        "native_multimodal": True,
    },
}

# Minimax models
MINIMAX_DEFAULT_MODEL: Final[str] = "abab6.5s-chat"
MINIMAX_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "abab5-chat": {
        "id": "abab5-chat",
        "context_length": 6144,
        "max_output_tokens": 6144,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab5.5-chat": {
        "id": "abab5.5-chat",
        "context_length": 16384,
        "max_output_tokens": 16384,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab6-chat": {
        "id": "abab6-chat",
        "context_length": 32768,
        "max_output_tokens": 32768,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab6.5s-chat": {
        "id": "abab6.5s-chat",
        "context_length": 245760,
        "max_output_tokens": 245760,
        "function_call_available": True,
        "response_format_available": True,
    },
    "abab7-preview": {
        "id": "abab7-preview",
        "context_length": 245760,
        "max_output_tokens": 245760,
        "function_call_available": True,
        "response_format_available": True,
    },
}

# Gemini models
GEMINI_DEFAULT_MODEL: Final[str] = "gemini-1.5-pro"
GEMINI_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "gemini-1.5-pro": {
        "id": "gemini-1.5-pro",
        "context_length": 2097152,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
    "gemini-1.5-flash": {
        "id": "gemini-1.5-flash",
        "context_length": 1048576,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
    "gemini-exp-1114": {
        "id": "gemini-exp-1114",
        "context_length": 32767,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
    "gemini-1.5-flash-8b": {
        "id": "gemini-1.5-flash-8b",
        "context_length": 1048576,
        "max_output_tokens": 8192,
        "function_call_available": True,
        "response_format_available": True,
        "native_multimodal": True,
    },
}

# 百度文心一言 ERNIE 模型
ERNIE_DEFAULT_MODEL: Final[str] = "ernie-lite"
ERNIE_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "ernie-lite": {
        "id": "ernie-lite",
        "context_length": 6144,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": False,
    },
    "ernie-speed": {
        "id": "ernie-speed",
        "context_length": 126976,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "ernie-speed-pro-128k": {
        "id": "ernie-speed-pro-128k",
        "context_length": 126976,
        "max_output_tokens": 4096,
        "function_call_available": False,
        "response_format_available": False,
    },
    "ernie-4.0-8k-latest": {
        "id": "ernie-4.0-8k-latest",
        "context_length": 5120,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": True,
    },
    "ernie-4.0-turbo-8k": {
        "id": "ernie-4.0-turbo-8k",
        "context_length": 5120,
        "max_output_tokens": 2048,
        "function_call_available": False,
        "response_format_available": True,
    },
}


STEPFUN_DEFAULT_MODEL: Final[str] = "step-1-8k"
STEPFUN_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "step-1-8k": {
        "id": "step-1-8k",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-1-32k": {
        "id": "step-1-32k",
        "context_length": 32000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-1-128k": {
        "id": "step-1-128k",
        "context_length": 128000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-1-256k": {
        "id": "step-1-256k",
        "context_length": 256000,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-2-16k": {
        "id": "step-2-16k",
        "context_length": 16384,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-1-flash": {
        "id": "step-1-flash",
        "context_length": 8192,
        "function_call_available": True,
        "response_format_available": True,
    },
    "step-1v-8k": {
        "id": "step-1v-8k",
        "context_length": 8192,
        "function_call_available": False,
        "response_format_available": False,
        "native_multimodal": True,
    },
    "step-1v-32k": {
        "id": "step-1v-32k",
        "context_length": 32768,
        "function_call_available": False,
        "response_format_available": False,
        "native_multimodal": True,
    },
}


XAI_DEFAULT_MODEL: Final[str] = "grok-beta"
XAI_MODELS: Final[Dict[str, Dict[str, Any]]] = {
    "grok-beta": {
        "id": "grok-beta",
        "context_length": 131072,
        "function_call_available": True,
        "response_format_available": True,
    },
}
