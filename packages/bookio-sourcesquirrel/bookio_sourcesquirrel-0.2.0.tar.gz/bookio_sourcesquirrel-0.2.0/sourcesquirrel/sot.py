import logging
from typing import Iterable, List

from sourcesquirrel import excel
from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.classes.collection import Collection
from sourcesquirrel.classes.media_type import MediaType
from sourcesquirrel.classes.platform import Platform
from sourcesquirrel.classes.release_type import ReleaseType
from sourcesquirrel.classes.series import Series
from sourcesquirrel.integrations.google.drive import GoogleDriveClient
from sourcesquirrel.prefabs import blockchains, media_types, platforms, release_types

logger = logging.getLogger(__name__)


class SourceOfTruth:
    def __init__(self, collections: List[Collection], series: List[Series]):
        self.collections: List[Collection] = collections
        self.series: List[Series] = series

    @property
    def blockchains(self) -> Iterable[Blockchain]:
        return list(blockchains.BLOCKCHAINS.values())

    @property
    def media_types(self) -> Iterable[MediaType]:
        return list(media_types.MEDIA_TYPES.values())

    @property
    def platforms(self) -> Iterable[Platform]:
        return list(platforms.PLATFORMS.values())

    @property
    def release_types(self) -> Iterable[ReleaseType]:
        return list(release_types.RELEASE_TYPES.values())

    def verify(self):
        logger.info("blockchains")

        self.verify_blockchains()
        self.verify_collections()
        self.verify_media_types()
        self.verify_platforms()
        self.verify_release_types()
        self.verify_series()

    def verify_blockchains(self):
        logger.info("blockchains")

        for blockchain in self.blockchains:
            try:
                blockchain.verify()
                logger.info("* %s", blockchain)
            except Exception as e:
                raise ValueError(f"Error verifying blockchain {blockchain.id}: {e}")

    def verify_collections(self):
        logger.info("collections")

        for collection in self.collections:
            try:
                collection.verify()
                logger.info("* %s", collection)
            except Exception as e:
                raise ValueError(f"Error verifying collection {collection.id}: {e}")

            try:
                for serie in collection.series:
                    serie.verify()
                    logger.info("  - %s", serie)
            except Exception as e:
                raise ValueError(f"Error verifying collection {collection.id} series: {e}")

    def verify_media_types(self):
        logger.info("media_types")

        for media_type in self.media_types:
            try:
                media_type.verify()
                logger.info("* %s", media_type)
            except Exception as e:
                raise ValueError(f"Error verifying media_type {media_type.id}: {e}")

    def verify_platforms(self):
        logger.info("platforms")

        for platform in self.platforms:
            try:
                platform.verify()
                logger.info("* %s", platform)
            except Exception as e:
                raise ValueError(f"Error verifying platform {platform.id}: {e}")

    def verify_release_types(self):
        logger.info("release_types")

        for release_type in self.release_types:
            try:
                release_type.verify()
                logger.info("* %s", release_type)
            except Exception as e:
                raise ValueError(f"Error verifying release_type {release_type.id}: {e}")

    def verify_series(self):
        logger.info("series")
        for serie in self.series:
            try:
                serie.verify()
                logger.info("* %s", serie)
            except Exception as e:
                raise ValueError(f"Error verifying serie {serie.id}: {e}")

    @staticmethod
    def load_xlsx(path: str) -> "SourceOfTruth":
        series = {s.slug: s for s in excel.load_series(path)}
        collections = [c for c in excel.load_collections(path, series)]

        return SourceOfTruth(collections, list(series.values()))

    @staticmethod
    def load_from_drive(
        google_secrets_json: str,
        file_drive_id: str,
        file_path: str = "/tmp/sot.xlsx",
    ) -> "SourceOfTruth":
        client = GoogleDriveClient.from_google_secrets_json(google_secrets_json)
        client.download(file_drive_id, file_path)

        return SourceOfTruth.load_xlsx(file_path)
