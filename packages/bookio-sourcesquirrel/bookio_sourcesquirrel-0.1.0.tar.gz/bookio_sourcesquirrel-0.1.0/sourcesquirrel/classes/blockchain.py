from typing import Optional


class Blockchain:
    def __init__(self, name: str, currency: str, coinmarketcap_id: int = None):
        self.name: str = name
        self.currency: str = currency

        self.coinmarketcap_id: Optional[int] = coinmarketcap_id

    def logo_url(self) -> str:  # pragma: no cover
        return f"https://s2.coinmarketcap.com/static/img/coins/64x64/{self.coinmarketcap_id}.png"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.currency})"
