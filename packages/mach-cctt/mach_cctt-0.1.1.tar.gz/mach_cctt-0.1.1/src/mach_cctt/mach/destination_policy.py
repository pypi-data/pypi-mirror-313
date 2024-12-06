import abc
from abc import ABC
from collections import defaultdict
import pprint
import random
import typing
from typing import AbstractSet, Optional, Iterator

from mach_client import Chain, MachClient, SupportedChain, Token

from .. import config, log
from ..log import Logger


class DestinationPolicy(ABC):
    __slots__ = ("client", "token_choices", "tried_chains", "tried_tokens", "logger")

    def __init__(
        self,
        client: MachClient,
        initial_excluded_chains: AbstractSet[Chain] = config.excluded_chains,
        logger: Logger = log.logger,
    ):
        self.logger = logger
        self.client = client

        # Maps chain -> set of tradeable tokens on that chain
        self.token_choices = defaultdict[Chain, set[Token]](
            set,
            {
                chain: tokens
                for chain, tokens in client.tokens.items()
                if chain not in initial_excluded_chains
            },
        )

        # Items from self.token_choices that have been removed because the chain was excluded
        self.tried_chains: list[tuple[Chain, set[Token]]] = []

        # Specific tokens that have been excluded
        self.tried_tokens: list[Token] = []

    # Produce the destination token for the next trade
    @abc.abstractmethod
    def __call__(self) -> Optional[Token]:
        pass

    def __repr__(self) -> str:
        # These be huge and we don't want to pollute logs
        obj = {
            "token_choices": f"({len(self.token_choices)} tokens)",
            "tried_chains": [chain for chain, _ in self.tried_chains],
        }
        return f"{self.__class__.__name__}{pprint.pformat(obj)}"

    def permanently_exclude_chain(self, chain: Chain) -> None:
        self.token_choices.pop(chain, None)

    def exclude_chain(self, chain: Chain) -> None:
        if choices := self.token_choices.pop(chain, None):
            self.tried_chains.append((chain, choices))

    def exclude_token(self, token: Token) -> None:
        chain = token.chain

        self.token_choices[chain].remove(token)

        # Remove this chain if there are no tokens we can choose from it
        if not self.token_choices[chain]:
            self.token_choices.pop(chain)

        self.tried_tokens.append(token)

    # Reset for the next trade
    def reset(self) -> None:
        self.token_choices.update(self.tried_chains)
        self.tried_chains.clear()

        for token in self.tried_tokens:
            self.token_choices[token.chain].add(token)

        self.tried_tokens.clear()


class RandomChainFixedSymbolPolicy(DestinationPolicy):
    __slots__ = ("symbol",)

    def __init__(
        self,
        client: MachClient,
        symbol: str,
        initial_excluded_chains: AbstractSet[Chain] = config.excluded_chains,
    ):
        super().__init__(client, initial_excluded_chains)
        self.symbol = symbol

        for chain, tokens in self.token_choices.items():
            self.token_choices[chain] = {
                symbol for symbol in tokens if symbol == self.symbol
            }

            if not self.token_choices[chain]:
                self.token_choices.pop(chain)

    @typing.override
    def __call__(self) -> Optional[Token]:
        try:
            chain = random.choice(tuple(self.token_choices.keys()))
            token = random.choice(
                tuple(self.token_choices[chain])
            )  # Should always be self.symbol, but this way respects token exclusions
        except IndexError:
            self.logger.critical(
                "Unable to choose destination token - all choices have been excluded"
            )
            return None

        return token


class CheapChainFixedSymbolPolicy(RandomChainFixedSymbolPolicy):
    __slots__ = tuple()

    cheap_chains = frozenset(
        (SupportedChain.ARBITRUM.value, SupportedChain.OPTIMISM.value)
    )

    def __init__(self, client: MachClient, symbol: str):
        assert len(self.cheap_chains.intersection(client.chains)) == len(
            self.cheap_chains
        ), "Not all cheap chains supported by client!"

        super().__init__(
            client,
            symbol,
            client.chains - self.cheap_chains,
        )


class RandomChainRandomSymbolPolicy(DestinationPolicy):
    __slots__ = tuple()

    def __init__(self, client: MachClient):
        super().__init__(client)

    @typing.override
    def __call__(self) -> Optional[Token]:
        try:
            chain = random.choice(tuple(self.token_choices.keys()))
            token = random.choice(tuple(self.token_choices[chain]))
        except IndexError:
            self.logger.critical(
                "Unable to choose destination token - all choices have been excluded"
            )
            return None

        return token


class TokenIteratorPolicy(DestinationPolicy):
    __slots__ = ("tokens",)

    def __init__(self, client: MachClient, tokens: Iterator[Token]):
        super().__init__(client)
        self.tokens = tokens

    @typing.override
    def __call__(self) -> Optional[Token]:
        try:
            while True:
                token = next(self.tokens)

                if token.chain not in self.token_choices:
                    continue
                elif token not in self.token_choices[token.chain]:
                    self.logger.warning(
                        f"Token {token} in given list not a valid choice"
                    )
                    continue

                return token

        except StopIteration:
            return None
