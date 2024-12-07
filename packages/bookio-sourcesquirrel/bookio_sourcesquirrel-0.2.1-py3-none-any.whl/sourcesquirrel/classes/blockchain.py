from typing import Optional

from sourcesquirrel.constants.blockchains import ALGORAND, CARDANO, COINBASE, ETHEREUM, POLYGON
from sourcesquirrel.helpers import required, optional
from sourcesquirrel.validators import algorand, cardano, evm


class Blockchain:
    def __init__(self, name: str, currency: str, coinmarketcap_id: int = None):
        self.id: str = name
        self.name: str = name
        self.currency: str = currency

        self.coinmarketcap_id: Optional[int] = coinmarketcap_id

    def is_collection_id(self, collection_id: str) -> bool:
        if self.name == ALGORAND:
            return algorand.is_address(collection_id)
        elif self.name == CARDANO:
            return cardano.is_policy_id(collection_id)
        elif self.name in (COINBASE, ETHEREUM, POLYGON):
            return evm.is_address(collection_id)
        else:
            raise ValueError(f"Unknown blockchain: {self.name}")

    def logo_url(self) -> str:  # pragma: no cover
        return f"https://s2.coinmarketcap.com/static/img/coins/64x64/{self.coinmarketcap_id}.png"

    def verify(self):
        required("blockchain.name", self.name, str)
        required("blockchain.currency", self.currency, str)
        optional("blockchain.coinmarketcap_id", self.coinmarketcap_id, int)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.currency})"
