import os
import re


import pytest
import responses
from responses import matchers

from fiddler.entities.model import Model
from fiddler.tests.constants import MODEL_ID, URL
from fiddler.tests.apis.test_model import API_RESPONSE_200


# Perform this test only if AWS_* env vars are set (so that this executes in a
# controlled environment, and skipped as part of general unit test suite
# invocation)
@pytest.mark.skipif(
    os.getenv('AWS_PARTNER_APP_AUTH') is None, reason='AWS_* env vars not set'
)
@responses.activate
def test_header_mutation() -> None:
    """
    Assume that the outer environment has set these environment variables:

    AWS_ACCESS_KEY_ID=dummykey
    AWS_SECRET_ACCESS_KEY=dummysecret
    AWS_PARTNER_APP_ARN=arn:aws:sagemaker:us-west-2:123456789012:partner-app/Partner/app-678901234567
    AWS_PARTNER_APP_URL=https://app-678901234567.us-west-2.mlapp.sagemaker.aws

    Note: boto.credentials is not affected by monkeypatch.setenv.
    fiddler-client initialization happens before entering this test, and
    the AWS_PARTNER_* vars need to be set _before_ entering this test.
    """

    arn = (
        'arn:aws:sagemaker:us-west-2:123456789012:partner-app/Partner/app-678901234567'
    )

    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=API_RESPONSE_200,
        match=[
            # regex-based header matching was added in
            # https://github.com/getsentry/responses/pull/663 which is also the
            # best documentation for that feature.
            matchers.header_matcher(
                {
                    # Note(JP): note how the dummy AWS_ACCESS_KEY_ID appears in
                    # the value -- the sagemaker wrapper creates a new
                    # Authorization header value with a SigV4 signature, using
                    # AWS credentials.
                    'Authorization': re.compile(
                        r'AWS4-HMAC-SHA256 Credential=dummykey/.+'
                    ),
                    # The sagemaker wrapper moves the original Authorization
                    # header here. In this test suite we typically set the
                    # value 'Bearer footoken'.
                    'X-Amz-Partner-App-Authorization': 'Bearer footoken',
                    'X-Amz-Target': 'SageMaker.CallPartnerAppApi',
                    'X-Mlapp-Sm-App-Server-Arn': arn,
                    # This is by default set by the client.
                    'X-Fiddler-Client-Name': 'python-sdk',
                }
            ),
        ],
    )

    # This call fails if it does not result in an HTTP request that matches
    # the pattern/structure defined with the `responses.get(...)` call above.
    # The error will say "the call doesn't match any registered mock" and
    # the detailed exception message allows for inspecting the headers seen
    # vs. the headers expected.
    Model.get(id_=MODEL_ID)
