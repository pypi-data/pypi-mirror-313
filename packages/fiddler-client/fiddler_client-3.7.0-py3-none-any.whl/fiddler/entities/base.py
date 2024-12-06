from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, TypeVar

from requests import Response

from fiddler.configs import DEFAULT_PAGE_SIZE
from fiddler.connection import ConnectionMixin
from fiddler.schemas.response import PaginatedApiResponse

BaseEntityType = TypeVar(  # pylint: disable=invalid-name
    'BaseEntityType', bound='BaseEntity'
)


class BaseEntity(ABC, ConnectionMixin):
    @classmethod
    def _from_response(cls: type[BaseEntityType], response: Response) -> BaseEntityType:
        """Build entity object from the given response"""
        return cls._from_dict(data=response.json()['data'])

    @classmethod
    @abstractmethod
    def _from_dict(cls: type[BaseEntityType], data: dict) -> BaseEntityType:
        """Build entity object from the given dictionary"""

    def _refresh(self, data: dict) -> None:  # pylint: disable=unused-argument
        """Refresh the fields of this instance from the given response dictionary"""
        return

    def _refresh_from_response(self, response: Response) -> None:
        """Refresh the instance from the given response"""
        self._refresh(data=response.json()['data'])

    @classmethod
    def _paginate(
        cls, url: str, params: dict | None = None, page_size: int = DEFAULT_PAGE_SIZE
    ) -> Iterator[dict]:
        """
        Iterate over given pagination endpoint

        :param url: Pagination endpoint
        :param page_size: Number of items per page
        :return: Iterator of items
        """
        offset = 0
        params = params or {}
        params.update({'limit': page_size})

        while True:
            params.update({'offset': offset})
            response = cls._client().get(
                url=url,
                params=params,
            )
            resp_obj = PaginatedApiResponse(**response.json()).data

            yield from resp_obj.items

            if resp_obj.page_index >= resp_obj.page_count:
                # Last page
                break

            # Update offset
            offset = resp_obj.offset + page_size
