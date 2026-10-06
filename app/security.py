"""Dependências de segurança da API."""
import hmac
import os

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader


API_KEY_HEADER = APIKeyHeader(name="X-API-Key", scheme_name="ApiKeyAuth", auto_error=False)
EXPECTED_API_KEY = os.getenv("API_KEY", "dev-api-key")


def require_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> str:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key ausente",
        )
    if not hmac.compare_digest(api_key, EXPECTED_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida",
        )
    return api_key
