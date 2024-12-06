class ReleaseType:
    def __init__(self, name: str, emoji: str):
        self.name: str = name
        self.emoji: str = emoji

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.emoji} {self.name}"
