
class Aliyun:

    def __init__(self, *, access_key: str, secret: str):
        self.__access_key = access_key
        self.__secret = secret

    @property
    def access_key(self):
        return self.__access_key

    @property
    def secret(self):
        return self.__secret

