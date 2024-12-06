from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Iterator
from uuid import UUID

from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.schemas.alert_record import AlertRecordResp


class AlertRecord(BaseEntity):
    def __init__(self) -> None:
        """Construct a alert record instance"""

        self.alert_run_start_time: int | None = None
        self.alert_time_bucket: int | None = None
        self.alert_value: float | None = None
        self.baseline_time_bucket: int | None = None
        self.baseline_value: float | None = None
        self.is_alert: bool | None = None
        self.severity: str | None = None
        self.failure_reason: str | None = None
        self.message: str | None = None
        self.feature_name: str | None = None
        self.alert_record_main_version: int | None = None
        self.alert_record_sub_version: int | None = None

        self.id: UUID | None = None
        self.alert_rule_id: UUID | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: AlertRecordResp | None = None

    @classmethod
    def _from_dict(cls, data: dict) -> AlertRecord:
        """Build alert record object from the given dictionary"""

        # Deserialize the response
        resp_obj = AlertRecordResp(**data)

        # Initialize
        instance = cls()

        # Add remaining fields
        fields = [
            'id',
            'alert_rule_id',
            'alert_run_start_time',
            'alert_time_bucket',
            'alert_value',
            'baseline_time_bucket',
            'baseline_value',
            'is_alert',
            'severity',
            'failure_reason',
            'message',
            'feature_name',
            'alert_record_main_version',
            'alert_record_sub_version',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj

        return instance

    @staticmethod
    def _get_url(alert_rule_id: UUID | str, id_: UUID | str | None = None) -> str:
        """Get alert record resource/item url"""
        url = f'/v2/alert-configs/{alert_rule_id}/records'

        return url if not id_ else f'{url}/{id_}'

    @classmethod
    @handle_api_error
    def list(
        cls,
        alert_rule_id: UUID | str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ordering: list[str] | None = None,
    ) -> Iterator[AlertRecord]:
        """
        List alert records triggered for an alert rule

        :param alert_rule_id: unique identifier for alert rule
        :param start_time: Start time to filter trigger alerts :default: 7 days ago
        :param end_time: End time to filter trigger alerts :default: time now
        :param ordering: order result as per list of fields. ["-field_name"] for descending

        :return: paginated list of alert records for the given alert rule
        """
        params: dict[str, Any] = {
            'start_time': start_time or datetime.now() - timedelta(days=7),
            'end_time': end_time or datetime.now(),
        }
        if ordering:
            params['ordering'] = ordering

        for record in cls._paginate(url=cls._get_url(alert_rule_id), params=params):
            yield cls._from_dict(data=record)
