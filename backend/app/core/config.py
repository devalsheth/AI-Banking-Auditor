from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    tcs_base_url: str = "https://genailab.tcs.in"
    tcs_model: str = "azure_ai/genailab-maas-DeepSeek-V3-0324"
    tcs_api_key: str = ""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
