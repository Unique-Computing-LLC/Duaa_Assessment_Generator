from pydantic_settings import BaseSettings


class Env(BaseSettings):
    # Example configuration values
    RUN_TYPE: str
    
    class Config:
        env_file = ".env"  # Optional: load variables from a .env file if present
        env_file_encoding = "utf-8"
