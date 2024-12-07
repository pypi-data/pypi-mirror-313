from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class PydanticModelConfig:

    @classmethod
    def default_dict(cls, **kwargs) -> dict:
        return {"populate_by_name": True, "alias_generator": to_camel, **kwargs}

    @classmethod
    def default(cls, **kwargs) -> ConfigDict:
        return ConfigDict(**cls.default_dict(**kwargs))
