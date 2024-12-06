# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["IndustryClassification"]


class IndustryClassification(BaseModel):
    industry_code: str
    """Industry code."""

    industry_name: str
    """Industry name."""
