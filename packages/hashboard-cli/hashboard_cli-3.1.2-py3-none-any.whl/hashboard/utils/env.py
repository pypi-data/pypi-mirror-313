from typing import Optional
from os import environ

def env_with_fallback(varname_1: str, varname_2: str, fallback: Optional[str] = None) -> str:
    return environ.get(varname_1, default=environ.get(varname_2, default=fallback))
