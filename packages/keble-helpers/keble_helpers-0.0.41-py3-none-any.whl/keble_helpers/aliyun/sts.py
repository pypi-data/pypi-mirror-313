# coding=utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdksts.request.v20150401.AssumeRoleRequest import AssumeRoleRequest
import json
from .base import Aliyun
from pydantic import BaseModel
from ..pydantic import PydanticModelConfig

class AliyunStsToken(BaseModel):
    model_config = PydanticModelConfig.default()
    access_key_secret: str
    security_token: str
    access_key_id: str


class AliyunSts(Aliyun):

    def __init__(self, region, **kwargs):
        super().__init__(**kwargs)
        self.__region = region

    def get_sts(self, session_name: str, role_arn: str) -> AliyunStsToken:
        # 构建一个阿里云客户端，用于发起请求。
        # 设置调用者（RAM用户或RAM角色）的AccessKey ID和AccessKey Secret。
        client = AcsClient(self.access_key, self.secret, self.__region)

        request = AssumeRoleRequest()
        request.set_accept_format('json')

        # set role
        request.set_RoleArn(role_arn)

        # give a name to this session, this is depends on you. no strict requirement
        request.set_RoleSessionName(session_name)

        response = client.do_action_with_exception(request)
        response_dict = json.loads(response.decode('utf-8'))['Credentials']
        return AliyunStsToken(
            access_key_secret=response_dict['AccessKeySecret'],
            security_token=response_dict['SecurityToken'],
            access_key_id=response_dict['AccessKeyId'],
        )
