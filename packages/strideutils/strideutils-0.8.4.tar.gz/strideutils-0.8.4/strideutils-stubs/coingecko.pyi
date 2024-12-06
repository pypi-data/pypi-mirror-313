import pandas as pd

from strideutils import stride_config as stride_config
from strideutils import stride_requests as stride_requests
from strideutils.stride_config import config as config
from strideutils.stride_config import get_env_or_raise as get_env_or_raise

COINGECKO_ENDPOINT: str
COINGECKO_PRICE_QUERY: str
COINGECKO_HISTORY_QUERY: str
COINGECKO_TVL_QUERY: str
COINGECKO_API_TOKEN_KEY: str

def validate_coingecko_env() -> None: ...
def get_coingecko_name(chain_config: stride_config.ChainConfig) -> str: ...
def get_token_price(ticker: str, api_token: str | None = None, cache_response: bool = False) -> float: ...
def get_tvl(
    chain_config: stride_config.ChainConfig, api_token: str | None = None, cache_response: bool = False
) -> float: ...
def get_token_price_history(
    token: str,
    num_days: int = 90,
    api_token: str | None = None,
    _memo: dict[tuple[str, int], pd.DataFrame] | None = None,
) -> pd.DataFrame: ...
def get_token_volume_history(
    token: str, num_days: int = 90, api_token: str | None = None, _memo: dict[tuple, pd.DataFrame] | None = None
) -> pd.DataFrame: ...
def get_dataframe_of_prices(token_list: list[str], num_days: int = 90) -> pd.DataFrame: ...
def get_dataframe_of_volumes(token_list: list[str], num_days: int = 90) -> pd.DataFrame: ...
