from typing import Optional

from mach_client import AccountID, Chain, MachClient, Token


async def choose_source_token(
    client: MachClient,
    token_choices: dict[Chain, set[Token]],
    account_id: AccountID,
) -> Token:
    balances = await client.get_token_balances(account_id)

    max_balance_token: Optional[tuple[int, Token]] = None

    # Choose the token with the greatest balance (regardless of denomination)
    for chain, tokens in token_choices.items():
        if chain not in balances:
            continue

        for token, balance in filter(
            lambda token_balances: token_balances[0] in tokens,
            balances[chain].items(),
        ):
            if not max_balance_token or max_balance_token[0] < balance:
                max_balance_token = (balance, token)

    if not max_balance_token:
        raise RuntimeError("No viable source tokens to choose from")

    return max_balance_token[1]
