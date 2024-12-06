from typing import Optional

from sourcesquirrel.classes.platform import Platform


class MediaType:
    def __init__(self, name: str, emoji: str, platform: Platform = None):
        self.name: str = name
        self.emoji: str = emoji
        self.platform: Optional[Platform] = platform

    def __str__(self) -> str:  # pragma: no cover
        if self.platform is None:
            return f"{self.emoji} {self.name}"

        return f"{self.emoji} {self.name} ({self.platform.name})"
