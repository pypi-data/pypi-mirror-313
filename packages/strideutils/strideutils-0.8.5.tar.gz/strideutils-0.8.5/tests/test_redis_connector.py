from typing import Dict, Generator, Iterator, List, Optional, Protocol
from unittest.mock import MagicMock, Mock, patch

import pytest
from redis import Redis
from redis.client import Pipeline

from strideutils.redis_connector import RedisClient


class RedisProtocol(Protocol):
    def get(self, key: str) -> Optional[str]: ...
    def mget(self, keys: List[str]) -> List[Optional[str]]: ...
    def scan_iter(self, match: Optional[str] = None) -> Iterator[str]: ...
    def set(self, key: str, value: str) -> bool: ...
    def pipeline(self) -> Pipeline: ...


class MockRedis(MagicMock):
    """Mock Redis client that implements RedisProtocol"""

    def get(self, key: str) -> Optional[str]:
        return self.mock_get(key)

    def mget(self, keys: List[str]) -> List[Optional[str]]:
        return self.mock_mget(keys)

    def scan_iter(self, match: Optional[str] = None) -> Iterator[str]:
        return self.mock_scan_iter(match=match)

    def set(self, key: str, value: str) -> bool:
        return self.mock_set(key, value)

    def pipeline(self) -> Pipeline:
        return self.mock_pipeline()


@pytest.fixture
def mock_redis() -> Generator[MockRedis, None, None]:
    """Provide a mock Redis client"""
    with patch('strideutils.redis_connector.Redis') as mock:
        mock_instance = MockRedis(spec=Redis)
        # Set up mock methods
        mock_instance.mock_get = Mock(return_value=None)
        mock_instance.mock_mget = Mock(return_value=[])
        mock_instance.mock_scan_iter = Mock(return_value=iter([]))
        mock_instance.mock_set = Mock(return_value=True)
        mock_instance.mock_pipeline = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture(autouse=True)
def mock_env_vars() -> Generator[Mock, None, None]:
    """
    This function is a patch for `get_env_or_raise` to make it return a dummy value and random port.
    for the new environment variables added to `stride_config.py`.
    So anywhere we do a call to `get_env_or_raise` in these tests, it will return
    a `dummy_value`.
    """
    with patch('strideutils.redis_connector.get_env_or_raise') as mock_get_env:

        def side_effect(arg: str) -> str:
            return "6379" if "PORT" in arg else "dummy_value"

        mock_get_env.side_effect = side_effect
        yield mock_get_env


@pytest.fixture
def redis_client(mock_redis: MockRedis, mock_env_vars: Mock) -> RedisClient:
    """Provide a configured RedisClient instance"""
    return RedisClient(['public'])


def test_redis_client_non_singleton():
    """Test that each RedisClient instance is independent"""
    client1 = RedisClient(['public'])
    client2 = RedisClient(['frontend'])

    # Different instances
    assert client1 is not client2

    # Different database connections
    assert set(client1._dbs.keys()) == {'public'}
    assert set(client2._dbs.keys()) == {'frontend'}


def test_init_with_specific_dbs() -> None:
    """Test initialization with specific databases"""
    client = RedisClient(['public', 'frontend'])
    assert set(client._dbs.keys()) == {'public', 'frontend'}


def test_init_with_invalid_db() -> None:
    """Test initialization with invalid database name"""
    with pytest.raises(ValueError, match="Invalid Redis database names"):
        RedisClient(['invalid_db'])


def test_get_db(redis_client: RedisClient) -> None:
    """Test getting database client"""
    assert isinstance(redis_client.get_db('public'), MockRedis)


def test_get_db_no_name_single_db() -> None:
    """Test getting default database when only one is configured"""
    client = RedisClient(['public'])
    assert client.get_db() == client._dbs['public']


def test_get_db_no_name_multiple_dbs() -> None:
    """Test error when getting default database with multiple configured"""
    client = RedisClient(['public', 'frontend'])
    with pytest.raises(ValueError, match="Database name must be specified if multiple databases are configured"):
        client.get_db()


def test_get(redis_client: RedisClient, mock_redis: MockRedis) -> None:
    """Test getting a value from Redis"""
    expected_value = 'test_value'
    mock_redis.mock_get.return_value = expected_value

    assert redis_client.get('test_key', 'public') == expected_value
    mock_redis.mock_get.assert_called_once_with('test_key')


def test_get_multiple_keys(redis_client: RedisClient, mock_redis: MockRedis) -> None:
    """Test getting multiple values from Redis"""
    expected_values = ['value1', 'value2']
    mock_redis.mock_mget.return_value = expected_values

    result = redis_client.get_multiple_keys(['key1', 'key2'], 'public')
    assert result == expected_values
    mock_redis.mock_mget.assert_called_once_with(['key1', 'key2'])


def test_get_all_keys(redis_client: RedisClient, mock_redis: MockRedis) -> None:
    """Test getting all keys from Redis"""
    expected_keys = ['key1', 'key2']
    # Configure the mock to return the expected iterator
    mock_redis.mock_scan_iter.return_value = iter(expected_keys)

    result = redis_client.get_all_keys('public')

    # Test both the return value and the mock call
    assert result == expected_keys
    mock_redis.mock_scan_iter.assert_called_once_with(match=None)


def test_set(redis_client: RedisClient, mock_redis: MockRedis) -> None:
    """Test setting a value in Redis"""
    mock_redis.mock_set.return_value = True

    redis_client.set('test_key', 'test_value', 'public')
    mock_redis.mock_set.assert_called_once_with('test_key', 'test_value')


def test_set_keys(redis_client: RedisClient, mock_redis: MockRedis) -> None:
    """Test setting multiple values in Redis"""
    test_dict: Dict[str, str] = {'key1': 'value1', 'key2': 'value2'}
    mock_pipeline = Mock()
    mock_redis.mock_pipeline.return_value.__enter__ = Mock(return_value=mock_pipeline)
    mock_redis.mock_pipeline.return_value.__exit__ = Mock()

    redis_client.set_keys(test_dict, 'public', 'prefix_')

    assert mock_pipeline.set.call_count == 2
    mock_pipeline.set.assert_any_call('prefix_key1', 'value1')
    mock_pipeline.set.assert_any_call('prefix_key2', 'value2')
    mock_pipeline.execute.assert_called_once()
