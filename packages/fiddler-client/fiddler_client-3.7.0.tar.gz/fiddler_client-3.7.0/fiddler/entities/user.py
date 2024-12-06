from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserCompact:
    id: UUID
    full_name: str
    email: str


class CreatedByMixin:
    @property
    def created_by(self) -> UserCompact:
        """Model instance"""
        response = getattr(self, '_resp', None)
        if not response or not hasattr(response, 'created_by'):
            raise AttributeError(
                'This property is available only for objects generated from API '
                'response.'
            )

        return UserCompact(
            id=response.created_by.id,
            full_name=response.created_by.full_name,
            email=response.created_by.email,
        )


class UpdatedByMixin:
    @property
    def updated_by(self) -> UserCompact:
        """Model instance"""
        response = getattr(self, '_resp', None)
        if not response or not hasattr(response, 'updated_by'):
            raise AttributeError(
                'This property is available only for objects generated from API '
                'response.'
            )

        return UserCompact(
            id=response.updated_by.id,
            full_name=response.updated_by.full_name,
            email=response.updated_by.email,
        )
