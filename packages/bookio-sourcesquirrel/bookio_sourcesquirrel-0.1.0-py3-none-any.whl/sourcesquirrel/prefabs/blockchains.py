from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.constants import blockchains as b
from sourcesquirrel.constants import cryptocurrencies as c

ALGORAND = Blockchain(b.ALGORAND, c.ALGO, 4030)
CARDANO = Blockchain(b.CARDANO, c.ADA, 2010)
COINBASE = Blockchain(b.COINBASE, c.BASE, 27789)
ETHEREUM = Blockchain(b.ETHEREUM, c.ETH, 1027)
POLYGON = Blockchain(b.POLYGON, c.POL, 3890)

BLOCKCHAINS = {
    b.ALGORAND: ALGORAND,
    b.CARDANO: CARDANO,
    b.COINBASE: COINBASE,
    b.ETHEREUM: ETHEREUM,
    b.POLYGON: POLYGON,
}


def get(name: str) -> Blockchain:
    return BLOCKCHAINS[name]
