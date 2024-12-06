import traceback
from typing import Callable, Optional

from strideutils import slack_connector
from strideutils.stride_config import config


def try_and_log_with_status(
    *functions: Callable,
    slack_channel: str = 'alerts-status',
    job_name: str = "alerts",
    slack_client: Optional[slack_connector.SlackClient] = None,
    botname: Optional[str] = None,
    print_status: bool = False,
):
    """
    Wrap functions in a try/catch and log exceptions.

    If the function failed, an error will get sent to slack_channel.
    If slack_channel is None, no slack message will be sent on failure.

    params
    ------
    functions: Callable
      Driver function
    """
    if config.ENV == 'DEV':
        slack_channel = 'alerts-debug'
        print_status = True

    if slack_client is None:
        slack_client = slack_connector.SlackClient()

    tracebacks = []
    msgs = []
    for func in functions:
        # Get the function name by first checking if there's a name attribute
        # (to cover cases where click was used)
        func_name = getattr(func, 'name', None) or func.__name__
        try:
            if print_status:
                print(f"Running {func_name}...", end="")

            # If the function was wrapped in a run_daily/run_epochly decorator,
            # the function will return a bool indicating if the function was executed
            # If it was skipped, use a different emoji
            output = func()
            func_skipped = type(output) is tuple and len(output) == 2 and not output[0]

            emoji_print = "⚪" if func_skipped else "✅"
            emoji_slack = ":white_circle:" if func_skipped else ":white_check_mark:"
            msgs += [f'{emoji_slack} {func_name}']

            if print_status:
                print(emoji_print)

        except Exception:
            print(traceback.format_exc())
            msgs += [f':x: {func_name} ']
            tracebacks.append(f"{func_name} \n\n" + traceback.format_exc())

            if print_status:
                print("❌")

    count_succeeded_msg = f"{len(functions) - len(tracebacks)}/{len(functions)} {job_name} succeeded"
    if len(tracebacks) > 0:
        status_msg = f':x: {count_succeeded_msg}'
    else:
        status_msg = f':white_check_mark: {count_succeeded_msg}'

    slack_client.post_message([status_msg] + ["\n".join(msgs)] + tracebacks, slack_channel, botname=botname)
