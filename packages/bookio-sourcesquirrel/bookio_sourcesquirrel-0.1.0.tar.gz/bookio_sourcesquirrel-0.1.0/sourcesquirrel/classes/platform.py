class Platform:
    def __init__(self, name: str):
        self.name: str = name

    @property
    def url(self) -> str:
        return f"https://{self.name}"

    def __str__(self) -> str:  # pragma: no cover
        return self.name
