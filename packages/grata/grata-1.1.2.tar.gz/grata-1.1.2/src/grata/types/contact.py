# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Contact"]


class Contact(BaseModel):
    name: str
    """Name of the contact."""

    title: str
    """Title of the contact."""

    work_email: str
    """Work email of the contact."""

    age: Optional[int] = None
    """Age of contact."""

    email_deliverability: Optional[str] = None
    """Email Deliverability of the contact's email."""

    socials_facebook: Optional[str] = None
    """Link to the contact's Facebook page."""

    socials_linkedin: Optional[str] = None
    """Link to the contact's LinkedIn page."""

    socials_twitter: Optional[str] = None
    """Link to the contact's Twitter page."""
