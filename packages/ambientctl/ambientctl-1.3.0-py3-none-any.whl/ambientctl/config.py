from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ambient_server: str = "http://localhost:7417"
    cred_to_rest_dict: dict = {
        "create": "POST",
        "read": "GET",
        "update": "PUT",
        "delete": "DELETE",
    }
    ambient_log_lines: int = 1000
    version: str = "1.3.0"
    ambient_dev_mode: bool = False


settings = Settings()
