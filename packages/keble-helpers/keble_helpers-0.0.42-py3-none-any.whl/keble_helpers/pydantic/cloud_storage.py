from pydantic import BaseModel
from .config import PydanticModelConfig
from enum import Enum
from typing import Optional
from ..common import is_mime_image, is_mime_video, is_mime_ms_excel, is_mime_csv


class CloudStorageType(str, Enum):
    AWS_S3 = "AWS_S3"
    ALIYUN_OSS = "ALIYUN_OSS"


class CloudStorageObjectType(str, Enum):
    IMAGE = "IMAGE",
    VIDEO = "VIDEO",
    EXCEL = "EXCEL",
    CSV = "CSV",
    OTHER = "OTHER"

    @classmethod
    def determine_type(cls, *, mime: str) -> "CloudStorageObjectType":
        mime = mime.lower()
        if is_mime_video(mime): return CloudStorageObjectType.VIDEO
        if is_mime_image(mime): return CloudStorageObjectType.IMAGE
        if is_mime_ms_excel(mime): return CloudStorageObjectType.EXCEL
        if is_mime_csv(mime): return CloudStorageObjectType.CSV
        return CloudStorageObjectType.OTHER



class CloudStorageBase(BaseModel):
    """Provide a universal CloudStorage Class for different
    cloud service platform"""

    model_config = PydanticModelConfig.default()

    # key for AWS is straightforward, for aliyun, it is name/or oss path.
    # they all refer as key
    key: str

    # endpoint of the cloud storage
    # base_url + key should be the URL of the cloud storage
    base_url: str

    # type of cloud service
    type: CloudStorageType

    # type of file
    object_type: CloudStorageObjectType

    # original file name
    original_file_name: Optional[str]
