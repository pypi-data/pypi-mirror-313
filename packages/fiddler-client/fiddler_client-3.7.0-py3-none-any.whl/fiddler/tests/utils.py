from typing import Any

from deepdiff import DeepDiff


def assert_approx(actual: Any, expected: Any, **kwargs: Any) -> None:
    """Assert with a threshold"""
    diff = DeepDiff(
        actual, expected, math_epsilon=0.0001, ignore_nan_inequality=True, **kwargs
    )
    if not diff:
        return

    raise AssertionError(diff)
