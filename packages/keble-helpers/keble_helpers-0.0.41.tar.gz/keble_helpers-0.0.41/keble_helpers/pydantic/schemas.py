# from pydantic import AnyHttpUrl as Url
# from pydantic.functional_serializers import PlainSerializer
# from typing import Annotated
#
# AnyHttpUrl = Annotated[
#     Url, PlainSerializer(lambda x: str(x), return_type=str, when_used='always')
# ]
