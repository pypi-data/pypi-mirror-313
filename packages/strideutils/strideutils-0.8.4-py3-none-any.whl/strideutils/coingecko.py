"""
Exposes an easy API to get prices from coingecko
"""

from typing import Dict, List, Optional, Tuple

import pandas as pd

from strideutils import stride_config, stride_requests
from strideutils.stride_config import Environment as e
from strideutils.stride_config import config, get_env_or_raise

COINGECKO_ENDPOINT = "https://pro-api.coingecko.com/api/v3"
COINGECKO_PRICE_QUERY = "simple/price"
COINGECKO_HISTORY_QUERY = "coins/{token_id}/market_chart"
COINGECKO_TVL_QUERY = "coins/{token_id}"
COINGECKO_API_TOKEN_KEY = "x-cg-pro-api-key"


def validate_coingecko_env() -> None:
    """Optional validation helper that can be called before critical sections"""
    try:
        get_env_or_raise(e.COINGECKO_API_TOKEN)
    except EnvironmentError as err:
        raise RuntimeError(f"Failed to validate coingecko environment: {err}")


def get_coingecko_name(chain_config: stride_config.ChainConfig) -> str:
    """
    Returns the coingecko name for a given chain

    Args:
        chain_config: Chain configuration object

    Returns:
        The coingecko name for the chain
    """
    try:
        return chain_config.coingecko_name
    except AttributeError:
        return chain_config.name


def get_token_price(
    ticker: str,
    api_token: Optional[str] = None,
    cache_response: bool = False,
) -> float:
    """
    Reads token price from coingecko

    Args:
        ticker: Token ticker symbol
        api_token: Optional Coingecko API token. If None, will try to get it from environment
        cache_response: Whether to cache the response

    Returns:
        Current price of the token in USD

    Raises:
        ValueError: If no API token is found in args or environment variables
    """
    api_token = api_token or get_env_or_raise(e.COINGECKO_API_TOKEN)

    # TODO: Consider using the coingecko ID for stTokens instead of the redemption rate
    # Get redemption rate for calculating st token prices.
    redemption_rate = float(1)
    if ticker.startswith('st') and ticker[3].isupper():
        redemption_rate = stride_requests.get_redemption_rate(ticker[2:])
        ticker = ticker[2:]

    try:
        coingecko_name = get_coingecko_name(config.get_chain(ticker=ticker))
    except KeyError:
        coingecko_name = ticker

    endpoint = f"{COINGECKO_ENDPOINT}/{COINGECKO_PRICE_QUERY}"
    headers = {COINGECKO_API_TOKEN_KEY: api_token}
    params = {"ids": coingecko_name, "vs_currencies": "usd"}
    response = stride_requests.request(
        endpoint,
        headers=headers,
        params=params,
        cache_response=cache_response,
    )

    price = response[coingecko_name]["usd"] * redemption_rate
    return price


def get_tvl(
    chain_config: stride_config.ChainConfig,
    api_token: Optional[str] = None,
    cache_response: bool = False,
) -> float:
    """
    Fetch TVL from coingecko in USD

    Args:
        chain_config: Chain configuration object
        api_token: Optional Coingecko API token. If None, will try to get it from environment
        cache_response: Whether to cache the response

    Returns:
        Total Value Locked in USD

    Raises:
        ValueError: If no API token is found in args or environment variables
    """
    api_token = api_token or get_env_or_raise(e.COINGECKO_API_TOKEN)

    coingecko_name = get_coingecko_name(chain_config)
    endpoint = f"{COINGECKO_ENDPOINT}/{COINGECKO_TVL_QUERY.format(token_id=coingecko_name)}"
    headers = {COINGECKO_API_TOKEN_KEY: api_token}

    # The data structure is huge https://docs.coingecko.com/reference/coins-id
    response = stride_requests.request(endpoint, headers=headers, cache_response=cache_response)
    return float(response['market_data']['market_cap']['usd'])


def _get_token_history(
    coingecko_name: str,
    num_days: int,
    api_token: str,
) -> dict:
    """
    Queries the coingecko token history endpoint to get historical prices and volumes
    """
    url = f"{COINGECKO_ENDPOINT}/{COINGECKO_HISTORY_QUERY.format(token_id=coingecko_name)}"
    params = {"vs_currency": "usd", "days": str(num_days)}
    headers = {COINGECKO_API_TOKEN_KEY: api_token}
    response = stride_requests.request(url, headers=headers, params=params)
    return response


def get_token_price_history(
    token: str,
    num_days: int = 90,
    api_token: Optional[str] = None,
    _memo: Optional[Dict[Tuple[str, int], pd.DataFrame]] = None,
) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame with token price data going back num_days

    Args:
        token: Token ticker symbol
        num_days: Number of days of historical data to fetch
        api_token: Optional Coingecko API token. If None, will try to get it from environment
        _memo: Internal cache

    Returns:
        DataFrame with historical price data
    """
    # TODO: Figure out why API key is throwing an error when used.
    if _memo is None:
        _memo = {}

    price_key = (token, num_days)
    if price_key in _memo:
        return _memo[price_key]

    api_token = api_token or get_env_or_raise(e.COINGECKO_API_TOKEN)
    coingecko_name = get_coingecko_name(config.get_chain(ticker=token))
    response = _get_token_history(coingecko_name, num_days=num_days, api_token=api_token)

    df = pd.DataFrame(response["prices"], columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["price"] = df["price"].astype(float)
    df.set_index("time", inplace=True)

    _memo[price_key] = df
    return df


def get_token_volume_history(
    token: str,
    num_days: int = 90,
    api_token: Optional[str] = None,
    _memo: Optional[Dict[tuple, pd.DataFrame]] = None,
) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame with token volume data going back num_days

    Args:
        token: Token ticker symbol
        num_days: Number of days of historical data to fetch
        api_token: Optional Coingecko API token. If None, will try to get it from environment
        _memo: Internal cache

    Returns:
        DataFrame with historical volume data
    """
    # TODO: Figure out why API key is throwing an error when used.
    if _memo is None:
        _memo = {}

    volume_key = (token, num_days)
    if volume_key in _memo:
        return _memo[volume_key]

    api_token = api_token or get_env_or_raise(e.COINGECKO_API_TOKEN)
    coingecko_name = get_coingecko_name(config.get_chain(ticker=token))
    response = _get_token_history(coingecko_name, num_days=num_days, api_token=api_token)

    df = pd.DataFrame(response["total_volumes"], columns=["time", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["volume"] = df["volume"].astype(float)
    df.set_index("time", inplace=True)

    _memo[volume_key] = df
    return df


def get_dataframe_of_prices(token_list: List[str], num_days: int = 90) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame with token price data going back num_days, for the given tokens

    Args:
        token_list: List of token ticker symbols
        num_days: Number of days of historical data to fetch
        use_key: Whether to use the API key

    Returns:
        DataFrame with historical price data for all tokens
    """
    price_data: Dict[str, pd.Series] = {}

    for token in token_list:
        token_df = get_token_price_history(token, num_days)
        price_data[token] = token_df["price"]

    result_df = pd.DataFrame(price_data)

    # Resample based on data range
    if num_days > 90:
        result_df = result_df.resample("1D").last()
    elif num_days >= 2:
        result_df = result_df.resample("1h").last()
    else:
        result_df = result_df.resample("5min").last()

    return result_df


def get_dataframe_of_volumes(token_list: List[str], num_days: int = 90) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame with token volume data going back num_days, for the given tokens

    Args:
        token_list: List of token ticker symbols
        num_days: Number of days of historical data to fetch

    Returns:
        DataFrame with historical volume data for all tokens
    """
    volume_data: Dict[str, pd.Series] = {}

    for token in token_list:
        token_df = get_token_volume_history(token, num_days)
        volume_data[token] = token_df["volume"]

    result_df = pd.DataFrame(volume_data)

    # Resample based on data range
    if num_days > 90:
        result_df = result_df.resample("1D").last()
    elif num_days >= 2:
        result_df = result_df.resample("1h").last()
    else:
        result_df = result_df.resample("5min").last()

    return result_df
