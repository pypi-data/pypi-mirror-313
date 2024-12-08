from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.constants import blockchains as b
from sourcesquirrel.constants import cryptocurrencies as c

ALGORAND = Blockchain(b.ALGORAND, c.ALGO)
CARDANO = Blockchain(b.CARDANO, c.ADA)
COINBASE = Blockchain(b.COINBASE, c.BASE)
ETHEREUM = Blockchain(b.ETHEREUM, c.ETH)
POLYGON = Blockchain(b.POLYGON, c.POL)

BLOCKCHAINS = {
    b.ALGORAND: ALGORAND,
    b.CARDANO: CARDANO,
    b.COINBASE: COINBASE,
    b.ETHEREUM: ETHEREUM,
    b.POLYGON: POLYGON,
}


def get(name: str) -> Blockchain:
    return BLOCKCHAINS[name]
