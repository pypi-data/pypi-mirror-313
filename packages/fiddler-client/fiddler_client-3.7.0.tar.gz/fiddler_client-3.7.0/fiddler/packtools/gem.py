from __future__ import annotations

import json
from typing import Any

import numpy as np


def convert_np_type_to_python(val: Any) -> Any:
    if isinstance(val, np.bool_):
        return bool(val)
    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        return float(val)
    return val


def convert_np_type(array: Any) -> Any:
    if isinstance(array, (np.ndarray, list)):
        return [convert_np_type_to_python(val) for val in array]
    return convert_np_type_to_python(array)


class GEMBase:
    def __init__(self) -> None:
        self._fields: dict[str, Any] = {'type': 'base'}

    def render(self) -> dict:
        out = {}
        for k, v in self._fields.items():
            out[k] = convert_np_type(v)
        return out

    def to_json(self) -> str:
        return json.dumps(self.render())


class GEMContainer(GEMBase):
    def __init__(
        self, display_name: str = '', contents: list[GEMBase] | None = None
    ) -> None:
        super().__init__()

        self._fields: dict[str, Any] = {'type': 'container'}

        if display_name:
            self._fields['display-name'] = display_name

        self._contents: list = []

        if contents is None:
            contents = []

        self.set_contents(contents)

    def set_contents(self, contents: list[GEMBase]) -> None:
        for x in contents:
            if not isinstance(x, GEMBase):
                raise ValueError(f'GEM_Container passed non-GEM child {x}.')

        self._contents = contents

    def render(self) -> dict:
        self._fields['contents'] = [child.render() for child in self._contents]

        att_list = [x['attribution'] for x in self._fields['contents']]
        self._fields['attribution'] = sum(att_list)

        return super().render()


class GEMSimple(GEMBase):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        display_name: str | None = None,
        feature_name: str | None = None,
        value: Any | None = None,
        attribution: float | None = None,
        attribution_uncertainty: float | None = None,
    ) -> None:
        super().__init__()

        self._fields: dict[str, Any] = {'type': 'simple'}

        if display_name is None and feature_name is None:
            raise ValueError(
                'GEM Simple fields must have "display_name", '
                '"feature_name", or both.'
            )

        if display_name is not None:
            self._fields['display-name'] = display_name

        if feature_name is not None:
            self._fields['feature-name'] = feature_name

        if value is not None:
            self._fields['value'] = value

        if attribution is not None:
            self._fields['attribution'] = attribution

        if attribution_uncertainty is not None:
            self._fields['attribution-uncertainty'] = attribution_uncertainty

    def set_attribution_uncertainty(self, attribution_uncertainty: float) -> None:
        self._fields['attribution-uncertainty'] = attribution_uncertainty


class GEMText(GEMBase):
    def __init__(
        self,
        display_name: str | None = None,
        feature_name: str | None = None,
        text_segments: list[str] | None = None,
        text_attributions: list[float] | None = None,
    ) -> None:
        super().__init__()

        self._fields: dict[str, Any] = {'type': 'text'}

        if display_name is None and feature_name is None:
            raise ValueError(
                'GEM Simple fields must have "display_name", '
                '"feature_name", or both.'
            )

        if display_name:
            self._fields['display-name'] = display_name

        if feature_name:
            self._fields['feature-name'] = feature_name

        if text_segments is not None and text_attributions is not None:
            self.set_contents(text_segments, text_attributions)

    def set_contents(
        self, text_segments: list[str], text_attributions: list[float]
    ) -> None:
        if len(text_segments) != len(text_attributions):
            raise ValueError(
                'GEM_Text requires that "text_segments" and '
                '"text_attributions" must be lists of the same'
                f' length.  They were {len(text_segments)} '
                f'and {len(text_attributions)} respectively.'
            )

        self._fields['text-segments'] = text_segments
        self._fields['text-attributions'] = text_attributions

    def render(self) -> dict:
        self._fields['attribution'] = sum(self._fields['text-attributions'])
        return super().render()
