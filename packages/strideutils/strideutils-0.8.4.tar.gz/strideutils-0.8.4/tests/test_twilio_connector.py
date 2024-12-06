from typing import Any, Dict, Generator
from unittest.mock import MagicMock, Mock, patch

import pytest
from twilio.rest import Client as TwilioRestClient

from strideutils.stride_config import Environment as e
from strideutils.twilio_connector import TwilioClient

# Test fixtures
TEST_PHONE_NUMBERS: Dict[str, str] = {
    'recipient1': '+12223334444',
    'recipient2': '+13334445555',
}

TEST_ALERT_NUMBER: str = '+15556667777'
TEST_TWIML: str = "<Response><Say>Test message</Say></Response>"


@pytest.fixture
def reset_twilio_client() -> Generator[None, None, None]:
    """Ensure each test starts with a fresh Twilio client instance"""
    TwilioClient._instance = None
    yield
    TwilioClient._instance = None


@pytest.fixture
def mock_twilio_rest_client() -> Generator[MagicMock, None, None]:
    """Mock the Twilio REST client to avoid real API calls"""
    with patch('strideutils.twilio_connector.Client') as mock:
        mock_instance = MagicMock(spec=TwilioRestClient)
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_env_vars() -> Generator[Mock, None, None]:
    """Mock environment variables required for Twilio client"""
    with patch('strideutils.twilio_connector.get_env_or_raise') as mock_get_env:

        def side_effect(arg: str) -> str:
            env_vars = {
                e.TWILIO_ACCOUNT_ID: 'fake_account_id',
                e.TWILIO_API_TOKEN: 'fake_api_token',
                e.TWILIO_ALERTS_NUMBER: 'fake_alert_numbers',
            }
            return env_vars.get(arg, 'dummy_value')

        mock_get_env.side_effect = side_effect
        yield mock_get_env


@pytest.fixture
def mock_config() -> Generator[Any, None, None]:
    """Mock config with test phone numbers"""
    with patch('strideutils.twilio_connector.config') as mock_cfg:
        mock_cfg.PHONE_NUMBERS = TEST_PHONE_NUMBERS
        mock_cfg.TWILIO_ALERTS_NUMBER = TEST_ALERT_NUMBER
        yield mock_cfg


@pytest.fixture
def twilio_client(mock_twilio_rest_client: MagicMock, mock_env_vars: Mock) -> TwilioClient:
    """Get a configured Twilio client instance"""
    return TwilioClient()


def test_twilio_client_singleton(mock_env_vars: Mock) -> None:
    """Test that TwilioClient maintains singleton pattern"""
    TwilioClient._instance = None  # Reset singleton
    client1 = TwilioClient()
    client2 = TwilioClient()
    assert client1 is client2
    TwilioClient._instance = None


def test_twilio_client_initialization(
    twilio_client: TwilioClient,
    mock_env_vars: Mock,
) -> None:
    """Test proper initialization of TwilioClient with environment variables"""
    assert twilio_client.account_id == 'fake_account_id'
    assert twilio_client.api_token == 'fake_api_token'
    assert twilio_client.alert_numbers == 'fake_alert_numbers'
    assert isinstance(twilio_client.client, MagicMock)


def test_call_single_recipient(
    twilio_client: TwilioClient,
    mock_twilio_rest_client: MagicMock,
    mock_config: Any,
) -> None:
    """Test making a call to a single recipient"""
    # Explicitly set the client to use our mock
    twilio_client.client = mock_twilio_rest_client

    twilio_client.call("Test message", "recipient1")

    mock_twilio_rest_client.calls.create.assert_called_once_with(
        to=TEST_PHONE_NUMBERS['recipient1'],
        from_=TEST_ALERT_NUMBER,
        twiml=TEST_TWIML,
    )


def test_call_multiple_recipients(
    twilio_client: TwilioClient,
    mock_twilio_rest_client: MagicMock,
    mock_config: Any,
) -> None:
    """Test making calls to multiple recipients"""
    # Explicitly set the client to use our mock
    twilio_client.client = mock_twilio_rest_client

    twilio_client.call("Test message", ["recipient1", "recipient2"])
    assert mock_twilio_rest_client.calls.create.call_count == 2
    mock_twilio_rest_client.calls.create.assert_any_call(
        to=TEST_PHONE_NUMBERS['recipient1'],
        from_=TEST_ALERT_NUMBER,
        twiml=TEST_TWIML,
    )
    mock_twilio_rest_client.calls.create.assert_any_call(
        to=TEST_PHONE_NUMBERS['recipient2'],
        from_=TEST_ALERT_NUMBER,
        twiml=TEST_TWIML,
    )


def test_call_invalid_recipient(
    twilio_client: TwilioClient,
    mock_config: Any,
) -> None:
    """Test that calling an invalid recipient raises KeyError"""
    with pytest.raises(KeyError):
        twilio_client.call("Test message", "invalid_recipient")
