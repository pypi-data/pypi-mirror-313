from typing import Optional

from mach_client import (
    Account,
    AccountID,
    Chain,
    account as account_factory,
)
from mach_client.chain import EthereumChain, SolanaChain, TronChain


class AccountManager:
    def __init__(
        self,
        *,
        ethereum: Optional[str] = None,
        solana: Optional[str] = None,
        tron: Optional[str] = None,
    ) -> None:
        self.private_keys: dict[type, Optional[str]] = {
            EthereumChain: ethereum,
            SolanaChain: solana,
            TronChain: tron,
        }

    def get(self, chain: Chain) -> Optional[Account]:
        chain_type = type(chain)

        if not (private_key := self.private_keys.get(chain_type)):
            return None

        return account_factory.create_account(chain, private_key)

    def __getitem__(self, chain: Chain) -> Account:
        if not (account := self.get(chain)):
            raise KeyError(f"No private key for {chain}")

        return account


class AccountIDManager:
    def __init__(
        self,
        *,
        ethereum: Optional[str] = None,
        solana: Optional[str] = None,
        tron: Optional[str] = None,
    ) -> None:
        self.addresses: dict[type, Optional[str]] = {
            EthereumChain: ethereum,
            SolanaChain: solana,
            TronChain: tron,
        }

    def get(self, chain: Chain) -> Optional[AccountID]:
        chain_type = type(chain)

        if not (address := self.addresses.get(chain_type)):
            return None

        return account_factory.create_account_id(chain, address)

    def __getitem__(self, chain: Chain) -> AccountID:
        if not (account_id := self.get(chain)):
            raise KeyError(f"No address for {chain}")

        return account_id
