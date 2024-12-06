from uuid import UUID

from sourcesquirrel.classes.blockchain import Blockchain


class Series:
    def __init__(self, id: UUID, name: str, slug: str, emoji: str, blockchain: Blockchain):
        self.id: UUID = id
        self.name: str = name
        self.slug: str = slug
        self.emoji: str = emoji
        self.blockchain: Blockchain = blockchain

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.emoji} {self.name} ({self.blockchain.name})"
