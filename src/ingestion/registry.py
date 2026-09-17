from src.core.enums import SourceType
from src.ingestion.base import BaseLoader
from src.ingestion.loaders.file_loader import FileLoader
from src.ingestion.loaders.image_loader import ImageLoader
from src.ingestion.loaders.url_loader import UrlLoader
from src.ingestion.loaders.video_loader import VideoLoader
from src.ingestion.loaders.zip_loader import ZipLoader

LOADERS: dict[SourceType, BaseLoader] = {
    SourceType.FILE: FileLoader(),
    SourceType.TEXT: FileLoader(),
    SourceType.URL: UrlLoader(),
    SourceType.PAGE: UrlLoader(),
    SourceType.ZIP: ZipLoader(),
    SourceType.IMAGE: ImageLoader(),
    SourceType.VIDEO: VideoLoader(),
}


def get_loader(source_type: SourceType) -> BaseLoader:
    loader = LOADERS.get(source_type)
    if loader is None:
        raise ValueError(f"No loader registered for source type: {source_type}")
    return loader