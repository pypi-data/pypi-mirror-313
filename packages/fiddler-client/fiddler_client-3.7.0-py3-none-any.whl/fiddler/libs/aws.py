# type: ignore
# TODO: do type-checking soon: https://github.com/fiddler-anyprem/hadron/issues/25

# Note(JP): allow for type hints using strings (so that for example
# "PartnerAppAuthProvider" can be used as a type hint w/o having to import the
# class).
from __future__ import annotations
import logging
import os
from collections import namedtuple
from typing import Optional

from fiddler.exceptions import BaseError


logger = logging.getLogger(__name__)

AwsSageMakerAuthConfig = namedtuple('AwsSageMakerAuthConfig', ['arn', 'url'])


def _read_env_for_aws_sagemaker_or_raise() -> Optional[AwsSageMakerAuthConfig]:
    """

    Raise `fiddler.exceptions.BaseError` when the environment appears to be
    misconfigured.
    """
    av = os.getenv('AWS_PARTNER_APP_AUTH')

    if av is None:
        return None

    if av.lower().strip() != 'true':
        return None

    # User has declared intent: activate SageMaker authentication. Require
    # other environment variables to be set.
    keys = ('AWS_PARTNER_APP_ARN', 'AWS_PARTNER_APP_URL')
    for k in keys:
        errmsg = f'AWS_PARTNER_APP_AUTH is set to `{av}`, but {k} is not set'
        if os.getenv(k) is None:
            # Future: maybe have a ConfigError type?
            raise BaseError(errmsg)

    # Future: potentially do validation for got error messages, but be sure
    # that the validation isn't getting in the way, _ever_.

    # Remove leading and trailing whitespace: that's a safe operation, and
    # always a user/config "error". That we can correct for.
    arn = os.getenv('AWS_PARTNER_APP_ARN').strip()  # type: ignore[union-attr]
    url = os.getenv('AWS_PARTNER_APP_URL').strip()  # type: ignore[union-attr]
    return AwsSageMakerAuthConfig(arn, url)


def _import_sm_sdk():  # -> "PartnerAppAuthProvider":
    """
    Return `sagemaker.PartnerAppAuthProvider` instance or raise an exception.
    """
    try:
        from sagemaker import PartnerAppAuthProvider  # pylint: disable=import-error
    except Exception as exc:
        errmsg = (
            f'The AWS_PARTNER_APP_* environment variables are set, but '
            f'importing a dependency failed: {exc}'
        )
        raise BaseError(errmsg)

    # Note(JP): can initialization of this auth provider object fail? Does it
    # use Internet resources? Update 1: this call is expected to fail with e.g.
    # `ValueError: Must specify a valid AWS_PARTNER_APP_ARN environment
    # variable` when this env var is not set. Update 2: this does indeed deeper
    # validation of the user-given config values. May throw for example
    # "ValueError: Must specify a valid AWS_PARTNER_APP_ARN environment
    # variable" when something non-ARN-looking has been provided. That is, we
    # can (and should) skip validating these env var values and lave this job
    # to the SM SDK.
    p = PartnerAppAuthProvider()
    logger.info('initialized AWS SageMaker authentication provider: %s', p)
    return p


def conditionally_init_aws_sm_auth():  # -> Optional["PartnerAppAuthProvider"]:
    """
    Return `None` or `PartnerAppAuthProvider` instance.

    Raise an exception upon configuration error or when dependencies are
    missing.
    """
    aws_sm_auth_cfg = _read_env_for_aws_sagemaker_or_raise()

    logger.debug('auth config: %s', aws_sm_auth_cfg)
    if aws_sm_auth_cfg is not None:
        return _import_sm_sdk()

    # Just to make this expected case explicit.
    return None
