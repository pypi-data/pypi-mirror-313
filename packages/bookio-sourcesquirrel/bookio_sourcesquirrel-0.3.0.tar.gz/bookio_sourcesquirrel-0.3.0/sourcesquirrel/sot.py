import logging
from typing import Iterable, List, Any

from sourcesquirrel import excel
from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.classes.collection import Collection
from sourcesquirrel.classes.media_type import MediaType
from sourcesquirrel.classes.platform import Platform
from sourcesquirrel.classes.release_type import ReleaseType
from sourcesquirrel.classes.serie import Serie
from sourcesquirrel.integrations.google.drive import GoogleDriveClient
from sourcesquirrel.prefabs import blockchains, platforms

logger = logging.getLogger(__name__)


class SourceOfTruth:
    def __init__(
        self,
        collections: List[Collection],
        series: List[Serie],
        media_types: List[MediaType],
        release_types: List[ReleaseType],
    ):
        self.collections: List[Collection] = collections
        self.series: List[Serie] = series
        self.media_types: List[MediaType] = media_types
        self.release_types: List[ReleaseType] = release_types

    @property
    def blockchains(self) -> Iterable[Blockchain]:
        return list(blockchains.BLOCKCHAINS.values())

    @property
    def platforms(self) -> Iterable[Platform]:
        return list(platforms.PLATFORMS.values())

    def verify(self):
        logger.info("blockchains")

        self.verify_helper("blockchain", self.blockchains)
        self.verify_helper("collection", self.collections)
        self.verify_helper("media_type", self.media_types)
        self.verify_helper("platform", self.platforms)
        self.verify_helper("release_type", self.release_types)
        self.verify_helper("serie", self.series)

    def verify_helper(self, name: str, items: List[Any]):
        logger.info(f"{name}s")

        ids = set()

        for item in items:
            if item.id in ids:
                raise ValueError(f"Duplicate {name} id: {item.id}")

            try:
                item.verify()
                ids.add(item.id)

                logger.info("* %s", item)
            except Exception as e:
                raise ValueError(f"Error verifying {name} {item.id}: {e}")

        pass

    @staticmethod
    def load_xlsx(path: str) -> "SourceOfTruth":
        series = {s.slug: s for s in excel.load_series(path)}
        media_types = {mt.name: mt for mt in excel.load_media_types(path)}
        release_types = {rt.name: rt for rt in excel.load_release_types(path)}
        collections = [c for c in excel.load_collections(path, series, media_types, release_types)]

        return SourceOfTruth(
            collections=collections,
            series=list(series.values()),
            media_types=list(media_types.values()),
            release_types=list(release_types.values()),
        )

    @staticmethod
    def load_from_drive(
        file_drive_id: str,
        file_path: str = "/tmp/sot.xlsx",
        google_secrets_json: str = None,
        google_secrets_path: str = None,
    ) -> "SourceOfTruth":
        if google_secrets_json:
            client = GoogleDriveClient.from_google_secrets_json(google_secrets_json)
        elif google_secrets_path:
            client = GoogleDriveClient.from_google_secrets_path(google_secrets_path)
        else:
            raise ValueError("Missing Google secrets")

        client.download(file_drive_id, file_path)

        return SourceOfTruth.load_xlsx(file_path)
