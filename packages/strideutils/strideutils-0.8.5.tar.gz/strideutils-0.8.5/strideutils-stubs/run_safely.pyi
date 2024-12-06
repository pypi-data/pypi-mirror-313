from typing import Callable

from strideutils import slack_connector as slack_connector
from strideutils.stride_config import config as config

def try_and_log_with_status(
    *functions: Callable,
    slack_channel: str = 'alerts-status',
    job_name: str = 'alerts',
    slack_client: slack_connector.SlackClient | None = None,
    botname: str | None = None,
    print_status: bool = False,
): ...
