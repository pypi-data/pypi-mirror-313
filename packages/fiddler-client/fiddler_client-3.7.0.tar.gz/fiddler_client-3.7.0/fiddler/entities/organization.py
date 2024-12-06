from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fiddler.entities.base import BaseEntity
from fiddler.schemas.organization import OrganizationResp


class Organization(BaseEntity):
    def __init__(self) -> None:
        """Construct a organization instance"""

        self.name: str | None = None
        self.id: UUID | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: OrganizationResp | None = None

    @classmethod
    def _from_dict(cls, data: dict) -> Organization:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = OrganizationResp(**data)

        # Initialize
        instance = cls()

        # Add remaining fields
        fields = ['id', 'name', 'created_at', 'updated_at']
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance
