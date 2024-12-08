from typing import Optional
from uuid import UUID

from sourcesquirrel.classes.platform import Platform
from sourcesquirrel.helpers import required, optional


class MediaType:
    def __init__(self, id: UUID, name: str, emoji: str, platform: Platform = None):
        self.id: UUID = id
        self.name: str = name
        self.emoji: str = emoji
        self.platform: Optional[Platform] = platform

    def verify(self) -> bool:
        required("media_type.id", self.id, UUID)
        required("media_type.name", self.name, str)
        required("media_type.emoji", self.emoji, str)
        optional("media_type.platform", self.platform, Platform)

        if self.platform:
            self.platform.verify()

    def __str__(self) -> str:  # pragma: no cover
        if self.platform is None:
            return f"{self.emoji} {self.name}"

        return f"{self.emoji} {self.name} ({self.platform.name})"
