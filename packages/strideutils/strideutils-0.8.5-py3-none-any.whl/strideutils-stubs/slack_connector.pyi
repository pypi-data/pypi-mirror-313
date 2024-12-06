from _typeshed import Incomplete

from strideutils.stride_config import config as config
from strideutils.stride_config import get_env_or_raise as get_env_or_raise

class SlackClient:
    def __new__(cls): ...
    api_token: Incomplete
    client: Incomplete
    def __init__(self) -> None: ...
    def post_message(
        self, message: str | list[str], channel: str, botname: str | None = None, thread_ts: str | None = None
    ): ...
    def upload_file(self, file_name: str, content: str) -> str: ...

def post_msg(
    txt: str | list[str],
    channel: str,
    botname: str | None = None,
    unfurl_links: bool = False,
    unfurl_media: bool = False,
    thread_ts: str | None = None,
): ...
def upload_file(file_name: str, content: str) -> str: ...
