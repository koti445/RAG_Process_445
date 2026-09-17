from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
    )
    
    app_name: str  =  "RAG Process 445"
    app_env:  str  =  "development"
    debug: bool  =  True
    api_prefix: str  =  "/api/v1"
    
    database_url: str  = ("postgresql+psycopg2://postgres:postgres@localhost:5432/rag_process_445")
    
    openai_api_key: str  = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    chroma_persist_dir: str = "./data/chroma"
    
    max_upload_mb: int = 50
    request_timeout_seconds: int = 30
    tesseract_cmd: str = ""
    
    
    @property
    def base_dir(self) ->  Path:
        return Path(__file__).resolve().parent.parent.parent
        
    @property
    def data_raw_dir(self) -> Path:
        path =  self.base_dir / "data" / "raw"
        path.mkdir(parents=True, exists_ok=True)
        return path
        
    @property
    def data_processed_dir(self) -> Path:
        path =  self.base_dir / "data" / "processed"
        path.mkdir(parents=True, exists_ok=True)
        return path
        
    @property
    def max_upload_bytes(self) -> int :
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
    
#get_settings()
        
        
    