from typing import Dict, List, Union
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from strideutils import stride_config
from strideutils.coingecko import (
    get_coingecko_name,
    get_dataframe_of_prices,
    get_dataframe_of_volumes,
    get_token_price,
    get_token_price_history,
    get_token_volume_history,
    get_tvl,
    validate_coingecko_env,
)
from strideutils.stride_config import Environment as e

# Test fixtures
HOST_ZONE_CONFIG: stride_config.HostChainConfig = stride_config.HostChainConfig(
    name="cosmos",
    id="cosmoshub-4",
    coingecko_name="cosmos",
    denom="ATOM",
)

BASIC_CHAIN_CONFIG: stride_config.HostChainConfig = stride_config.HostChainConfig(
    name="osmosis",
    id="osmosis-1",
    denom="OSMO",
)

# More specific types for the nested dictionaries
MarketDataType = Dict[str, Dict[str, Dict[str, float]]]
PriceDataType = Dict[str, Dict[str, float]]
CombinedResponseType = Dict[str, Union[Dict[str, float], Dict[str, Dict[str, float]]]]

COINGECKO_PRICE_RESPONSE: CombinedResponseType = {
    "cosmos": {"usd": 10.50},
    "market_data": {"market_cap": {"usd": 1000000.0}},
}

COINGECKO_HISTORY_RESPONSE: Dict[str, List[List[float]]] = {
    "prices": [
        [1643673600000, 10.50],  # 2022-02-01
        [1643760000000, 11.20],  # 2022-02-02
    ],
    "total_volumes": [
        [1643673600000, 1000000.0],  # 2022-02-01
        [1643760000000, 1200000.0],  # 2022-02-02
    ],
}


@pytest.fixture
def mock_config(monkeypatch):
    """Fixture to mock the config for chain lookups"""

    def mock_get_chain(*args, **kwargs):
        return HOST_ZONE_CONFIG

    monkeypatch.setattr("strideutils.stride_config.config.get_chain", mock_get_chain)


def test_validate_coingecko_env() -> None:
    """Test the environment validation function"""
    with patch("strideutils.coingecko.get_env_or_raise") as mock_get_env:
        # Test successful validation
        mock_get_env.return_value = "test_token"
        validate_coingecko_env()
        mock_get_env.assert_called_once_with(e.COINGECKO_API_TOKEN)

        # Test validation failure
        mock_get_env.reset_mock()
        mock_get_env.side_effect = EnvironmentError("Missing API token")
        with pytest.raises(RuntimeError, match="Failed to validate coingecko environment"):
            validate_coingecko_env()


def test_get_coingecko_name() -> None:
    """Test getting coingecko name from chain config"""
    # Test with coingecko_name attribute present
    assert get_coingecko_name(HOST_ZONE_CONFIG) == "cosmos"

    # Test fallback to name attribute when coingecko_name is not present
    assert get_coingecko_name(BASIC_CHAIN_CONFIG) == "osmosis"


@patch("strideutils.stride_requests.request")
@patch("strideutils.stride_requests.get_redemption_rate")
@patch("strideutils.coingecko.get_env_or_raise")
@patch("strideutils.coingecko.config")
def test_get_token_price(
    mock_config: Mock,
    mock_get_env_or_raise: Mock,
    mock_get_redemption_rate: Mock,
    mock_coingecko_request: Mock,
) -> None:
    """Test getting token price from coingecko"""
    # Set up our mocks
    mock_coingecko_request.return_value = {
        "cosmos": {"usd": 10.50},
        "ATOM": {"usd": 10.50},  # Added ATOM key for stATOM test
    }
    mock_get_redemption_rate.return_value = 1.0
    mock_get_env_or_raise.return_value = "test_token"

    # Mock the config.get_chain to return a proper config object
    mock_chain = Mock()
    mock_chain.coingecko_name = "cosmos"
    mock_config.get_chain.return_value = mock_chain

    # Test with explicit token
    price = get_token_price("cosmos", api_token="dummy_token")
    assert price == 10.50
    mock_coingecko_request.assert_called_with(
        "https://pro-api.coingecko.com/api/v3/simple/price",
        headers={"x-cg-pro-api-key": "dummy_token"},
        params={"ids": "cosmos", "vs_currencies": "usd"},
        cache_response=False,
    )

    # Should not call get_env_or_raise when explicit token is provided
    mock_get_env_or_raise.assert_not_called()

    # Test with environment variable
    price = get_token_price("cosmos")
    assert price == 10.50
    mock_get_env_or_raise.assert_called_once_with(e.COINGECKO_API_TOKEN)

    # Test stToken price calculation
    mock_get_redemption_rate.return_value = 1.1
    mock_config.get_chain.side_effect = KeyError  # Simulate config not found
    price = get_token_price("stATOM", api_token="dummy_token")
    assert price == 11.55  # 10.50 * 1.1
    mock_get_redemption_rate.assert_called_with("ATOM")


@patch("strideutils.stride_requests.request")
def test_get_tvl(mock_request: Mock) -> None:
    """Test getting TVL from coingecko"""
    mock_request.return_value = COINGECKO_PRICE_RESPONSE
    tvl = get_tvl(HOST_ZONE_CONFIG, api_token="dummy_token")
    assert tvl == 1000000.0
    mock_request.assert_called_with(
        "https://pro-api.coingecko.com/api/v3/coins/cosmos",
        headers={"x-cg-pro-api-key": "dummy_token"},
        cache_response=False,
    )


@patch("strideutils.stride_requests.request")
def test_get_token_price_history(mock_request: Mock, mock_config) -> None:
    """Test getting token price history from coingecko"""
    mock_request.return_value = COINGECKO_HISTORY_RESPONSE

    # Test with explicit token
    df = get_token_price_history("cosmos", num_days=2, api_token="dummy_token")

    expected_df = pd.DataFrame(
        {
            "price": [10.50, 11.20],
        },
        index=pd.DatetimeIndex(pd.to_datetime([1643673600000, 1643760000000], unit="ms"), name="time"),
    )
    assert_frame_equal(df, expected_df)

    mock_request.assert_called_with(
        "https://pro-api.coingecko.com/api/v3/coins/cosmos/market_chart",
        headers={"x-cg-pro-api-key": "dummy_token"},
        params={"vs_currency": "usd", "days": "2"},
    )

    # Test memoization
    df_cached = get_token_price_history("cosmos", num_days=2, api_token="dummy_token", _memo={})
    assert_frame_equal(df, df_cached)


@patch("strideutils.stride_requests.request")
def test_get_token_volume_history(mock_request: Mock, mock_config) -> None:
    """Test getting token volume history from coingecko"""
    mock_request.return_value = COINGECKO_HISTORY_RESPONSE

    df = get_token_volume_history("cosmos", num_days=2, api_token="dummy_token")

    expected_df = pd.DataFrame(
        {
            "volume": [1000000.0, 1200000.0],
        },
        index=pd.DatetimeIndex(pd.to_datetime([1643673600000, 1643760000000], unit="ms"), name="time"),
    )
    assert_frame_equal(df, expected_df)

    mock_request.assert_called_with(
        "https://pro-api.coingecko.com/api/v3/coins/cosmos/market_chart",
        headers={"x-cg-pro-api-key": "dummy_token"},
        params={"vs_currency": "usd", "days": "2"},
    )

    # Test memoization
    df_cached = get_token_volume_history("cosmos", num_days=2, api_token="dummy_token", _memo={})
    assert_frame_equal(df, df_cached)


@patch("strideutils.coingecko.get_token_price_history")
def test_get_dataframe_of_prices(mock_get_price_history: Mock) -> None:
    """Test getting price dataframe for multiple tokens"""
    start_date = pd.to_datetime("2022-02-01")
    end_date = pd.to_datetime("2022-02-02")

    # Create mock DataFrames with hourly data
    dates = pd.date_range(start=start_date, end=end_date, freq="h")
    mock_df1 = pd.DataFrame(
        {"price": [10.50] * len(dates)},
        index=dates,
    )
    mock_df2 = pd.DataFrame(
        {"price": [20.50] * len(dates)},
        index=dates,
    )
    mock_get_price_history.side_effect = [mock_df1, mock_df2]
    df = get_dataframe_of_prices(["cosmos", "osmosis"], num_days=2)
    expected_df = pd.DataFrame(
        {
            "cosmos": [10.50] * len(dates),
            "osmosis": [20.50] * len(dates),
        },
        index=dates,
    )
    assert_frame_equal(df, expected_df)


@patch("strideutils.coingecko.get_token_volume_history")
def test_get_dataframe_of_volumes(mock_get_volume_history: Mock) -> None:
    """Test getting volume dataframe for multiple tokens"""
    start_date = pd.to_datetime("2022-02-01")
    end_date = pd.to_datetime("2022-02-02")
    # Create mock DataFrames with hourly data
    dates = pd.date_range(start=start_date, end=end_date, freq="h")
    mock_df1 = pd.DataFrame(
        {"volume": [1000000.0] * len(dates)},
        index=dates,
    )
    mock_df2 = pd.DataFrame(
        {"volume": [2000000.0] * len(dates)},
        index=dates,
    )
    mock_get_volume_history.side_effect = [mock_df1, mock_df2]
    df = get_dataframe_of_volumes(["cosmos", "osmosis"], num_days=2)
    expected_df = pd.DataFrame(
        {
            "cosmos": [1000000.0] * len(dates),
            "osmosis": [2000000.0] * len(dates),
        },
        index=dates,
    )
    assert_frame_equal(df, expected_df)
