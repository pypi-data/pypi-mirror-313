from __future__ import annotations

import builtins
import logging
from datetime import datetime
from typing import Any, Iterator
from uuid import UUID

from pydantic.v1 import ValidationError

from fiddler.constants.alert_rule import AlertCondition, BinSize, CompareTo, Priority
from fiddler.decorators import handle_api_error
from fiddler.entities.base import BaseEntity
from fiddler.entities.baseline import BaselineCompactMixin
from fiddler.entities.model import ModelCompactMixin
from fiddler.entities.project import ProjectCompactMixin
from fiddler.schemas.alert_rule import AlertRuleResp, NotificationConfig
from fiddler.schemas.filter_query import OperatorType, QueryCondition, QueryRule


logger = logging.getLogger(__name__)


class AlertRule(
    BaseEntity, ModelCompactMixin, ProjectCompactMixin, BaselineCompactMixin
):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        model_id: UUID | str,
        metric_id: str | UUID,
        priority: Priority | str,
        compare_to: CompareTo | str,
        condition: AlertCondition | str,
        bin_size: BinSize | str,
        critical_threshold: float,
        warning_threshold: float | None = None,
        columns: list[str] | None = None,
        baseline_id: UUID | str | None = None,
        segment_id: UUID | str | None = None,
        compare_bin_delta: int | None = None,
        evaluation_delay: int = 0,
    ) -> None:
        """Construct a alert rule instance."""
        self.name = name
        self.model_id = model_id
        self.metric_id = metric_id
        self.columns = columns
        self.baseline_id = baseline_id
        self.priority = priority
        self.compare_to = compare_to
        self.compare_bin_delta = compare_bin_delta
        self.evaluation_delay = evaluation_delay
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.condition = condition
        self.bin_size = bin_size
        self.segment_id = segment_id

        self.id: UUID | None = None
        self.project_id: UUID | None = None

        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: AlertRuleResp | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get alert resource url."""
        url = '/v3/alert-rules'
        return url if not id_ else f'{url}/{id_}'

    @staticmethod
    def _get_notification_url(id_: UUID | str | None = None) -> str:
        """Get alert notification resource url."""
        return f'/v3/alert-rules/{id_}/notification'

    @classmethod
    def _from_dict(cls, data: dict) -> AlertRule:
        """Build entity object from the given dictionary."""

        # Deserialize the response
        resp_obj = AlertRuleResp(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
            model_id=resp_obj.model.id,
            metric_id=resp_obj.metric.id,
            priority=resp_obj.priority,
            compare_to=resp_obj.compare_to,
            condition=resp_obj.condition,
            bin_size=resp_obj.bin_size,
            critical_threshold=resp_obj.critical_threshold,
            warning_threshold=resp_obj.warning_threshold,
            columns=resp_obj.columns,
            baseline_id=resp_obj.baseline.id if resp_obj.baseline else None,
            segment_id=resp_obj.segment.id if resp_obj.segment else None,
            compare_bin_delta=resp_obj.compare_bin_delta,
            evaluation_delay=resp_obj.evaluation_delay,
        )

        # Add remaining fields
        fields = [
            'id',
            'created_at',
            'updated_at',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance.project_id = resp_obj.project.id
        instance._resp = resp_obj

        return instance

    def _refresh(self, data: dict) -> None:
        """Refresh the fields of this instance from the given response dictionary"""
        # Deserialize the response
        resp_obj = AlertRuleResp(**data)

        # Reset properties
        self.model_id = resp_obj.model.id
        self.project_id = resp_obj.project.id
        self.metric_id = resp_obj.metric.id

        # Add remaining fields
        fields = [
            'id',
            'created_at',
            'updated_at',
            'evaluation_delay',
        ]
        for field in fields:
            setattr(self, field, getattr(resp_obj, field, None))

        self._resp = resp_obj

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> AlertRule:
        """
        Get the alert rule instance using alert rule id.

        :param id_: unique uuid format identifier for alert rule
        :return: alert rule instance
        """

        response = cls._client().get(url=cls._get_url(id_=id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def list(  # pylint: disable=too-many-arguments
        cls,
        model_id: UUID | str,
        metric_id: UUID | str | None = None,
        columns: list[str] | None = None,
        baseline_id: UUID | str | None = None,
        ordering: list[str] | None = None,
    ) -> Iterator[AlertRule]:
        """
        Get a list of all alert rules in the organization.

        :param model_id: list from the specified model
        :param metric_id: list rules set on the specified metric id
        :param columns: list rules set on the specified list of columns
        :param baseline_id: list rules set on the specified baseline_id
        :param ordering: order result as per list of fields. ["-field_name"] for descending

        :return: paginated list of alert rules for the specified filters
        """
        rules: list[QueryRule | QueryCondition] = [
            QueryRule(field='model_id', operator=OperatorType.EQUAL, value=model_id)
        ]

        if baseline_id:
            rules.append(
                QueryRule(
                    field='baseline_id', operator=OperatorType.EQUAL, value=baseline_id
                )
            )
        if metric_id:
            rules.append(
                QueryRule(
                    field='metric_id', operator=OperatorType.EQUAL, value=metric_id
                )
            )
        if columns:
            for column in columns:
                rules.append(
                    QueryRule(
                        field='feature_names', operator=OperatorType.ANY, value=column
                    )
                )

        _filter = QueryCondition(rules=rules)
        params: dict[str, Any] = {'filter': _filter.json()}

        if ordering:
            params['ordering'] = ','.join(ordering)

        for rule in cls._paginate(url=cls._get_url(), params=params):
            yield cls._from_dict(data=rule)

    @handle_api_error
    def delete(self) -> None:
        """Delete an alert rule."""
        assert self.id is not None

        self._client().delete(url=self._get_url(id_=self.id))

    @handle_api_error
    def create(self) -> AlertRule:
        """Create a new alert rule."""
        payload: dict[str, Any] = {
            'name': self.name,
            'model_id': self.model_id,
            'metric_id': self.metric_id,
            'priority': self.priority,
            'compare_to': self.compare_to,
            'condition': self.condition,
            'bin_size': self.bin_size,
            'segment_id': self.segment_id,
            'critical_threshold': self.critical_threshold,
            'warning_threshold': self.warning_threshold,
            'feature_names': self.columns,
            'compare_bin_delta': self.compare_bin_delta,
            'evaluation_delay': self.evaluation_delay,
        }
        if self.baseline_id:
            payload['baseline_id'] = self.baseline_id

        response = self._client().post(
            url=self._get_url(),
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        self._refresh_from_response(response=response)
        return self

    @handle_api_error
    def enable_notifications(self) -> None:
        """Enable notifications for an alert rule"""
        self._client().patch(
            url=self._get_url(id_=self.id), json={'enable_notification': True}
        )
        logger.info(
            'notifications have been enabled for alert rule with id: %s', self.id
        )

    @handle_api_error
    def disable_notifications(self) -> None:
        """Disable notifications for an alert rule"""
        self._client().patch(
            url=self._get_url(id_=self.id), json={'enable_notification': False}
        )
        logger.info(
            'Notifications have been disabled for alert rule with id: %s', self.id
        )

    @handle_api_error
    def set_notification_config(
        self,
        emails: builtins.list[str] | None = None,
        pagerduty_services: builtins.list[str] | None = None,
        pagerduty_severity: str | None = None,
        webhooks: builtins.list[UUID] | None = None,
    ) -> NotificationConfig:
        """
        Set notification config for an alert rule

        :param emails: list of emails
        :param pagerduty_services: list of pagerduty services
        :param pagerduty_severity: severity of pagerduty
        :param webhooks: list of webhooks UUIDs

        :return: NotificationConfig object
        """

        # Validating input
        try:
            payload: dict[str, Any] = NotificationConfig(
                emails=emails,
                pagerduty_services=pagerduty_services,
                pagerduty_severity=pagerduty_severity,
                webhooks=webhooks,
            ).dict(exclude_none=True)
        except ValidationError as e:
            logger.exception('Invalid input: The format of input is not correct')
            raise e
        response = self._client().patch(
            url=self._get_notification_url(id_=self.id),
            data=payload,
            headers={'Content-Type': 'application/json'},
        )

        return NotificationConfig(**response.json()['data'])

    @handle_api_error
    def get_notification_config(self) -> NotificationConfig:
        """
        Get notifications config for an alert rule

        :return: NotificationConfig object
        """

        response = self._client().get(url=self._get_notification_url(id_=self.id))

        return NotificationConfig(**response.json()['data'])
