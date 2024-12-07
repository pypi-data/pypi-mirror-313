from pydantic import BaseModel


class AliyunOssPutObjectResponse(BaseModel):
    # see https://help.aliyun.com/zh/oss/developer-reference/simple-upload-1?spm=a2c4g.11186623.0.i4
    status: int
    request_id: str
    etag: str
    headers: dict
