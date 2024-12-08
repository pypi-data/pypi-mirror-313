from sourcesquirrel.constants.blockchains import ALGORAND, CARDANO, COINBASE, ETHEREUM, POLYGON
from sourcesquirrel.helpers import required
from sourcesquirrel.validators import algorand, cardano, evm


class Blockchain:
    def __init__(self, name: str, currency: str):
        self.id: str = name
        self.name: str = name
        self.currency: str = currency

    def is_collection_id(self, collection_id: str) -> bool:
        if self.name == ALGORAND:
            return algorand.is_address(collection_id)
        elif self.name == CARDANO:
            return cardano.is_policy_id(collection_id)
        elif self.name in (COINBASE, ETHEREUM, POLYGON):
            return evm.is_address(collection_id)
        else:
            raise ValueError(f"Unknown blockchain: {self.name}")

    def verify(self):
        required("blockchain.name", self.name, str)
        required("blockchain.currency", self.currency, str)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.currency})"
