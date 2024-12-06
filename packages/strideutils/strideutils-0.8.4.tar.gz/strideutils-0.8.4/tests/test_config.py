from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional

import pytest

from strideutils.stride_config import (
    MISSING_CONFIG_MSG,
    ChainConfig,
    ConfigDict,
    ConfigObj,
    HostChainConfig,
    RedisConfig,
    _parse_raw_configs,
)


# Test fixtures - Using actual objects instead of mocks where possible.
@dataclass(repr=False)
class DummyConfig(ConfigObj):
    """Test config class for testing ConfigObj behavior"""

    field_a: str
    field_b: str = ""
    field_c: Optional[str] = None

    def __iter__(self) -> Iterator[str]:
        return super().__iter__()


def test_config_obj() -> None:
    """Test ConfigObj attribute access and iteration behavior"""
    config = DummyConfig(field_a="value_a")

    # Accessing field A should be successful
    assert config.field_a == "value_a"

    # Accessing field B will error since it's empty
    with pytest.raises(AttributeError, match=MISSING_CONFIG_MSG.format(x="field_b")):
        config.field_b

    # Accessing field C will error since it's None
    with pytest.raises(AttributeError, match=MISSING_CONFIG_MSG.format(x="field_c")):
        config.field_c

    # Accessing field D will error since the field doesn't exist
    with pytest.raises(AttributeError, match="'DummyConfig' object has no attribute 'field_d'"):
        config.field_d

    # Test field existens checks
    assert "field_a" in config
    assert "field_d" not in config

    # Test iteration with all fields populated
    config_full = DummyConfig(field_a="value_a", field_b="value_b", field_c="value_c")
    assert list(config_full) == ["value_a", "value_b", "value_c"]


def test_config_dict() -> None:
    """Test ConfigDict key access and validation behavior"""
    config: ConfigDict = ConfigDict()
    config["field_a"] = "value_a"
    config["field_b"] = ""
    config["field_c"] = None

    # Accessing field A should be successful
    assert config["field_a"] == "value_a"

    # Accessing field B will error since it's empty
    with pytest.raises(KeyError, match=MISSING_CONFIG_MSG.format(x="field_b")):
        config["field_b"]

    # Accessing field C will error since it's None
    with pytest.raises(KeyError, match=MISSING_CONFIG_MSG.format(x="field_c")):
        config["field_c"]

    # Accessing field D will error since the field doesn't exist
    with pytest.raises(KeyError, match=MISSING_CONFIG_MSG.format(x="field_d")):
        config["field_d"]

    # Test key existence checks
    assert "field_a" in config
    assert "field_d" not in config


class TestParseConfig:
    """Tests for config parsing and chain configuration"""

    def setup_method(self) -> None:
        """Initialize test data before each test"""
        # Define some sample chain names
        self.host_chain_names = ["cosmoshub", "osmosis", "juno"]
        self.app_chain_names = ["neutron", "kava", "iris"]

        # Add redis configuration
        self.raw_redis = {
            "public": {"host": "test-public.upstash.io", "port": 1234, "ssl": False},
            "frontend": {"host": "test-frontend.upstash.io", "port": 5678, "ssl": True},
        }

        self.raw_stride: Dict[str, str] = {
            "name": "stride",
            "id": "stride-1",
            "ticker": "STRD",
            "denom": "ustrd",
        }

        self.raw_host_chains: Dict[str, Dict[str, str]] = {
            chain: {"name": chain, "id": f"{chain}-1"} for chain in self.host_chain_names
        }

        self.raw_app_chains: Dict[str, Dict[str, str]] = {
            chain: {"name": chain, "id": f"{chain}-1"} for chain in self.app_chain_names
        }

        self.raw_config: Dict[str, Any] = {
            "stride": self.raw_stride,
            "host_zones": self.raw_host_chains,
            "app_chains": self.raw_app_chains,
            "redis": self.raw_redis,
        }
        self.raw_secrets: Dict[str, Optional[str]] = {"ENV": "DEV"}

    def test_parse_valid_config(self) -> None:
        """Tests parsing a valid config"""
        config = _parse_raw_configs(self.raw_config, self.raw_secrets)

        # Validate all chains are set
        assert config.stride.name == "stride"
        assert set(config.host_zone_names) == set(self.host_chain_names)
        assert set(config.app_chain_names) == set(self.app_chain_names)

        # Validate Redis configuration
        assert isinstance(config.redis, dict)
        assert "public" in config.redis
        assert isinstance(config.redis["public"], RedisConfig)
        assert config.redis["public"].host == "test-public.upstash.io"
        assert config.redis["public"].port == 1234
        assert config.redis["public"].ssl is False  # Verify SSL setting

        # Test iteration over host_zones
        assert len(list(config.host_zones)) == len(self.host_chain_names)
        assert all(isinstance(zone, HostChainConfig) for zone in config.host_zones)

    def test_parse_config_missing_stride(self) -> None:
        """Test that parsing fails when stride config is missing"""
        raw_config = deepcopy(self.raw_config)
        del raw_config["stride"]

        with pytest.raises(KeyError, match="stride"):
            _parse_raw_configs(raw_config, self.raw_secrets)

    def test_parse_config_extra_host_chain_field(self) -> None:
        """
        Tests that parsing a config with a host chain field that's not defined in
        the ChainConfig class will succeed, but the extra field won't be accessible
        """
        raw_config = deepcopy(self.raw_config)
        raw_config["host_zones"]["cosmoshub"] = {"name": "cosmoshub", "id": "cosmoshub-1", "new_field": "value1"}

        config = _parse_raw_configs(raw_config, self.raw_secrets)
        host_chain = config.get_host_chain(name="cosmoshub")

        assert isinstance(host_chain, HostChainConfig)
        assert host_chain.name == "cosmoshub"
        assert host_chain.id == "cosmoshub-1"

        # Verify extra field is not accessible
        with pytest.raises(AttributeError, match="'HostChainConfig' object has no attribute 'new_field'"):
            host_chain.new_field  # type: ignore

    def test_parse_config_extra_app_chain_field(self):
        """
        Tests that parsing a config with an app chain field that's not defined in
        the ChainConfig class will succeed, but the extra field won't be accessible
        """
        raw_config = deepcopy(self.raw_config)
        raw_config["app_chains"]["neutron"] = {"name": "neutron", "id": "neutron-1", "new_field": "value1"}

        config = _parse_raw_configs(raw_config, self.raw_secrets)
        app_chain = config.get_chain(name="neutron")

        assert isinstance(app_chain, ChainConfig)
        assert app_chain.name == "neutron"
        assert app_chain.id == "neutron-1"

        # Verify the extra field is not accessible
        with pytest.raises(AttributeError, match="'ChainConfig' object has no attribute 'new_field'"):
            app_chain.new_field  # type: ignore

    def test_get_chain(self):
        """Test the get_chain lookup functionality"""
        config = _parse_raw_configs(self.raw_config, self.raw_secrets)

        # Test looking up stride
        assert config.get_chain(name="stride").id == "stride-1"
        assert config.get_chain(id="stride-1").name == "stride"

        # Test looking up a host zone
        assert config.get_chain(name="osmosis").id == "osmosis-1"
        assert config.get_chain(id="osmosis-1").name == "osmosis"

        # Test looking up an app chain
        assert config.get_chain(name="neutron").id == "neutron-1"
        assert config.get_chain(id="neutron-1").name == "neutron"

        # Test looking up non-existent chain
        with pytest.raises(KeyError, match="No chain found for the given parameter"):
            config.get_chain(name="non-existent")

        # Test invalid parameters
        with pytest.raises(KeyError, match="Exactly one of name, id, ticker, denom, or token hash must be specified"):
            config.get_chain(name="osmosis", id="osmosis-1")

    def test_get_host_chain(self):
        """Tests the get_host_chain lookup"""
        config = _parse_raw_configs(self.raw_config, self.raw_secrets)

        # Test looking up a valid host zone
        host_chain = config.get_host_chain(name="osmosis")
        assert host_chain.id == "osmosis-1"
        assert isinstance(host_chain, HostChainConfig)

        # Test looking up stride (should fail)
        with pytest.raises(TypeError, match="Chain stride is not a host zone"):
            config.get_host_chain(name="stride")

        # Test looking up an app chain (should fail)
        with pytest.raises(TypeError, match="Chain neutron is not a host zone"):
            config.get_host_chain(name="neutron")

        # Test looking up non-existent chain
        with pytest.raises(KeyError, match="No chain found for the given parameter"):
            config.get_host_chain(name="non-existent")
