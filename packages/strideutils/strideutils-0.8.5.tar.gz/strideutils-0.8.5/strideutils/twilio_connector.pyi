from _typeshed import Incomplete
from strideutils.stride_config import config as config, get_env_or_raise as get_env_or_raise
from typing import Iterable

class TwilioClient:
    call_template: str
    def __new__(cls): ...
    account_id: Incomplete
    api_token: Incomplete
    alert_numbers: Incomplete
    client: Incomplete
    def __init__(self) -> None: ...
    def call(self, msg: str, to: str | Iterable[str] | list[str]) -> None: ...
