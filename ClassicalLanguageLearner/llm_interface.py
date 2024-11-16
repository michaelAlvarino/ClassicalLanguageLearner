from functools import cache
from openai import OpenAI

@cache
def get_llm_client() -> OpenAI:
    return OpenAI()