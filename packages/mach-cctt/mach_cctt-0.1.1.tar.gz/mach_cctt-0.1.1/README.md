# Cross Chain Trade Test (CCTT)

Test automated trades between multiple chains on Mach.

[PyPI](https://pypi.org/project/mach-cctt/)

[Test PyPI](https://test.pypi.org/project/mach-cctt/)

## Overview

Test automated trades on Mach. Specify a start chain and symbol, and a policy determining how the destination token will be chosen (randomize chain and symbol, randomize chain and fix symbol). In each trade, the test wallet's entire balance of the source token will be sold for the destination token, and then the destination token because the new source token for the next trade. This continues until the script is killed by the user.

## Usage

1. Install

    ```bash
    python -m pip install mach-cctt
    ```

1. Usage

    ```bash
    cctt --help
    ```

1. Example

    ```bash
    # The script will create log files and an account data file. Make a working directory for it.
    mkdir cctt/ && cd cctt/

    # Set password to avoid being prompted
    # export CCTT_PASSWORD="abc"

    # Backend defaults to production, change if necessary
    # export MACH_BACKEND_URL="https://cache-half-full-staging.fly.dev"
    
    cctt import # Import account
    cctt decrypt # Show public/private key
    cctt balances # Show account balances

    # Trade USDC on random chains, starting from optimism-USDC
    cctt run --source optimism-USDC --destination-policy fixed:USDC

    # Trade USDC on only arbitrum and optimism, starting from polygon-USDC
    cctt run --source polygon-USDC --destination-policy cheap:USDC

    # Trade between random tokens on random chains, starting from arbitrum-USDT
    cctt run --source arbitrum-USDT --destination-policy random
    
    # If the --source is empty, then an appropriate source with a non-zero balance is chosen for you.
    cctt run --source --destination-policy random
    ```

    Notes:

    - You need to have a gas on every chain, or a gas of exactly 0 on chains that you do not wish the testing script to trade on, which will cause those chains to be disabled.
    - The `--source` token should be one that you hold a non-zero balance of in your wallet. If you set it to empty, it will be automatically chosen as any token with a non-zero balance in the wallet.
    - There is a known issue with trades filling for a single tick less than the order was placed at. As a preventative measure, any token balance of 1 tick in the wallet is treated as an empty balance.

## Log Files

There are 4 log files created by the application:

- `app.log` - everything
- `delayed_transactions.log` - the source funds where not withdrawn in time
- `stuck_transactions.log` - the source funds were withdrawn but the destination funds were not received in time
- `improper_fill.log` - the trade filled on the source chain for 1 tick less than the order was placed for. This has been observed to happen primarily to USDM (on multiple chains)

## Account File

A plaintext JSON file storing your account encrypted with your password will be created once you first generate or import a wallet. By default this file is called `account.json` but you can give a path to your own file via the `--file PATH` flag. This file is required to be present for any operation other than importing or generating a new wallet.

## Development

### Requirements

You need the [`just`](https://github.com/casey/just) command runner and either Python 3.12.5+ with `virtualenv`, or `pyenv`.

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/tristeroresearch/cross-chain-trade-test.git
    cd cross-chain-trade-test
    ```

1. **Create and activate a virtual environment**

    Using `venv`:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    Or using `pyenv`:

    ```bash
    pyenv virtualenv 3.12.5 cctt
    pyenv activate
    ```

1. **Install dependencies**

    ```bash
    just init
    ```

1. **View available recipes**

    ```bash
    just -l
    ```

    Note that there are recipes that allow you to run the application in-source without needed to build and package to PyPI first:

    ```bash
    just account_file=account.json import <private key> # Import a new account
    just decrypt # Show public and private key
    just balances # List balances of account
    just source=arbitrum-USDC policy=random run # Run the trade tester, starting from arbitrum-USDC and trading to random tokens
    just wallet=<public key> withdraw # Withdraw funds from the stored account to the given wallet
    ```

1. **Building**

    ```bash
    just build
    ```

#### Packaging

Make sure to bump the version number in `pyproject.toml`.

To upload to the test PyPI:

```bash
just upload-test
```

To upload to the main PyPI:

```bash
just upload
```
