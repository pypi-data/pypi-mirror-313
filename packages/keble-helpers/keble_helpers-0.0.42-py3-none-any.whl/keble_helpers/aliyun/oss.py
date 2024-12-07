import oss2
from typing import Optional
import urllib.request
from pydantic import BaseModel, Field, AnyHttpUrl
from .base import Aliyun
from ..pydantic import PydanticModelConfig
from .schemas import AliyunOssPutObjectResponse


# meta data for aliyun oss object, return from bucket.get_object_meta
class AliyunOssMeta(BaseModel):
    model_config = PydanticModelConfig.default()

    etag: Optional[str] = Field(None, description='Aliyun OSS etag')
    content_length: Optional[int] = Field(None, description='File size in bytes', serialization_alias="contentLength")
    last_modified: Optional[int] = Field(None, description='File size in bytes', serialization_alias="lastModified")
    content_type: Optional[str] = Field(None, description='MIME type of the file, e.g. img/jpeg',
                                        serialization_alias="contentType")


class AliyunOss(Aliyun):

    # Aliyun OSS upload requires STS+RAM user authentication
    # see: https://help.aliyun.com/zh/oss/developer-reference/use-the-accesskey-pair-of-a-ram-user-to-initiate-a-request

    def __init__(self, oss_endpoint: AnyHttpUrl, bucket: str, **kwargs):
        super().__init__(**kwargs)
        self.__oss_endpoint: str = str(oss_endpoint).strip("/ ")
        self.__bucket_name: str = bucket.strip("/ ")

    def get_bucket(self) -> oss2.Bucket:
        auth = oss2.Auth(self.access_key, self.secret)
        return oss2.Bucket(auth, self.__oss_endpoint, self.__bucket_name)

    def get_bucket_with_sts(self, sts_token: str):
        auth = oss2.StsAuth(self.access_key, self.secret, sts_token)
        return oss2.Bucket(auth, self.__oss_endpoint, self.__bucket_name)

    def get_object_meta(self, key: str) -> AliyunOssMeta:
        """Get an oss file metadata
        example key as oss path: some_folder/file.txt"""
        bucket = self.get_bucket()
        meta = bucket.head_object(key)
        return AliyunOssMeta(
            etag=meta.etag,
            content_length=meta.content_length,
            last_modified=meta.last_modified,
            content_type=meta.content_type
        )

    def save_object_to_local(self, key: str, local_path: str, *args, **kwargs):
        """Convert a file from oss path to local file
        key(as oss path) can be something like some_folder/file.txt"""
        bucket = self.get_bucket()
        bucket.get_object_to_file(key, local_path, *args, **kwargs)

    def save_local_to_cloud(self, key: str, local_path: str, *args, **kwargs):
        """Convert a file from oss path to local file
        key(as oss path) can be something like some_folder/file.txt"""
        bucket = self.get_bucket()
        res = bucket.put_object_from_file(key, local_path)
        return AliyunOssPutObjectResponse(
            status=res.status,
            request_id=res.request_id,
            etag=res.etag,
            headers=res.headers
        )


    def save_snapshot_to_local(self, key: str, local_path: str, seconds: int):
        """Get a snapshot file from an oss object.
         Use case: video snapshot"""
        bucket = self.get_bucket()

        signed_url = bucket.sign_url('GET', key, 10 * 60,
                                     params={'x-oss-process': f'video/snapshot,t_{seconds}000,f_jpg,w_0,h_0,m_fast'})
        urllib.request.urlretrieve(signed_url, local_path)

    def cold_archive_object(self, key: str):
        """Convert a file into cold archive status"""
        bucket = self.get_bucket()

        # change object by changing its header class
        headers = {'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_COLD_ARCHIVE}

        # override it by coping the object, from current path to the same current path
        bucket.copy_object(bucket.bucket_name, key, key, headers)

    def get_sts_signed_url(self, sts_token: str, key: str, *, expire_seconds: int = 60,
                           content_type: Optional[str] = None, oss_storage_class: Optional[str] = None) -> str:
        bucket = self.get_bucket_with_sts(sts_token)

        # 指定Header。
        headers = dict()
        # You can set fixed Content-Type by:
        if content_type is not None:
            headers['Content-Type'] = content_type  # sample value: 'text/txt'

        # or configure storage class
        if oss_storage_class is not None:
            headers["x-oss-storage-class"] = oss_storage_class  # sample value: "Standard"

        # URL will expire after expire_seconds/60 seconds
        # due to OSS url error, you need to set slash_safe as TRUE
        url = bucket.sign_url('GET', key, expire_seconds, slash_safe=True, headers=headers)
        return url
