# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["InstallDeploymentPackageResponse", "PackageInstallation"]


class PackageInstallation(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    organization_id: str
    """The identifier of the organization."""

    package_version_id: str
    """The package version which is installed"""

    account_id: Optional[str] = None
    """The ID of the account to which the installed package belongs.

    Unset for non-EGP entity deployment packages.
    """

    deleted_at: Optional[datetime] = None
    """The date and time when the entity was deleted in ISO format."""

    install_log: Optional[str] = None
    """output of installation step"""

    state: Optional[object] = None
    """Properties of the installation, must match schema of the package type."""

    status: Optional[Literal["INSTALLED", "UNINSTALLED", "IN_PROGRESS", "FAILED"]] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class InstallDeploymentPackageResponse(BaseModel):
    package_installation: PackageInstallation
