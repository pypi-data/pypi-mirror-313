import os
import pytest
from unittest.mock import patch, MagicMock
from clickhouse_driver.dbapi.connection import Connection
from clickhouse_driver.dbapi.extras import NamedTupleCursor

from good_clickhouse import (
    Clickhouse,
    ClickhouseProvider,
    ClickhouseAsync,
    ClickhouseAsyncProvider,
    ConnectionProfile,
)

# import os
# import pytest
# from unittest.mock import patch, MagicMock
# from clickhouse_driver.dbapi.connection import Connection
# from clickhouse_driver.dbapi.extras import NamedTupleCursor

# from good_clickhouse import Clickhouse, ClickhouseProvider, ClickhouseAsync, ClickhouseAsyncProvider, ConnectionProfile


@pytest.fixture
def mock_connection():
    connection = MagicMock(spec=Connection)
    cursor = MagicMock(spec=NamedTupleCursor)
    connection.cursor.return_value = cursor
    return connection


@pytest.fixture
def mock_clickhouse_provider(mock_connection):
    with patch(
        "good_clickhouse.ClickhouseProvider.provide",
        return_value=Clickhouse(mock_connection),
    ):
        yield ClickhouseProvider()


@pytest.fixture
def mock_async_clickhouse_provider(mock_clickhouse_provider):
    with patch("good_clickhouse.ClickhouseAsync") as async_client_mock:
        async_client_mock.return_value = MagicMock()
        yield ClickhouseAsync(sync_client=mock_clickhouse_provider.get())


def test_connection_profile_load_by_prefix():
    config = {
        "CLICKHOUSE_HOST": "localhost",
        "CLICKHOUSE_PORT": "9000",
        "CLICKHOUSE_DATABASE": "test_db",
        "CLICKHOUSE_USER": "default",
        "CLICKHOUSE_PASSWORD": "secret",
        "CLICKHOUSE_SECURE": "False",
        "CLICKHOUSE_COMPRESSION": "False",
    }
    profile = ConnectionProfile.load_by_prefix("CLICKHOUSE", config)
    assert profile.host == "localhost"
    assert profile.port == 9000
    assert profile.database == "test_db"
    assert profile.user == "default"
    assert profile.password.get_secret_value() == "secret"
    assert profile.secure is False
    assert profile.compression is False
    assert profile.model_dump(mode="json") == {
        "host": "localhost",
        "port": 9000,
        "database": "test_db",
        "user": "default",
        "password": "secret",
        "secure": False,
        "compression": False,
    }


def test_clickhouse_provider_provide(mock_clickhouse_provider, mock_connection):
    clickhouse_instance = mock_clickhouse_provider.provide()
    assert isinstance(clickhouse_instance, Clickhouse)
    assert clickhouse_instance.connection == mock_connection


def test_clickhouse_enter_exit(mock_connection):
    clickhouse = Clickhouse(connection=mock_connection)
    with clickhouse as cursor:
        assert cursor == mock_connection.cursor.return_value
    mock_connection.cursor.return_value.close.assert_called_once()
    mock_connection.close.assert_called_once()


@pytest.mark.asyncio
async def test_clickhouse_async_provide(mock_async_clickhouse_provider):
    async with mock_async_clickhouse_provider as async_client:
        assert async_client == mock_async_clickhouse_provider.connection


@pytest.mark.asyncio
async def test_clickhouse_async_enter_exit(mock_async_clickhouse_provider):
    async with mock_async_clickhouse_provider as async_client:
        assert async_client is not None
    # You can add assertions here if needed for closing the async connection
