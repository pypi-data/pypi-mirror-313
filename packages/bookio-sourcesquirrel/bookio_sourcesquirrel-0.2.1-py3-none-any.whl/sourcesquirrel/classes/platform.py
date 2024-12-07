from sourcesquirrel.helpers import required


class Platform:
    def __init__(self, name: str):
        self.id: str = name
        self.name: str = name

    @property
    def url(self) -> str:
        return f"https://{self.name}"

    def verify(self):
        required("platform.name", self.name, str)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
