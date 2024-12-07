from sourcesquirrel.classes.media_type import MediaType
from sourcesquirrel.constants import emojis as e
from sourcesquirrel.constants import media_types as mt
from sourcesquirrel.prefabs.platforms import BOOK_IO, STUFF_IO

SPECIAL = MediaType(mt.SPECIAL, e.GEM, None)
SUBSCRIPTION = MediaType(mt.SUBSCRIPTION, e.ARROWS, None)

AUDIOBOOK = MediaType(mt.AUDIOBOOK, e.HEADPHONES, BOOK_IO)
BOOK = MediaType(mt.BOOK, e.BOOK, BOOK_IO)
CHAPTER = MediaType(mt.CHAPTER, e.MEMO, BOOK_IO)
COMIC = MediaType(mt.COMIC, e.TEXT_BUBBLE, BOOK_IO)
DOCUMENT = MediaType(mt.DOCUMENT, e.PAGE, BOOK_IO)

ALBUM = MediaType(mt.ALBUM, e.CD, STUFF_IO)
MOVIE = MediaType(mt.MOVIE, e.FILM, STUFF_IO)
MUSIC = MediaType(mt.MUSIC, e.MUSICAL_NOTE, STUFF_IO)
PODCAST = MediaType(mt.PODCAST, e.MICROPHONE, STUFF_IO)
VIDEO = MediaType(mt.VIDEO, e.VCR, STUFF_IO)

MEDIA_TYPES = {
    mt.ALBUM: ALBUM,
    mt.AUDIOBOOK: AUDIOBOOK,
    mt.BOOK: BOOK,
    mt.CHAPTER: CHAPTER,
    mt.COMIC: COMIC,
    mt.DOCUMENT: DOCUMENT,
    mt.MOVIE: MOVIE,
    mt.MUSIC: MUSIC,
    mt.PODCAST: PODCAST,
    mt.SPECIAL: SPECIAL,
    mt.SUBSCRIPTION: SUBSCRIPTION,
    mt.VIDEO: VIDEO,
}


def get(name: str) -> MediaType:
    return MEDIA_TYPES[name]
