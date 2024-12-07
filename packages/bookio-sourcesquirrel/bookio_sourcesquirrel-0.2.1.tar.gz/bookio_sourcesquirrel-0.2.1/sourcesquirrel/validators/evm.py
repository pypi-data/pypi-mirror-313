from sourcesquirrel.validators.utils import check


ADDRESS_REGEX = r"^0x[a-fA-F0-9]{40}$"
ASSET_ID_REGEX = r"^[0-9]+$"
ENS_DOMAIN_REGEX = r"^[a-z0-9]+([\-\.][a-z0-9]+)*\.eth$"


def is_address(string: str) -> bool:
    return check(ADDRESS_REGEX, string)


def is_asset_id(string: str) -> bool:
    return check(ASSET_ID_REGEX, string)


def is_ens_domain(string: str) -> bool:
    return check(ENS_DOMAIN_REGEX, string)


def is_account(wallet: str) -> bool:
    return is_address(wallet) or is_ens_domain(wallet)
