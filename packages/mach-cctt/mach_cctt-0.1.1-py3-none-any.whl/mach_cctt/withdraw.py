import asyncio

from mach_client import Account, AccountID, MachClient, SupportedChain

from .account_manager import AccountManager, AccountIDManager


async def withdraw_network(
    client: MachClient,
    account: Account,
    recipient: AccountID,
) -> None:
    balances = await client.get_token_balances(account.downcast())

    # This has to be done sequentially to avoid nonce issues
    for chain_balances in balances.values():
        for token, balance in chain_balances.items():
            if balance <= 0:
                continue

            await token.transfer(
                sender=account,
                recipient=recipient,
                amount=balance,
            )


async def withdraw(
    client: MachClient,
    account_manager: AccountManager,
    recipients: AccountIDManager,
) -> None:
    chains = (
        SupportedChain.ETHEREUM.value,
        SupportedChain.SOLANA.value,
        # SupportedChain.TRON.value,
    )

    coros = []

    for chain in chains:
        account = account_manager.get(chain)
        recipient = recipients.get(chain)

        if not account or not recipient:
            continue

        coros.append(withdraw_network(client, account, recipient))

    await asyncio.gather(*coros)
