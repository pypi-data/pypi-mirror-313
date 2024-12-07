import boto3


class Aws:

    def __init__(self, *, access_key: str, secret: str, region: str):
        """

        :param access_key: access key id
        :param secret: access key secret
        """
        self.__access_key = access_key
        self.__secret = secret
        self.__region = region

    @property
    def access_key(self):
        return self.__access_key

    @property
    def secret(self):
        return self.__secret

    def get_session(self):
        return boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret,
            region_name=self.__region
        )
