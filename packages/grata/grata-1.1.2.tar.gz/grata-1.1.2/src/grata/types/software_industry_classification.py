# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["SoftwareIndustryClassification"]


class SoftwareIndustryClassification(BaseModel):
    industry_code: str
    """Software industry code."""

    industry_name: str
    """Software industry name."""
