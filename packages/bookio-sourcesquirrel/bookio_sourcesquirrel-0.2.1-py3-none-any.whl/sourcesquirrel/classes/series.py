from uuid import UUID

from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.helpers import required


class Series:
    def __init__(self, id: UUID, name: str, slug: str, emoji: str, blockchain: Blockchain):
        self.id: UUID = id
        self.name: str = name
        self.slug: str = slug
        self.emoji: str = emoji
        self.blockchain: Blockchain = blockchain

    def verify(self):
        required("series.id", self.id, UUID)
        required("series.name", self.name, str)
        required("series.slug", self.slug, str)
        required("series.emoji", self.emoji, str)
        required("series.blockchain", self.blockchain, Blockchain)

        self.blockchain.verify()

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.emoji} {self.name} ({self.blockchain.name})"
