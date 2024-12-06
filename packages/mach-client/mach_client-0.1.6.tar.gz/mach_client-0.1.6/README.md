# mach-client-py

A (mostly) strongly typed Python client for the Mach exchange, including multichain abstractions for interacting with each network.

## Getting Started

Create a copy of the `template.config.yaml` file:

```bash
cp template.config.yaml config.yaml
```

Edit the config to add the credentials for the account you wish to run the example with:

```yaml
mach_client:
  secrets:
    ethereum: "YOUR PRIVATE KEY"
# ...
```

Then look at the notebook in the `examples/` directory.

## Adding a Chain

**Case 1:** The chain is an L2/testnet of a chain that's already supported

The code is roughly broken up into different networks, so adding an L2 or testnet of a network that is already supported just means updating the `chains/constants.py` file:

- [ ] Add the chain to the `SupportedChain` enum
- [ ] Add the chain's name (ie. what you want to be displayed by `str()`) to `CHAIN_NAMES`
- [ ] Add the chain's LayerZero EID to `LAYERZERO_IDS`. Refer to the [deployments](https://github.com/tristeroresearch/cache-half-full/blob/tron-test/config/deployments.json) file. Note that at the time of writing, only Tron uses LayerZero V2, and all other chains use V1.
- [ ] Add the name the chain is referred to with in the Mach backend to the `MACH_NAME_TO_CHAIN` dict. Refer to the [deployments](https://github.com/tristeroresearch/cache-half-full/blob/tron-test/config/deployments.json) file.
- [ ] Add the chain's scanner to `scanners/`. If the scanner is [EIP-3091](https://eips.ethereum.org/EIPS/eip-3091) compliant, just add the chain and the base URL of its scanner to the `chains/eip3091.py:SCANNER_URLS` dict.
- [ ] Add an entry in `template.config.yaml` for the endpoint URI of the chain
- [ ] Add tests

**Case 2:** The chain is on a brand new network

- [ ] Subclass `Chain` under `chain/` to represent the new chain. Then update the `Chain.from_id()` factory method.
- [ ] Do all the steps from Case 1
- [ ] Subclass the `AccountID` and `Account` classes under `account/` to create a proxy for the chain's public and private keys. Then update the factory functions in `account/__init__.py`.
- [ ] Subclass the `ChainClient` class to create a proxy for the client/connection to the chain. Then update the `_create` factory function in `chain_client/__init__.py`.
- [ ] Subclass the `Transaction` and `SentTransaction` classes under `transaction/` to create a proxy for the chain's transactions and sent/broadcasted transactions.
- [ ] Subclass the `Token` or `ApprovableToken` classes undero `asset/` to create a proxy for the chain's fungible token standard. Then update the `register_token` function in `asset/__init__.py`.
- [ ] Update the `client/order_book.py:create_place_order_transaction` function
