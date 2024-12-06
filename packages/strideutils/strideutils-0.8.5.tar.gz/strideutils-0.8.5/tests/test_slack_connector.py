from typing import Generator
from unittest.mock import Mock, patch

import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from strideutils.slack_connector import SlackClient

# Test fixture and constants
TEST_TIMESTAMP: str = "1234567890.123456"
TEST_FILE_URL: str = "https://slack.com/file/123456"
TEST_CHANNEL: str = "#alerts-debug"

pytestmark = pytest.mark.usefixtures("mock_environ_get")


@pytest.fixture
def mock_environ_get(monkeypatch: pytest.MonkeyPatch) -> Generator[Mock, None, None]:
    """Mock environment variable access for testing."""
    mock = Mock(return_value=None)
    monkeypatch.setattr('os.environ.get', mock)
    yield mock


@pytest.fixture
def mock_webclient() -> Generator[Mock, None, None]:
    """Provide a mock Slack WebClient to avoid real API calls"""
    with patch('strideutils.slack_connector.WebClient') as mock_client:
        mock_instance = Mock(spec=WebClient)
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def slack_client(mock_webclient: Mock) -> Generator[SlackClient, None, None]:
    """Provide a configured SlackClient instance with mocked dependencies"""
    with patch("strideutils.slack_connector.get_env_or_raise", return_value="fake_token"):
        client = SlackClient()
        client.client = mock_webclient
        yield client


def test_slack_client_singleton() -> None:
    """Test that SlackClient maintains singleton pattern and properly handles env vars"""
    # Reset singleton state
    SlackClient._instance = None

    with (
        patch('strideutils.slack_connector.WebClient') as mock_client,
        patch('strideutils.slack_connector.get_env_or_raise', return_value='fake_token'),
    ):
        # Create first instance
        client1 = SlackClient()
        # Create second instance
        client2 = SlackClient()

        # Verify singleton behavior
        assert client1 is client2
        # Verify WebClient was only initialized once
        mock_client.assert_called_once_with(token='fake_token')

    # Clean up singleton state
    SlackClient._instance = None


def test_post_message_string(
    slack_client: SlackClient,
    mock_webclient: Mock,
    mock_environ_get: Mock,
) -> None:
    """Test posting a single message string"""
    # Setup environment mock to return None for SLACK_CHANNEL_OVERRIDE
    mock_environ_get.side_effect = lambda key, default=None: default

    # Mock the chat_postMessage response with a simple dictionary
    mock_webclient.chat_postMessage.return_value = {"ts": TEST_TIMESTAMP}

    thread_ts = slack_client.post_message("Hello, World!", TEST_CHANNEL)

    mock_webclient.chat_postMessage.assert_called_once_with(
        channel=TEST_CHANNEL,
        text="Hello, World!",
        thread_ts=None,
        username=None,
    )
    assert thread_ts == TEST_TIMESTAMP


def test_post_message_list(slack_client: SlackClient, mock_webclient: Mock) -> None:
    """Test posting a list of messages as a thread"""
    timestamps = [f"{TEST_TIMESTAMP[:-1]}{i}" for i in range(3)]
    mock_webclient.chat_postMessage.side_effect = [{"ts": ts} for ts in timestamps]

    messages = ["Message 1", "Message 2", "Message 3"]
    thread_ts = slack_client.post_message(messages, TEST_CHANNEL)

    assert mock_webclient.chat_postMessage.call_count == len(messages)
    assert thread_ts == timestamps[0]  # should return the first message's timestamp.


def test_upload_file(slack_client: SlackClient, mock_webclient: Mock) -> None:
    """Test file upload functionality"""
    mock_webclient.files_upload_v2.return_value = {
        "file": {"permalink": TEST_FILE_URL},
    }

    file_link = slack_client.upload_file("test.txt", "Hello, World!")

    mock_webclient.files_upload_v2.assert_called_once_with(
        filename="test.txt",
        content="Hello, World!",
    )
    assert file_link == TEST_FILE_URL


def test_post_message_error(slack_client: SlackClient, mock_webclient: Mock) -> None:
    """Test handling of Slack API errors"""
    mock_webclient.chat_postMessage.side_effect = SlackApiError("Error", {"error": "invalid_auth"})

    with pytest.raises(SlackApiError):
        slack_client.post_message("Hello, World!", TEST_CHANNEL)


def test_channel_override(
    mock_environ_get: Mock,
    slack_client: SlackClient,
    mock_webclient: Mock,
) -> None:
    """Test channel override functionality"""
    override_channel = "#override-channel"
    mock_environ_get.return_value = override_channel
    mock_webclient.chat_postMessage.return_value = {"ts": TEST_TIMESTAMP}

    slack_client.post_message("Hello, World!", TEST_CHANNEL)

    mock_webclient.chat_postMessage.assert_called_once_with(
        channel=override_channel,
        text="Hello, World!",
        thread_ts=None,
        username=None,
    )
