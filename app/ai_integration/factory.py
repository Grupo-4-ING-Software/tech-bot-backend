from typing import Dict, Type
from .base import AIProvider
from .providers.langchain_llm import LangchainLLMProvider

class AIProviderFactory:
    _providers: Dict[str, Type[AIProvider]] = {
        "langchain": LangchainLLMProvider
    }

    @classmethod
    def get_provider(cls, provider_name: str) -> AIProvider:
        provider_class = cls._providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Provider {provider_name} not found")
        return provider_class()

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[AIProvider]):
        cls._providers[name] = provider_class 