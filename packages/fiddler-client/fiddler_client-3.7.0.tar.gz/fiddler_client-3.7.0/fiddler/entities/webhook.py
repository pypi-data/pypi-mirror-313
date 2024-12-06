from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule
from fiddler.schemas.webhook import WebhookProvider, WebhookResp
from fiddler.utils.helpers import raise_not_found


class Webhook(BaseEntity):
    def __init__(self, name: str, url: str, provider: WebhookProvider | str) -> None:
        """
        Construct a webhook instance

        :param name: Slug like name
        """
        self.name = name
        self.url = url
        # provider is 'SLACK' or 'OTHER' as of Aug 2023.
        self.provider = provider

        self.id: UUID | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: WebhookResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get webhook resource/item url"""
        url = '/v2/webhooks'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Webhook:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = WebhookResp(**data)

        # Initialize
        instance = cls(name=resp_obj.name, url=resp_obj.url, provider=resp_obj.provider)
        # Add remaining fields
        fields = ['id', 'created_at', 'updated_at']
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = WebhookResp(**data)

        fields = [
            'id',
            'name',
            'url',
            'provider',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Webhook:
        """
        Get the webhook instance using webhook id

        :params uuid: UUID belongs to the Webhook
        :returns: `Webhook` object
        """
        response = cls._client().get(url=cls._get_url(id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, name: str) -> Webhook:
        """Get the webhook instance using webhook name"""
        _filter = QueryCondition(
            rules=[QueryRule(field='name', operator=OperatorType.EQUAL, value=name)]
        )

        response = cls._client().get(
            url=cls._get_url(), params={'filter': _filter.json()}
        )
        if response.json()['data']['total'] == 0:
            raise_not_found('Webhook not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(cls) -> Iterator[Webhook]:
        """Get a list of all webhooks in the organization"""
        for webhook in cls._paginate(url=cls._get_url()):
            yield cls._from_dict(data=webhook)

    @handle_api_error
    def create(self) -> Webhook:
        """
        Create a new webhook

        :params name: name of webhook
        :params url: webhook url
        :params provider: Either 'SLACK' or 'OTHER'

        :returns: Created `Webhook` object.
        """

        request_body = {
            'name': self.name,
            'url': self.url,
            'provider': self.provider,
        }
        response = self._client().post(
            url=self._get_url(),
            # Use custom JSON encoder (for UUID etc)
            data=request_body,
            headers={'Content-Type': 'application/json'},
        )
        self._refresh_from_response(response=response)
        return self

    @handle_api_error
    def update(self) -> None:
        """Update an existing webhook."""
        body: dict[str, Any] = {
            'name': self.name,
            'url': self.url,
            'provider': self.provider,
        }

        response = self._client().patch(url=self._get_url(id_=self.id), data=body)
        self._refresh_from_response(response=response)

    @handle_api_error
    def delete(self) -> None:
        """Delete an existing webhook."""

        self._client().delete(url=self._get_url(id_=self.id))
