from __future__ import annotations
from .client import client
import os

api = client(
    base_url="https://studio.edgeimpulse.com/v1",
    headers={"x-api-key": os.environ.get("EI_API_KEY")},
)

__all__ = [api]
