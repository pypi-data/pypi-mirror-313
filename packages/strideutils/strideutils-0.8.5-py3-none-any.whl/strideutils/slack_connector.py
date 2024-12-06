import os
import traceback
from typing import List, Optional, Union

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from strideutils.stride_config import Environment as e
from strideutils.stride_config import config, get_env_or_raise


class SlackClient:
    """
    Singleton client used to post messages to slack
    """

    _instance = None

    def __new__(cls):
        # Creates a new instance if one does not already exist
        if cls._instance is None:
            cls._instance = super(SlackClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization if a client has already been created
        if hasattr(self, "client"):
            return

        self.api_token = get_env_or_raise(e.STRIDEBOT_API_TOKEN)
        self.client = WebClient(token=self.api_token)

    def post_message(
        self,
        message: Union[str, List[str]],
        channel: str,
        botname: Optional[str] = None,
        thread_ts: Optional[str] = None,
    ):
        """
        Posts a slack message to the given channel
        If the message is an array, this will post each element of the array as a thread

        Returns the thread_ts to allow chaining messages
        """
        # Allow optional channel overrides via an environment variable
        channel = os.environ.get(e.SLACK_CHANNEL_OVERRIDE, default=channel)

        # Listify
        messages = [message] if type(message) is str else message

        # Post each message, threading with the previous
        thread_ts = None or thread_ts
        for msg in messages:
            response = self.client.chat_postMessage(
                channel=channel,
                text=msg,
                thread_ts=thread_ts,
                username=botname,
            )
            if thread_ts is None:  # API advises to use parent IDs instead of child's
                thread_ts = response["ts"]

        return thread_ts

    def upload_file(self, file_name: str, content: str) -> str:
        """
        This uploads a file and returns a link that can be used to embed a file in slack
        Ex:
            url = upload_file("test.txt", "Hello World")
            post_msg(f"<{url}|This is a file>", channel="#alerts-debug")
        """
        slack_file = self.client.files_upload_v2(filename=file_name, content=content)
        file_link = slack_file["file"]["permalink"]
        return file_link


# TODO: Remove after all launchpad instances are removed
def post_msg(
    txt: Union[str, List[str]],
    channel: str,
    botname: Optional[str] = None,
    unfurl_links: bool = False,
    unfurl_media: bool = False,
    thread_ts: Optional[str] = None,
):
    """
    DEPRECATED: Use slack client instead

    Posts a slack message to the given channel, e.g.

        post_msg('hello world', 'general')

    if txt is an array, this will post each element of the array as a thread

    Args:
      username: Rename stridebot
    """
    token = get_env_or_raise(e.STRIDEBOT_API_TOKEN)
    client = WebClient(token=token)
    channel = config.slack_channels.get(channel.replace('#', ''), channel)
    channel = os.environ.get('SLACK_CHANNEL_OVERRIDE', default=channel)

    # Listify
    messages = [txt] if type(txt) is str else txt

    # thread ts keeps track of the latest thread ID so we can keep replying in-thread
    thread_ts = None or thread_ts
    for msg in messages:
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=msg,
                thread_ts=thread_ts,
                username=botname,
                unfurl_links=unfurl_links,
                unfurl_media=unfurl_media,
            )
            if thread_ts is None:  # API advises to use parent IDs instead of child's
                thread_ts = response['ts']
        except SlackApiError as error:
            print("Error sending message: ", error)
            raise
    return thread_ts


def upload_file(file_name: str, content: str) -> str:
    """
    DEPRECATED: Use slack client instead

    This uploads a file called "file_name" with the string contents "content"

    This will return a link that can be used to embed a file in slack.
    For example:
        url = upload_file("test.txt", "Hello World")
        post_msg(f"<{url}|This is a file>", channel="#alerts-debug")
    """
    token = get_env_or_raise(e.STRIDEBOT_API_TOKEN)
    client = WebClient(token=token)
    try:
        slack_file = client.files_upload_v2(filename=file_name, content=content)
    except Exception as error:
        print(f"Error uploading file to slack: {error}")
        traceback.print_exc()
        raise ValueError(f"Error uploading file to slack: {error}")
    file_link = slack_file['file']['permalink']
    return file_link
