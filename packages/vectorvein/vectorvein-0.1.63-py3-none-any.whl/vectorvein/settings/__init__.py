# @Author: Bi Ying
# @Date:   2024-07-27 00:30:56
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from ..types import defaults as defs
from ..types.enums import BackendType
from ..types.llm_parameters import BackendSettings, EndpointSetting


class Server(BaseModel):
    host: str
    port: int
    url: Optional[str]


class Settings(BaseModel):
    endpoints: List[EndpointSetting] = Field(
        default_factory=list, description="Available endpoints for the LLM service."
    )
    token_server: Optional[Server] = Field(default=None, description="Token server address. Format: host:port")

    anthropic: BackendSettings = Field(default_factory=BackendSettings, description="Anthropic models settings.")
    deepseek: BackendSettings = Field(default_factory=BackendSettings, description="Deepseek models settings.")
    gemini: BackendSettings = Field(default_factory=BackendSettings, description="Gemini models settings.")
    groq: BackendSettings = Field(default_factory=BackendSettings, description="Groq models settings.")
    local: BackendSettings = Field(default_factory=BackendSettings, description="Local models settings.")
    minimax: BackendSettings = Field(default_factory=BackendSettings, description="Minimax models settings.")
    mistral: BackendSettings = Field(default_factory=BackendSettings, description="Mistral models settings.")
    moonshot: BackendSettings = Field(default_factory=BackendSettings, description="Moonshot models settings.")
    openai: BackendSettings = Field(default_factory=BackendSettings, description="OpenAI models settings.")
    qwen: BackendSettings = Field(default_factory=BackendSettings, description="Qwen models settings.")
    yi: BackendSettings = Field(default_factory=BackendSettings, description="Yi models settings.")
    zhipuai: BackendSettings = Field(default_factory=BackendSettings, description="Zhipuai models settings.")
    baichuan: BackendSettings = Field(default_factory=BackendSettings, description="Baichuan models settings.")
    stepfun: BackendSettings = Field(default_factory=BackendSettings, description="StepFun models settings.")
    xai: BackendSettings = Field(default_factory=BackendSettings, description="XAI models settings.")

    def __init__(self, **data):
        model_types = {
            "anthropic": defs.ANTHROPIC_MODELS,
            "deepseek": defs.DEEPSEEK_MODELS,
            "gemini": defs.GEMINI_MODELS,
            "groq": defs.GROQ_MODELS,
            "local": {},
            "minimax": defs.MINIMAX_MODELS,
            "mistral": defs.MISTRAL_MODELS,
            "moonshot": defs.MOONSHOT_MODELS,
            "openai": defs.OPENAI_MODELS,
            "qwen": defs.QWEN_MODELS,
            "yi": defs.YI_MODELS,
            "zhipuai": defs.ZHIPUAI_MODELS,
            "baichuan": defs.BAICHUAN_MODELS,
            "stepfun": defs.STEPFUN_MODELS,
        }

        for model_type, default_models in model_types.items():
            if model_type in data:
                model_settings = BackendSettings()
                model_settings.update_models(default_models, data[model_type].get("models", {}))
                data[model_type] = model_settings
            else:
                data[model_type] = BackendSettings(models=default_models)

        super().__init__(**data)

    def load(self, settings_dict: Dict):
        self.__init__(**settings_dict)

    def get_endpoint(self, endpoint_id: str) -> EndpointSetting:
        for endpoint in self.endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        raise ValueError(f"Endpoint {endpoint_id} not found.")

    def get_backend(self, backend: BackendType) -> BackendSettings:
        return getattr(self, backend.value.lower())


settings = Settings()
