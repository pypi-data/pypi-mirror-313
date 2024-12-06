import pytest
from pytest_mock import MockerFixture

from fiddler import Connection
from fiddler.schemas.server_info import ServerInfo
from fiddler.tests.constants import ORG_ID, ORG_NAME, SERVER_VERSION, TOKEN, URL


@pytest.fixture(autouse=True, scope='session')
def connection(session_mocker: MockerFixture) -> Connection:
    """Connection instance"""
    conn = Connection(
        url=URL,
        token=TOKEN,
        validate=False,
    )

    server_info = ServerInfo(
        **{
            'feature_flags': {},
            'server_version': SERVER_VERSION,
            'organization': {
                'id': ORG_ID,
                'name': ORG_NAME,
            },
        }
    )
    session_mocker.patch.object(conn, '_get_server_info', return_value=server_info)
    session_mocker.patch('fiddler.conn', conn)
    yield conn
