from decimal import Decimal
from importlib import resources
import os
from pathlib import Path

from mach_client import SupportedChain
from mach_client import config as client_config
import yaml


config_path = Path(os.environ.get("CONFIG_PATH", "config.yaml"))
with open(config_path) as config_file:
    config: dict = yaml.safe_load(config_file)["mach_cctt"]


# Trades on these chains will not be considered
excluded_chains = frozenset(
    (
        SupportedChain.BLAST.value,
        SupportedChain.CELO.value,
        SupportedChain.ETHEREUM.value,
        SupportedChain.MODE.value,
        SupportedChain.POLYGON.value,
    )
)

# Relative to the root of the repository
abi_path = resources.files("abi")

solidity_uint_max = 2**256 - 1

# Default logger
log_file = Path("logs") / "app.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

aave_symbols = frozenset[str](config["aave"]["symbols"])

aave_supply_duration: int = config["aave"]["supplyDuration"]

aave_rebalance_threshold = Decimal(config["aave"]["rebalanceThreshold"])

aave_pool_addresses_provider = {
    SupportedChain.ETHEREUM.value: "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e",
    SupportedChain.OPTIMISM.value: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    SupportedChain.BNB.value: "0xff75B6da14FfbbfD355Daf7a2731456b3562Ba6D",
    SupportedChain.POLYGON.value: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    # SupportedChain.OPBNB.value
    # SupportedChain.MANTLE.value
    SupportedChain.BASE.value: "0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D",
    # SupportedChain.MODE.value
    SupportedChain.ARBITRUM.value: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    # SupportedChain.CELO.value
    SupportedChain.AVALANCHE_C_CHAIN.value: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    # SupportedChain.BLAST.value
    SupportedChain.SCROLL.value: "0x69850D0B276776781C063771b161bd8894BCdD04",
}

aave_pool_addresses_provider_abi = client_config.load_abi(
    abi_path / "aave" / "pool_addresses_provider.json"
)

aave_protocol_data_provider_abi = client_config.load_abi(
    abi_path / "aave" / "protocol_data_provider.json"
)

aave_pool_abi = client_config.load_abi(abi_path / "aave" / "pool.json")
