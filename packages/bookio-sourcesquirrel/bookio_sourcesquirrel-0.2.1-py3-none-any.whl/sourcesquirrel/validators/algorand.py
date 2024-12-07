from sourcesquirrel.validators.utils import check

ADDRESS_REGEX = r"^[A-Z2-7]{58}$"
ASSET_ID_REGEX = r"^[0-9]+$"
NF_DOMAIN_REGEX = r"^[a-z0-9]+([\-\.][a-z0-9]+)*\.algo$"


def is_address(string: str) -> bool:
    return check(ADDRESS_REGEX, string)


def is_asset_id(string: str) -> bool:
    return check(ASSET_ID_REGEX, string)


def is_nf_domain(string: str) -> bool:
    return check(NF_DOMAIN_REGEX, string)


def is_account(wallet: str) -> bool:
    return is_address(wallet) or is_nf_domain(wallet)
