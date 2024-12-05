from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, description="The OpenAI API key.")
    openai_model: str = Field(default="gpt-4o-mini", description="The OpenAI model name.")
    openai_temperature: float = Field(default=0.0, description="The OpenAI temperature setting.")
    openai_max_tokens: int | None = Field(default=None, description="The OpenAI max tokens setting.")
    openai_embedding_model: str = Field(default="text-embedding-3-small", description="The OpenAI embedding model.")
    openai_api_version: str = Field(default="2024-10-01-preview", description="The OpenAI API version.")

    # azure
    azure_openai_api_key: str | None = Field(default=None, description="The Azure OpenAI API key.")
    azure_openai_endpoint: str | None = Field(default=None, description="The Azure OpenAI endpoint.")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


@cache
def get_settings() -> Settings:
    return Settings()
