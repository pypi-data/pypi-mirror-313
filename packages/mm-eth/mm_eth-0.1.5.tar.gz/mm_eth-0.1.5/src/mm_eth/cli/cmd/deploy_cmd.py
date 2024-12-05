import yaml
from mm_std import print_json
from pydantic import StrictStr

from mm_eth import account, deploy
from mm_eth.cli import cli_helpers, cli_utils
from mm_eth.cli.cli_utils import BaseConfig


class Config(BaseConfig):
    private_key: StrictStr
    nonce: int | None = None
    gas: StrictStr
    max_fee_per_gas: str
    max_priority_fee_per_gas: str
    value: str | None = None
    contract_bin: StrictStr
    constructor_types: StrictStr = "[]"
    constructor_values: StrictStr = "[]"
    chain_id: int
    node: str


def run(config_path: str, *, print_config: bool) -> None:
    config = cli_utils.read_config(Config, config_path)
    if print_config:
        print_json(config.model_dump(exclude={"private_key"}))
        exit(0)

    constructor_types = yaml.full_load(config.constructor_types)
    constructor_values = yaml.full_load(config.constructor_values)

    sender_address = account.private_to_address(config.private_key)
    if sender_address is None:
        cli_utils.fatal("private address is wrong")

    nonce = cli_helpers.get_nonce(config.node, sender_address)
    if nonce is None:
        cli_utils.fatal("can't get nonce")

    deploy.get_deploy_contract_data(config.contract_bin, constructor_types, constructor_values)
