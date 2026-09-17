from src.domain.models import LoadedDocument
from src.ingestion.base import BaseLoader


class VideoLoader(BaseLoader):
    """
    Stub — extend later with whisper / ffmpeg transcription.
    """

    def supports(self, source_type: str) -> bool:
        return source_type == "video"

    def load(self, source: str, **kwargs) -> list[LoadedDocument]:
        raise NotImplementedError(
            "VideoLoader is not implemented yet. Add whisper or ffmpeg support."
        )