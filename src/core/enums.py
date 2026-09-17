import enum


class SourceType(str, enum.Enum):
    FILE = "file"
    URL = "url"
    PAGE = "page"
    ZIP = "zip"
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    

class IngestionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    

class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    INDEXED = "indexed"
    FAILED = "failed"