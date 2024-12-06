# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserInfo", "AccessProfile", "AccessProfileAccount", "AssumedAccessProfile", "AssumedAccessProfileAccount"]


class AccessProfileAccount(BaseModel):
    id: str

    name: str


class AccessProfile(BaseModel):
    id: str
    """Access profile id."""

    account: AccessProfileAccount
    """The account in the access profile."""

    role: Literal["manager", "admin", "editor", "member", "labeler", "disabled", "invited", "viewer"]
    """The role of the user in the access profile."""

    user_id: str
    """Id of the user in the access profile."""


class AssumedAccessProfileAccount(BaseModel):
    id: str

    name: str


class AssumedAccessProfile(BaseModel):
    id: str
    """Access profile id."""

    account: AssumedAccessProfileAccount
    """The account in the access profile."""

    role: Literal["manager", "admin", "editor", "member", "labeler", "disabled", "invited", "viewer"]
    """The role of the user in the access profile."""

    user_id: str
    """Id of the user in the access profile."""


class UserInfo(BaseModel):
    id: str
    """User id"""

    access_profiles: List[AccessProfile]
    """A list of access profiles that the selected user has access to"""

    email: str
    """E-mail address"""

    assumed_access_profile: Optional[AssumedAccessProfile] = None
    """Present if the user has assumed a specific access profile via JWT token."""

    first_name: Optional[str] = None
    """First name"""

    is_organization_admin: Optional[bool] = None
    """True if the current user is an organization admin."""

    last_name: Optional[str] = None
    """Last name"""

    organization_id: Optional[str] = None
    """The organization ID of the user."""

    preferences: Optional[object] = None
    """User preferences that can be stored in the Scale GenAI Platform."""
