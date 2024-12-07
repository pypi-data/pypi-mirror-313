from typing import Tuple, Optional


def split_asset_id(asset_id: str) -> Tuple[str, str, Optional[str]]:
    try:
        return asset_id[:56], asset_id[56:], bytes.fromhex(asset_id[56:]).decode()
    except UnicodeDecodeError:
        return asset_id[:56], asset_id[56:], None
