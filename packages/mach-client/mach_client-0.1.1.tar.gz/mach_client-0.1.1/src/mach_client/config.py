from __future__ import annotations
from decimal import Decimal
from importlib import resources
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel
import yaml

from .chain import Chain, constants


def add_backend_url[Model: BaseModel](model: Model, backend_url: str) -> Model:
    return type(model)(
        **{key: f"{backend_url}{value}" for key, value in model.model_dump().items()}
    )


class APIRoutes(BaseModel):
    orders: str
    order_status: str
    gas: str
    quotes: str
    points: str
    token_balances: str
    get_config: str
    get_all_tokens_from_db: str

    def add_backend_url(self, backend_url: str) -> APIRoutes:
        return add_backend_url(self, backend_url)


class TokenServerAPIRoutes(BaseModel):
    assets: str
    prices: str
    users: str

    def add_backend_url(self, backend_url: str) -> TokenServerAPIRoutes:
        return add_backend_url(self, backend_url)


config_path = Path(os.environ.get("CONFIG_PATH", "config.yaml"))
with open(config_path) as config_file:
    config: dict = yaml.safe_load(config_file)["mach_client"]


def load_abi(path: Traversable) -> Any:
    with path.open("r") as abi:
        return json.load(abi)


endpoint_uris: dict[Chain, str] = {
    Chain.from_id(*chain_id.split(":")): endpoint_uri
    for chain_id, endpoint_uri in config["chain_endpoint_uris"].items()
    if chain_id in constants.CHAIN_ID_TO_CHAIN
}

backend_url: str = config["backend"]["url"]
api_routes = APIRoutes.model_validate(config["backend"]["endpoints"])

token_server_url: str = config["tokenServer"]["url"]
token_server_api_routes = TokenServerAPIRoutes.model_validate(
    config["tokenServer"]["endpoints"]
)

# Only used for swaps between similar tokens (ie. WETH -> ETH, USDC -> USDT, etc.)
slippage_tolerance = Decimal(config["trading"]["slippageTolerance"])

# Default max time to wait for an order to be filled, or for it to be completed after being filled
default_wait_time = 300

# Relative to the root of the repository
abi_path = resources.files("abi")

order_book_abis = {
    chain: load_abi(abi_path / chain / "order_book.json")
    for chain in ("ethereum", "tron")
}

erc20_abi = load_abi(abi_path / "ethereum" / "erc20.json")
