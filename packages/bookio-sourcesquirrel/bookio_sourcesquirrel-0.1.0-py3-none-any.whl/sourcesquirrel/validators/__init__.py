from sourcesquirrel.constants.blockchains import ALGORAND, CARDANO, COINBASE, ETHEREUM, POLYGON
from . import algorand, cardano, evm


def is_collection_id(blockchain_name: str, value: str) -> bool:
    if blockchain_name == ALGORAND:
        return algorand.is_address(value)
    if blockchain_name == CARDANO:
        return cardano.is_policy_id(value)
    if blockchain_name in (COINBASE, ETHEREUM, POLYGON):
        return evm.is_address(value)

    raise ValueError(f"Unknown blockchain: {blockchain_name}")
