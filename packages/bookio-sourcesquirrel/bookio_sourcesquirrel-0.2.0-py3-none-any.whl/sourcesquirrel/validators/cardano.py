from sourcesquirrel.validators.utils import check

HANDLE_REGEX = r"?:^\$[a-z0-9_.-]{1,15}$"
SUBHANDLE_REGEX = r"?:^\$(?!.{29})[a-z0-9_.-]+@[a-z0-9_.-]{1,15}$"

ADA_HANDLE_REGEX = rf"({HANDLE_REGEX})|({SUBHANDLE_REGEX})"

ASSET_ID_REGEX = r"^[a-f0-9]{56}[a-fA-F0-9]+$"
POLICY_ID_REGEX = r"^[a-f0-9]{56}$"

SHORT_ADDRESS_REGEX = r"^addr1[0-9a-z]{53}$"
LONG_ADDRESS_REGEX = r"^addr1[0-9a-z]{98}$"
PREPROD_SHORT_ADDRESS_REGEX = r"^addr_test1[0-9a-z]{53}$"
PREPROD_LONG_ADDRESS_REGEX = r"^addr_test1[0-9a-z]{98}$"

STAKE_ADDRESS_REGEX = r"^stake1[0-9a-z]{53}$"
PREPROD_STAKE_ADDRESS_REGEX = r"^stake_test1[0-9a-z]{53}$"


def is_ada_handle(string: str) -> bool:
    return check(ADA_HANDLE_REGEX, string)


def is_address(string) -> bool:
    if check(SHORT_ADDRESS_REGEX, string):
        return True

    return check(LONG_ADDRESS_REGEX, string)


def is_preprod_address(string) -> bool:
    if check(PREPROD_SHORT_ADDRESS_REGEX, string):
        return True

    return check(PREPROD_LONG_ADDRESS_REGEX, string)


def is_asset_id(string: str) -> bool:
    return check(ASSET_ID_REGEX, string)


def is_policy_id(string: str) -> bool:
    return check(POLICY_ID_REGEX, string)


def is_stake_address(string: str) -> bool:
    return check(STAKE_ADDRESS_REGEX, string)


def is_preprod_stake_address(string: str) -> bool:
    return check(PREPROD_STAKE_ADDRESS_REGEX, string)


def is_account(wallet: str) -> bool:
    return is_stake_address(wallet) or is_address(wallet) or is_ada_handle(wallet)


def is_preprod_account(wallet: str) -> bool:
    return is_preprod_stake_address(wallet) or is_preprod_address(wallet) or is_ada_handle(wallet)
