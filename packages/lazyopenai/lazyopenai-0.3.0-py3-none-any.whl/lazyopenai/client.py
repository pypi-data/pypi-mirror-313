from functools import cache

from openai import AzureOpenAI
from openai import OpenAI

from .settings import settings


@cache
def get_openai_client() -> OpenAI | AzureOpenAI:
    if settings.openai_api_key and settings.azure_openai_api_key:
        raise ValueError("Both OpenAI and Azure OpenAI API keys are set. Please set only one.")

    if settings.azure_openai_endpoint and settings.azure_openai_api_key:
        return AzureOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.openai_api_version,
            api_key=settings.azure_openai_api_key,
        )
    elif settings.openai_api_key:
        return OpenAI(api_key=settings.openai_api_key)
    else:
        raise ValueError("No OpenAI API key set.")
