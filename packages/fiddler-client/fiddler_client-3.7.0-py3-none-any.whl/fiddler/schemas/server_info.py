from typing import Dict, Generator

from fiddler.libs.semver import VersionInfo
from fiddler.schemas.base import BaseModel
from fiddler.schemas.organization import OrganizationCompactResp


class Version(VersionInfo):
    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return a list of validator methods for pydantic models."""
        yield cls.parse


class ServerInfo(BaseModel):
    feature_flags: Dict
    server_version: Version
    organization: OrganizationCompactResp
