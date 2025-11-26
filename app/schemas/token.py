"""Token schemas for authentication."""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data schema."""
    username: Optional[str] = None
