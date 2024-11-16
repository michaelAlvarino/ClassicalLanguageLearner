import os

def get_env() -> str:
    return os.environ.get("APP_ENV", "dev")

def is_prod() -> bool:
    return get_env() == "prod"
