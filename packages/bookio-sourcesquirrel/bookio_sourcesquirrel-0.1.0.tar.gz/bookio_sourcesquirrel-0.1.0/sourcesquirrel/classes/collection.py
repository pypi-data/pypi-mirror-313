from datetime import date
from typing import List, Optional
from uuid import UUID

from sourcesquirrel import validators
from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.classes.media_type import MediaType
from sourcesquirrel.classes.release_type import ReleaseType
from sourcesquirrel.classes.series import Series


class Collection:
    def __init__(
        self,
        id: UUID,
        title: str,
        onchain_collection_id: str,
        onchain_collection_id_mainnet: str,
        is_public_domain: bool,
        release_date: date,
        supply: int,
        cover_count: int,
        one_to_one_count: int,
        source_royalties: float,
        team_royalties: float,
        blockchain: Blockchain,
        media_type: MediaType,
        release_type: ReleaseType,
        onchain_discriminator: str = None,
        authors: List[str] = None,
        publishers: List[str] = None,
        series: List[Series] = None,
    ):
        self.id: UUID = id
        self.title: str = title
        self.onchain_collection_id: str = onchain_collection_id
        self.onchain_collection_id_mainnet: str = onchain_collection_id_mainnet
        self.is_public_domain: bool = is_public_domain
        self.release_date: date = release_date
        self.supply: int = supply
        self.cover_count: int = cover_count
        self.one_to_one_count: int = one_to_one_count
        self.source_royalties: float = source_royalties
        self.team_royalties: float = team_royalties
        self.blockchain: Blockchain = blockchain
        self.media_type: MediaType = media_type
        self.release_type: ReleaseType = release_type
        self.onchain_discriminator: Optional[str] = onchain_discriminator
        self.authors: List[str] = authors or []
        self.publishers: List[str] = publishers or []
        self.series: List[Series] = series or []

    def validate(self):
        blockchain_name = self.blockchain.name

        if not validators.is_collection_id(blockchain_name, self.onchain_collection_id):
            raise ValueError(f"Invalid onchain_collection_id for blockchain {str(self)}")

        if not validators.is_collection_id(blockchain_name, self.onchain_collection_id_mainnet):
            raise ValueError(f"Invalid onchain_collection_id_mainnet for blockchain {str(self)}")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.media_type.emoji} {self.title} ({self.blockchain.name})"
