# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Owner"]


class Owner(BaseModel):
    id: str
    """Platform ID for the owner."""

    name: str
    """Name of the owner."""

    domain: Optional[str] = None
    """Domain of the owner."""

    status: Optional[str] = None
    """Platform status of the owner."""
