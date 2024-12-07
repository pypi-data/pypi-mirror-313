from sourcesquirrel.classes.release_type import ReleaseType
from sourcesquirrel.constants import emojis as e
from sourcesquirrel.constants import release_types as rt

AIRDROP = ReleaseType(rt.AIRDROP, e.PARACHUTE)
FLASH = ReleaseType(rt.FLASH, e.LIGHTNING)
GIVEAWAY = ReleaseType(rt.GIVEAWAY, e.GIFT)
MINT = ReleaseType(rt.MINT, e.COIN)
SALE = ReleaseType(rt.SALE, e.MONEY)
SPECIAL = ReleaseType(rt.SPECIAL, e.STAR)
SUBSCRIPTION = ReleaseType(rt.SUBSCRIPTION, e.CALENDAR)

RELEASE_TYPES = {
    rt.AIRDROP: AIRDROP,
    rt.FLASH: FLASH,
    rt.GIVEAWAY: GIVEAWAY,
    rt.MINT: MINT,
    rt.SALE: SALE,
    rt.SPECIAL: SPECIAL,
    rt.SUBSCRIPTION: SUBSCRIPTION,
}


def get(name: str) -> ReleaseType:
    return RELEASE_TYPES.get(name)
