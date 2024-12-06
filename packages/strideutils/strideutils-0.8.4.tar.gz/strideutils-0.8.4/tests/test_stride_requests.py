from typing import Any
from unittest.mock import PropertyMock, patch

import numpy as np
import pandas as pd
import pytest

from strideutils.stride_config import HostChainConfig
from strideutils.stride_requests import (
    _get_host_zone_redemption_rate_slack,
    get_redemption_rate_slack,
    get_redemption_rate_slack_string,
)


@pytest.fixture
def mock_host_zones():
    """Mock host zone configurations"""
    host_zone1 = HostChainConfig(
        name="osmosis",
        id="osmosis-1",
        coingecko_name="osmosis",
        denom="uosmo",
        ticker="OSMO",
        api_endpoint="https://api.osmosis.zone",
        rpc_endpoint="https://rpc.osmosis.zone",
        denom_on_stride="stuosmo",
    )
    host_zone2 = HostChainConfig(
        name="cosmos",
        id="cosmoshub-4",
        coingecko_name="cosmos",
        denom="uatom",
        ticker="ATOM",
        api_endpoint="https://api.cosmos.network",
        rpc_endpoint="https://rpc.cosmos.network",
        denom_on_stride="statom",
    )
    return [host_zone1, host_zone2]


@pytest.fixture
def mock_host_zone_data():
    """Mock the response data from get_host_zone"""

    def get_mock_data(zone_id: str):
        if zone_id == "osmosis-1":
            return {
                "redemption_rate": "1.05",
                "min_redemption_rate": "0.95",
                "max_redemption_rate": "1.15",
                "min_inner_redemption_rate": "0.97",
                "max_inner_redemption_rate": "1.12",
                "halted": False,
            }
        elif zone_id == "cosmoshub-4":
            return {
                "redemption_rate": "1.10",
                "min_redemption_rate": "0.90",
                "max_redemption_rate": "1.20",
                "min_inner_redemption_rate": "0.93",
                "max_inner_redemption_rate": "1.18",
                "halted": True,
            }
        raise ValueError(f"Unknown zone ID: {zone_id}")

    return get_mock_data


def test_get_host_zone_redemption_rate_slack(mock_host_zone_data: dict[str, Any]):
    """Test slack calculation for a single host zone"""
    with patch('strideutils.stride_requests.get_host_zone') as mock_get_zone:
        mock_get_zone.side_effect = mock_host_zone_data

        result = _get_host_zone_redemption_rate_slack("osmosis-1")

        assert result["rr"] == 1.05
        assert np.isclose(result["down_slack"], 761.90, atol=0.01)  # (1.05 - 0.97) * 100 * 100 / 1.05
        assert np.isclose(result["up_slack"], 666.67, atol=0.01)  # (1.12 - 1.05) * 100 * 100 / 1.05
        assert not result["halted"]


def test_get_redemption_rate_slack(mock_host_zones: list[HostChainConfig], mock_host_zone_data: dict[str, Any]):
    """Test DataFrame output of redemption rate slack"""
    with (
        patch('strideutils.stride_requests.config') as mock_config,  # Mock entire config
        patch('strideutils.stride_requests.get_host_zone') as mock_get_host_zone,
    ):
        # Set up the host_zones property to return our mock data
        type(mock_config).host_zones = PropertyMock(return_value=mock_host_zones)
        mock_get_host_zone.side_effect = mock_host_zone_data

        result = get_redemption_rate_slack()

        assert isinstance(result, pd.DataFrame)
        assert list(result.index) == ["osmosis-1", "cosmoshub-4"]
        assert list(result.columns) == ["rr", "down_slack", "up_slack", "halted"]

        # Verify calculations
        osmosis = result.loc["osmosis-1"]
        assert osmosis["rr"] == 1.05
        assert np.isclose(osmosis["down_slack"], 761.90, atol=0.01)
        assert np.isclose(osmosis["up_slack"], 666.67, atol=0.01)
        assert not osmosis["halted"]


def test_get_redemption_rate_slack_string(mock_host_zones: HostChainConfig, mock_host_zone_data: dict[str, Any]):
    """Test string output format"""
    with (
        patch('strideutils.stride_requests.config') as mock_config,
        patch('strideutils.stride_requests.get_host_zone') as mock_get_host_zone,
    ):
        # Set up the host_zones property
        type(mock_config).host_zones = PropertyMock(return_value=mock_host_zones)
        mock_get_host_zone.side_effect = mock_host_zone_data

        result = get_redemption_rate_slack_string()

        assert isinstance(result, str)
        assert "osmosis-1" in result
        assert "RR: 1.050000" in result
        assert "Down Slack: 761.90" in result
        assert "Up Slack: 666.67" in result


def test_get_redemption_rate_slack_no_zones():
    """Test behavior when no host zones are available"""
    with patch('strideutils.stride_requests.config') as mock_config:
        # Set up empty host_zones
        type(mock_config).host_zones = PropertyMock(return_value=[])

        result = get_redemption_rate_slack()

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert list(result.columns) == ["rr", "down_slack", "up_slack", "halted"]
