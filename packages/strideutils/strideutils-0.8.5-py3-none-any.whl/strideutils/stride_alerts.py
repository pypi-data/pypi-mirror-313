import datetime
import os
from enum import Enum
from functools import wraps
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union, cast

import pandas as pd
import tabulate

from strideutils import slack_connector
from strideutils.stride_config import config

DEFAULT_DAILY_UTC_HOUR = 17


class AlertType(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'


def get_tags(individuals: Union[str, Iterable[str]]) -> str:
    """Fetch slack ids for founders"""
    individuals = [individuals] if type(individuals) is str else individuals
    return " ".join(f"<@{config.slack_channels.get(person.lower(), person)}>" for person in individuals)


def df_to_message_body(df: pd.DataFrame) -> str:
    """Helper function to prettify a pandas dataframe for the slack message"""
    table = tabulate.tabulate(df, headers='keys', tablefmt='pretty', showindex=False)  # type: ignore
    return f"```\n{table}\n```"


def wrap_in_code_block(message: str) -> str:
    """
    Wraps a slack message in a code block
    """
    return f"```\n{message}\n```"


def notify(
    messages: Union[str, List[str]],
    urgency,
    tag: Optional[Union[str, Iterable[str]]] = None,
    beta_alert: bool = False,
    debug_readme: str = config.alerts_playbook,
    debug_readme_section: str = "",
) -> None:
    """
    Post an alert in the proper channel

    Args:
        msgs: A string or list of strings to notify on
        urgency: One of 'debug', 'info', 'warning', or 'critical'
        tag: A single or list of names or slack ids
        beta_alert: Modfies top-level message to not it's a work in progress
    """
    urgency = AlertType(urgency)

    messages_list: List = cast(List, [messages] if type(messages) is str else messages)

    debug_msg = f"Read more: {debug_readme}{debug_readme_section}"

    channel = "#alerts-info"
    if urgency == AlertType.DEBUG:
        channel = "#alerts-debug"
    elif urgency == AlertType.INFO:
        channel = "#alerts-info"
    elif urgency == AlertType.WARNING:
        channel = "#alerts-warnings"
    elif urgency == AlertType.CRITICAL:
        channel = "#alerts-critical"

    if beta_alert:
        messages_list[0] += "\nβ _This alert is in beta and might be unstable_"

    if tag:
        messages_list[0] += f"\n{get_tags(tag)}"

    messages_list.append(debug_msg)

    slack_client = slack_connector.SlackClient()
    slack_client.post_message(message=messages_list, channel=channel)


def raise_alert(
    urgency: Union[AlertType, str],
    tag: Optional[Union[str, Iterable[str]]] = None,
    beta_alert: bool = False,
    debug_readme: str = config.alerts_playbook,
    debug_readme_section: str = "",
) -> Callable:
    """
    Modify an alert to notify users based on severity

    The alert should have a return signature of
    msgs: Union[str, Iterable[str]]

    For local testing, set an environment variable ENV=DEV or use
    urgency='debug'
    """
    # Initialize stride client to make sure environment variables are set
    slack_connector.SlackClient()

    urgency = AlertType(urgency)
    if urgency == AlertType.DEBUG or os.environ.get('ENV') == 'DEV':
        print("DEV mode: Alert tagging and calling is suppressed. \n" "Slack alerts will appear in #alerts-debug.")
        tag = []
        urgency = AlertType.DEBUG

    def _decorator(f: Callable):
        @wraps(f)
        def _func(*args, **kwargs):
            output = f(*args, **kwargs)
            msgs: List = output[-1] if type(output) is tuple and len(output) == 2 else output  # type: ignore
            if urgency == 'debug':
                debug_msg = (
                    'In debug mode. Tags and calls have been disabled' 'and the message is routed to alerts-debug.'
                )
                print(debug_msg)
                msgs += [debug_msg]
            if msgs:
                notify(
                    messages=msgs,
                    urgency=urgency,
                    tag=tag,
                    beta_alert=beta_alert,
                    debug_readme=debug_readme,
                    debug_readme_section=debug_readme_section,
                )
            return output

        return _func

    return _decorator


def run_daily(utc_hour_or_alert: Union[int, Callable]) -> Callable:
    """
    Modifies an function to only run when the utc_hour matches the current time
    E.g. run_daily(5) would run if it's 5-6 UTC

    Runs at noon est by default, but can be modified:
    ```
    # Run if it's 17:00 utc
    @run_daily
    def foo():
        ...

    # Run if its 2:00 utc
    @run_daily(2)
    def bar():
        ...
    ```

    The returned function also returns a bool to indicate if the function was invoked
    """
    # If used without an argument, act as an unparameterized decorator
    if callable(utc_hour_or_alert):
        alert = utc_hour_or_alert

        @wraps(alert)
        def _func(*args, **kwargs) -> Tuple[bool, Any]:
            dt = datetime.datetime.now(tz=datetime.timezone.utc)
            if config.ENV == "DEV" or dt.hour == DEFAULT_DAILY_UTC_HOUR:
                return True, alert(*args, **kwargs)
            return False, None

        return _func

    # Otherwise return a decorator which modifies the function based on the
    # parameter
    assert type(utc_hour_or_alert) is int
    utc_hour = utc_hour_or_alert

    def _decorator(f: Callable):
        @wraps(f)
        def _func(*args, **kwargs):
            dt = datetime.datetime.now(tz=datetime.timezone.utc)
            if config.ENV == "DEV" or dt.hour == utc_hour:
                return True, f(*args, **kwargs)
            return False, None

        return _func

    return _decorator


def run_stride_epochly(f: Callable) -> Callable:
    """
    Modifies an function to run once per stride epoch
    Returns the new function returns a bool indicating if the function was executed
    When running in DEV mode, the function always executes
    """

    @wraps(f)
    def _func(*args, **kwargs) -> Tuple[bool, Any]:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        if config.ENV == "DEV" or dt.hour in {1, 7, 13, 19}:
            return True, f(*args, **kwargs)
        return False, None

    return _func


def run_day_epochly(f: Callable) -> Callable:
    """
    Modifies an function to run once per day epoch
    Returns the new function returns a bool indicating if the function was executed
    When running in DEV mode, the function always executes
    """

    @wraps(f)
    def _func(*args, **kwargs) -> Tuple[bool, Any]:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        if config.ENV == "DEV" or dt.hour == 19:
            return True, f(*args, **kwargs)
        return False, None

    return _func
