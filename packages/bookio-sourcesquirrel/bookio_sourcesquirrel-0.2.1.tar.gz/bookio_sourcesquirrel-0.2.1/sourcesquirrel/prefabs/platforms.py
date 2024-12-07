from sourcesquirrel.classes.platform import Platform
from sourcesquirrel.constants import platforms as p

BOOK_IO = Platform(p.BOOK_IO)
STUFF_IO = Platform(p.STUFF_IO)

PLATFORMS = {
    p.BOOK_IO: BOOK_IO,
    p.STUFF_IO: STUFF_IO,
}


def get(name: str) -> Platform:
    return PLATFORMS.get(name)
