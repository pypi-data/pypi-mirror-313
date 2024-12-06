from typing import Iterable, List
import os

from sourcesquirrel import excel
from sourcesquirrel.classes.blockchain import Blockchain
from sourcesquirrel.classes.collection import Collection
from sourcesquirrel.classes.media_type import MediaType
from sourcesquirrel.classes.platform import Platform
from sourcesquirrel.classes.release_type import ReleaseType
from sourcesquirrel.classes.series import Series
from sourcesquirrel.integrations.google.drive import GoogleDriveClient
from sourcesquirrel.prefabs import blockchains, media_types, platforms, release_types


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
