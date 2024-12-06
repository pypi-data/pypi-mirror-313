# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["Investors"]


class Investors(BaseModel):
    id: str
    """Platform ID for the investor."""

    domain: str
    """Domain of the investor."""

    name: str
    """Name of the investor."""
